"""
Seed the database with synthetic demo data for at least 3 faculty members:
1. Dr. Ananya Rao (FAC001) - Associate Professor, Computer Science and AI
2. Dr. Rajesh Kumar (FAC002) - Professor, Electronics & Communication
3. Dr. Sneha Patil (FAC003) - Assistant Professor, Mechanical & Robotics

All data is fictional — for educational demonstration only.
"""
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from app.database.database import init_db, get_connection, DB_PATH

BASE_FACULTY_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data", "faculty")


def seed_faculty(conn, faculty_id: str, previous_scores: dict, evidence_list: list):
    fac_dir = os.path.join(BASE_FACULTY_DIR, faculty_id)
    profile_path = os.path.join(fac_dir, "profile.json")
    with open(profile_path, "r") as f:
        profile = json.load(f)

    # 1. Faculty record
    conn.execute(
        "INSERT OR REPLACE INTO faculty (faculty_id, name, department, designation, email, joining_year, academic_year) VALUES (?,?,?,?,?,?,?)",
        (profile["faculty_id"], profile["name"], profile["department"],
         profile["designation"], profile["email"], profile["joining_year"], profile["academic_year"])
    )

    # 2. Clear old evidence & validations
    conn.execute("DELETE FROM validation_results WHERE faculty_id = ?", (faculty_id,))
    conn.execute("DELETE FROM evidence WHERE faculty_id = ?", (faculty_id,))

    # 3. Insert evidence
    for ev in evidence_list:
        conn.execute(
            "INSERT INTO evidence (faculty_id, category, sub_category, title, description, file_path, year, status, metadata) VALUES (?,?,?,?,?,?,?,?,?)",
            ev
        )

    # 4. Previous appraisal for comparison (Lab 4 memory)
    conn.execute("DELETE FROM appraisal_results WHERE faculty_id = ? AND academic_year = '2025-26'", (faculty_id,))
    conn.execute(
        """INSERT INTO appraisal_results
        (faculty_id, run_id, academic_year, research_score, teaching_score, administration_score, total_score, max_score, score_breakdown, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (faculty_id, f"APP-2025-{faculty_id}", "2025-26",
         previous_scores["research"], previous_scores["teaching"], previous_scores["administration"],
         previous_scores["total"], 100.0,
         json.dumps({"summary": previous_scores.get("details", "")}),
         "APPROVED")
    )

    # 5. Scoped Memory
    scope_key = f"faculty:{faculty_id}"
    conn.execute("DELETE FROM memory WHERE scope = ?", (scope_key,))
    conn.execute(
        "INSERT OR REPLACE INTO memory (scope, key, value) VALUES (?, ?, ?)",
        (scope_key, "previous_appraisal",
         json.dumps({
             "academic_year": "2025-26",
             "total_score": previous_scores["total"],
             "max_score": 100.0,
             "research": previous_scores["research"],
             "teaching": previous_scores["teaching"],
             "administration": previous_scores["administration"]
         }))
    )
    conn.execute(
        "INSERT OR REPLACE INTO memory (scope, key, value) VALUES (?, ?, ?)",
        (scope_key, "profile", json.dumps(profile))
    )

    print(f"  [OK] Seeded {profile['name']} ({faculty_id}): {len(evidence_list)} evidence items, Prev Score: {previous_scores['total']}/100")


def seed():
    """Seed all 3 demo faculty."""
    init_db()
    conn = get_connection()
    print(f"Seeding database at {DB_PATH} ...")

    # =========================================================================
    # FAC001: Dr. Ananya Rao
    # =========================================================================
    fac001_evidence = [
        ("FAC001", "research", "publication", "Deep Learning for Smart Agriculture",
         "IEEE Transactions on AI, 2026", "research/publication_01.pdf", 2026, "pending", None),
        ("FAC001", "research", "publication", "Federated Learning in Healthcare Systems",
         "ACM Computing Surveys, 2026", "research/publication_02.pdf", 2026, "pending", None),
        ("FAC001", "research", "publication", "Transformer Architectures for Edge Devices",
         "Neural Computing and Applications, 2025", None, 2025, "pending", None),
        ("FAC001", "research", "publication", "Reinforcement Learning for Autonomous Navigation",
         "Springer AI Review, 2026", None, 2026, "pending", None),
        ("FAC001", "research", "publication", "Explainable AI in Clinical Decision Support",
         "Nature Machine Intelligence, 2025", None, 2025, "pending", None),
        ("FAC001", "research", "conference", "Agentic AI for Education",
         "AAAI 2026, Vancouver", None, 2026, "pending", None),
        ("FAC001", "research", "conference", "Privacy-Preserving ML Pipelines",
         "NeurIPS 2025, Montreal", None, 2025, "pending", None),
        ("FAC001", "research", "patent", "AI-Driven Irrigation Controller",
         "IND-PAT-2026-001, Granted", "research/patent_01.pdf", 2026, "pending", None),
        ("FAC001", "research", "project", "AI for Precision Agriculture",
         "DST-SERB, Rs 12.5L, ongoing", None, 2025, "pending", None),
        ("FAC001", "research", "project", "Federated Learning Framework",
         "AICTE, Rs 8L, completed", None, 2026, "pending", None),
        ("FAC001", "teaching", "course", "Deep Learning (CS601)",
         "Fall 2026, 4 credits, 62 students", None, 2026, "pending",
         json.dumps({"course_id": "CS601", "attendance_pct": 91.0, "feedback": 4.5, "pass_rate": 90.0})),
        ("FAC001", "teaching", "course", "Natural Language Processing (CS502)",
         "Spring 2026, 3 credits, 55 students", None, 2026, "pending",
         json.dumps({"course_id": "CS502", "attendance_pct": 91.0, "feedback": 4.1, "pass_rate": 84.9})),
        ("FAC001", "teaching", "course", "Agentic AI Systems (CS701)",
         "Fall 2026, 4 credits, 40 students", None, 2026, "pending",
         json.dumps({"course_id": "CS701", "attendance_pct": 91.25, "feedback": 4.3, "pass_rate": 90.0})),
        ("FAC001", "administration", "committee", "Board of Studies",
         "Member, active since 2026", None, 2026, "pending", None),
        ("FAC001", "administration", "committee", "Anti-Ragging Committee",
         "Member, active since 2026", None, 2026, "pending", None),
        ("FAC001", "administration", "coordinator_role", "AI Lab Coordinator",
         "Department scope, active", None, 2026, "pending", None),
        ("FAC001", "administration", "activity", "National Tech Fest Organizer",
         "Organized college-level national technical festival", None, 2026, "pending", None),
        ("FAC001", "administration", "activity", "Faculty Development Program",
         "Conducted 5-day FDP on AI and ML", None, 2026, "pending", None),
        ("FAC001", "administration", "activity", "Industry-Academia Connect",
         "Coordinated industry guest lecture series", None, 2026, "pending", None),
    ]
    seed_faculty(conn, "FAC001", {"research": 28.0, "teaching": 32.0, "administration": 14.0, "total": 74.0, "details": "4 publications, 3 courses"}, fac001_evidence)

    # =========================================================================
    # FAC002: Dr. Rajesh Kumar
    # =========================================================================
    fac002_evidence = [
        ("FAC002", "research", "publication", "Ultra-Wideband Antennas for Satellite Communications",
         "IEEE Transactions on Antennas and Propagation, 2026", "research/publication_01.pdf", 2026, "pending", None),
        ("FAC002", "research", "publication", "Low-Power VLSI Design Techniques for Bio-Telemetry",
         "ACM Transactions on Embedded Computing, 2026", None, 2026, "pending", None),
        ("FAC002", "research", "publication", "Signal Processing for 6G Wireless Networks",
         "Springer Wireless Networks, 2025", None, 2025, "pending", None),
        ("FAC002", "research", "conference", "Energy Efficient Routing in LoRaWAN Networks",
         "IEEE GLOBECOM 2026, Madrid", None, 2026, "pending", None),
        ("FAC002", "research", "patent", "Reconfigurable Metasurface for Terahertz Beamforming",
         "IND-PAT-2026-102, Granted", "research/patent_01.pdf", 2026, "pending", None),
        ("FAC002", "research", "patent", "Low-Power Wake-Up Radio Receiver",
         "IND-PAT-2025-089, Granted", None, 2025, "pending", None),
        ("FAC002", "research", "project", "Terahertz Communication Testbed",
         "ISRO-RESPOND, Rs 28L, ongoing", None, 2025, "pending", None),
        ("FAC002", "teaching", "course", "Digital Communication Systems (EC401)",
         "Fall 2026, 4 credits, 68 students", None, 2026, "pending",
         json.dumps({"course_id": "EC401", "attendance_pct": 87.5, "feedback": 4.4, "pass_rate": 91.0})),
        ("FAC002", "teaching", "course", "Wireless Sensor Networks (EC503)",
         "Spring 2026, 3 credits, 60 students", None, 2026, "pending",
         json.dumps({"course_id": "EC503", "attendance_pct": 88.5, "feedback": 4.6, "pass_rate": 91.5})),
        ("FAC002", "teaching", "course", "RF & Microwave Engineering (EC612)",
         "Fall 2026, 4 credits, 45 students", None, 2026, "pending",
         json.dumps({"course_id": "EC612", "attendance_pct": 90.5, "feedback": 4.5, "pass_rate": 91.1})),
        ("FAC002", "teaching", "course", "Advanced Antenna Systems (EC720)",
         "Spring 2026, 3 credits, 35 students", None, 2026, "pending",
         json.dumps({"course_id": "EC720", "attendance_pct": 93.5, "feedback": 4.7, "pass_rate": 97.1})),
        ("FAC002", "administration", "committee", "Research Advisory Council",
         "Convener, active 2026", None, 2026, "pending", None),
        ("FAC002", "administration", "committee", "Departmental Curriculum Committee",
         "Chairman, active 2026", None, 2026, "pending", None),
        ("FAC002", "administration", "committee", "Institution Innovation Council",
         "Vice-President, active 2026", None, 2026, "pending", None),
        ("FAC002", "administration", "coordinator_role", "Dean of Research and Consultancy",
         "Institutional leadership role, active 2026", None, 2026, "pending", None),
        ("FAC002", "administration", "activity", "International Conference on Antennas (General Chair)",
         "Chaired international IEEE antenna symposium", None, 2026, "pending", None),
        ("FAC002", "administration", "activity", "DRDO Sponsored Workshop",
         "Conducted 3-day radar systems workshop", None, 2026, "pending", None),
        ("FAC002", "administration", "activity", "Semiconductor Industry MoUs",
         "Signed bilateral training agreements with 2 semiconductor firms", None, 2026, "pending", None),
    ]
    seed_faculty(conn, "FAC002", {"research": 34.0, "teaching": 35.0, "administration": 17.0, "total": 86.0, "details": "Senior Professor benchmark"}, fac002_evidence)

    # =========================================================================
    # FAC003: Dr. Sneha Patil
    # =========================================================================
    fac003_evidence = [
        ("FAC003", "research", "publication", "Soft Robotic Grippers for Agricultural Harvesting",
         "Bio-inspiration & Biomimetics, 2026", "research/publication_01.pdf", 2026, "pending", None),
        ("FAC003", "research", "publication", "Trajectory Optimization of Quadrupedal Robots",
         "IEEE Robotics and Automation Letters, 2026", None, 2026, "pending", None),
        ("FAC003", "research", "conference", "Adaptive Impedance Control for Exoskeletons",
         "IEEE ICRA 2026, London", None, 2026, "pending", None),
        ("FAC003", "research", "project", "Bionic Prosthetic Hand Prototype",
         "SERB-TARE, Rs 6L, ongoing", None, 2026, "pending", None),
        ("FAC003", "teaching", "course", "Kinematics of Machinery (ME302)",
         "Fall 2026, 4 credits, 58 students", None, 2026, "pending",
         json.dumps({"course_id": "ME302", "attendance_pct": 92.5, "feedback": 4.7, "pass_rate": 93.1})),
        ("FAC003", "teaching", "course", "Robotics & Automation (ME405)",
         "Spring 2026, 3 credits, 52 students", None, 2026, "pending",
         json.dumps({"course_id": "ME405", "attendance_pct": 93.25, "feedback": 4.8, "pass_rate": 94.2})),
        ("FAC003", "administration", "committee", "Women in Engineering (WIE) Committee",
         "Faculty Advisor, active 2026", None, 2026, "pending", None),
        ("FAC003", "administration", "coordinator_role", "Robotics Club Faculty In-Charge",
         "Department scope, active 2026", None, 2026, "pending", None),
        ("FAC003", "administration", "activity", "RoboWars Collegiate Championship",
         "Mentored student robotics team to national finals", None, 2026, "pending", None),
        ("FAC003", "administration", "activity", "3D Printing Workshop for School Students",
         "Conducted STEM community outreach workshop", None, 2026, "pending", None),
    ]
    seed_faculty(conn, "FAC003", {"research": 20.0, "teaching": 34.0, "administration": 14.0, "total": 68.0, "details": "Early career assistant professor baseline"}, fac003_evidence)

    conn.commit()
    conn.close()
    print("Database seeding completed successfully for all 3 faculty members.")


if __name__ == "__main__":
    seed()
