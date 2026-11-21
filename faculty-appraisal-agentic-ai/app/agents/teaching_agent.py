"""
Teaching-Learning Data Collection Agent (Domain Agent 2)
Responsibilities:
- Read teaching data
- Analyze courses
- Analyze attendance
- Analyze student feedback
- Analyze academic results
- Return structured teaching data
"""
from typing import Dict, Any
from app.agents.base_agent import BaseAgent


class TeachingLearningDataCollectionAgent(BaseAgent):
    def __init__(self, runtime):
        super().__init__("Teaching-Learning Data Collection Agent", runtime)

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        faculty_id = context.get("faculty_id")
        run_id = context.get("run_id")

        # 1. PLAN
        self.record_step(
            stage="PLAN",
            message=f"Plan to aggregate teaching records for faculty {faculty_id}. Target sets: courses, monthly attendance, student evaluations, course results.",
        )

        # 2. ACT
        self.record_step(
            stage="ACT",
            message="Invoking 'teaching_appraisal' skill via Agent Runtime.",
        )
        task_result = self.runtime.receive_task(
            task_description="Execute teaching_appraisal metrics analysis",
            task_input={"faculty_id": faculty_id},
            run_id=run_id,
            faculty_id=faculty_id,
        )

        # 3. OBSERVE
        skill_data = task_result.get("result", {})
        summary = skill_data.get("summary", {})
        courses_count = summary.get("courses_taught", 0)
        attendance_pct = summary.get("avg_attendance_pct", 0)
        feedback_score = summary.get("avg_feedback_score", 0)
        pass_rate_pct = summary.get("pass_rate_pct", 0)

        self.record_step(
            stage="OBSERVE",
            message=f"Analyzed {courses_count} courses: Attendance={attendance_pct}%, Feedback={feedback_score}/5.0, Pass Rate={pass_rate_pct}%.",
            details=summary,
        )

        # 4. DECIDE
        decision_notes = []
        if attendance_pct < 75.0:
            decision_notes.append("Attendance below institutional standard threshold (75%).")
        if feedback_score < 3.0:
            decision_notes.append("Student feedback rating below threshold (3.0).")

        self.record_step(
            stage="DECIDE",
            message="Teaching-learning dataset validated and structured. Forwarding to coordinator.",
            details={"decision_notes": decision_notes},
        )

        return {
            "agent": self.name,
            "status": task_result.get("status", "success"),
            "data": skill_data,
            "trace_steps": self.trace_steps,
            "warnings": decision_notes,
        }
