"""
Evidence Validation Skill (Lab 3)
Validates all collected evidence items for completeness, readability, file existence, and duplicates.
"""
from typing import Dict, Any, List
from app.skills.base_skill import BaseSkill


class EvidenceValidationSkill(BaseSkill):
    name = "evidence_validation"
    description = "Validate evidence items for completeness, readability, and duplicates"
    version = "1.0"
    allowed_tools = ["read_file", "read_pdf", "get_evidence", "save_validation_result"]

    def execute(self, task_input: Dict[str, Any], tool_registry, memory, **kwargs) -> Dict[str, Any]:
        faculty_id = task_input.get("faculty_id")
        run_id = task_input.get("run_id", "RUN-DEFAULT")

        if not faculty_id:
            raise ValueError("faculty_id is required for evidence_validation")

        tool_calls_trace = []

        # 1. Retrieve all registered evidence from database
        ev_call = tool_registry.execute("get_evidence", self.allowed_tools, faculty_id=faculty_id)
        tool_calls_trace.append(ev_call)
        evidence_items = ev_call.get("result", {}).get("evidence", [])

        valid_count = 0
        invalid_count = 0
        needs_review_count = 0
        validated_items = []
        seen_titles = set()

        for item in evidence_items:
            eid = item["evidence_id"]
            title = (item.get("title") or "").strip()
            category = item.get("category")
            sub_category = item.get("sub_category")
            file_path = item.get("file_path")

            status = "VALID"
            reason = "Evidence verified and complete."

            # Check 1: Empty title or description
            if not title:
                status = "INVALID"
                reason = "Missing required title or evidence metadata."

            # Check 2: Duplication check
            unique_key = f"{category}:{sub_category}:{title.lower()}"
            if unique_key in seen_titles:
                status = "INVALID"
                reason = f"Duplicate evidence item detected: '{title}'."
            else:
                seen_titles.add(unique_key)

            # Check 3: If file_path is specified, check file existence and readability
            if status != "INVALID":
                if file_path:
                    # Attempt reading file
                    if file_path.endswith(".pdf"):
                        f_read = tool_registry.execute("read_pdf", self.allowed_tools, file_path=file_path, faculty_id=faculty_id)
                    else:
                        f_read = tool_registry.execute("read_file", self.allowed_tools, file_path=file_path, faculty_id=faculty_id)
                    tool_calls_trace.append(f_read)

                    res = f_read.get("result", {})
                    if res.get("status") == "error":
                        status = "NEEDS_REVIEW"
                        reason = f"Referenced evidence file missing or unreadable: {file_path}."
                    elif res.get("status") == "rejected":
                        status = "INVALID"
                        reason = f"Access to evidence file was rejected by safety boundary: {file_path}."
                else:
                    # Some items (e.g. conference with no file uploaded yet) need review
                    if sub_category in ["conference"] and item.get("year", 2026) >= 2026:
                        status = "NEEDS_REVIEW"
                        reason = "Conference evidence submitted without attached verification PDF."

            # Count categories
            if status == "VALID":
                valid_count += 1
            elif status == "INVALID":
                invalid_count += 1
            else:
                needs_review_count += 1

            # Save validation result via tool
            save_call = tool_registry.execute(
                "save_validation_result",
                self.allowed_tools,
                evidence_id=eid,
                faculty_id=faculty_id,
                run_id=run_id,
                status=status,
                reason=reason,
            )
            tool_calls_trace.append(save_call)

            validated_items.append({
                "evidence_id": eid,
                "title": title,
                "category": category,
                "sub_category": sub_category,
                "status": status,
                "reason": reason,
                "file_path": file_path,
            })

        summary = {
            "total_evaluated": len(evidence_items),
            "VALID": valid_count,
            "INVALID": invalid_count,
            "NEEDS_REVIEW": needs_review_count,
        }

        result_data = {
            "faculty_id": faculty_id,
            "run_id": run_id,
            "summary": summary,
            "items": validated_items,
        }

        # Save to memory
        if memory:
            memory.set("validation_results", result_data)

        return {
            "status": "success",
            "data": result_data,
            "tool_calls_trace": tool_calls_trace,
        }
