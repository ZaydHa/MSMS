import json
import csv
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

class ScheduleManager:
    """
    Core in-memory data manager with JSON persistence + finance logging + CSV export.
    Keeps data as lists of dicts for simplicity and easy Streamlit display.
    """

    def __init__(self, data_path: str = "msms.json"):
        self.data_path = data_path
        self.students: List[Dict[str, Any]] = []
        self.teachers: List[Dict[str, Any]] = []
        self.courses:  List[Dict[str, Any]] = []
        self.attendance: List[Dict[str, Any]] = []
        self.finance_log: List[Dict[str, Any]] = []     # <-- PST5 new
        self._load_data()

    # ---------- Persistence ----------
    def _load_data(self) -> None:
        p = Path(self.data_path)
        if p.exists():
            with p.open("r", encoding="utf-8") as f:
                d = json.load(f)
            self.students    = d.get("students", [])
            self.teachers    = d.get("teachers", [])
            self.courses     = d.get("courses", [])
            self.attendance  = d.get("attendance", [])
            self.finance_log = d.get("finance_log", [])
            logging.info(f"Loaded data from {self.data_path}")
        else:
            self._save_data()
            logging.info(f"Created new data file at {self.data_path}")

    def _save_data(self) -> None:
        d = {
            "students": self.students,
            "teachers": self.teachers,
            "courses": self.courses,
            "attendance": self.attendance,
            "finance_log": self.finance_log,
        }
        with Path(self.data_path).open("w", encoding="utf-8") as f:
            json.dump(d, f, indent=2)
        logging.info("Data saved.")

    # ---------- Helpers ----------
    def _student_by_id(self, student_id: int) -> Optional[Dict[str, Any]]:
        return next((s for s in self.students if s.get("id") == student_id), None)

    def _course_by_id(self, course_id: int) -> Optional[Dict[str, Any]]:
        return next((c for c in self.courses if c.get("id") == course_id), None)

    # ---------- CRUD (examples kept minimal) ----------
    def add_student(self, name: str, email: str, enrolled_course_ids: Optional[List[int]] = None) -> Dict[str, Any]:
        new_id = (max([s["id"] for s in self.students], default=0) + 1)
        s = {"id": new_id, "name": name.strip(), "email": email.strip(), "enrolled_course_ids": enrolled_course_ids or []}
        self.students.append(s)
        self._save_data()
        logging.info(f"Added student: {s}")
        return s

    def add_teacher(self, name: str, email: str) -> Dict[str, Any]:
        new_id = (max([t["id"] for t in self.teachers], default=0) + 1)
        t = {"id": new_id, "name": name.strip(), "email": email.strip()}
        self.teachers.append(t)
        self._save_data()
        logging.info(f"Added teacher: {t}")
        return t

    def add_course(self, title: str, teacher_id: int) -> Dict[str, Any]:
        if not any(t["id"] == teacher_id for t in self.teachers):
            raise ValueError("Teacher does not exist.")
        new_id = (max([c["id"] for c in self.courses], default=0) + 1)
        c = {"id": new_id, "title": title.strip(), "teacher_id": teacher_id}
        self.courses.append(c)
        self._save_data()
        logging.info(f"Added course: {c}")
        return c

    # ---------- Attendance / Roster ----------
    def check_in(self, student_id: int, course_id: int) -> bool:
        student = self._student_by_id(student_id)
        course = self._course_by_id(course_id)
        if not student or not course:
            logging.warning("Check-in failed: invalid student or course.")
            return False
        if course_id not in student.get("enrolled_course_ids", []):
            logging.warning("Check-in failed: student not enrolled in course.")
            return False
        entry = {
            "student_id": student_id,
            "course_id": course_id,
            "timestamp": datetime.now().isoformat(timespec="seconds"),
        }
        self.attendance.append(entry)
        self._save_data()
        logging.info(f"Check-in OK: {entry}")
        return True

    # ---------- FINANCE (new for PST5) ----------
    def record_payment(self, student_id: int, amount: float, method: str) -> bool:
        student = self._student_by_id(student_id)
        if not student:
            logging.error(f"record_payment failed: no student with id={student_id}")
            return False
        if amount <= 0:
            logging.error(f"record_payment failed: non-positive amount={amount}")
            return False
        payment = {
            "student_id": student_id,
            "amount": float(amount),
            "method": (method or "").strip() or "Unspecified",
            "timestamp": datetime.now().isoformat(timespec="seconds"),
        }
        self.finance_log.append(payment)
        self._save_data()
        logging.info(f"Payment recorded: {payment}")
        return True

    def get_payment_history(self, student_id: int) -> List[Dict[str, Any]]:
        history = [p for p in self.finance_log if p.get("student_id") == student_id]
        return sorted(history, key=lambda x: x["timestamp"], reverse=True)

    def export_report(self, kind: str, out_path: str) -> bool:
        kind = (kind or "").lower().strip()
        if kind == "payments":
            rows = self.finance_log
            headers = ["student_id", "amount", "method", "timestamp"]
        elif kind == "attendance":
            rows = self.attendance
            headers = ["student_id", "course_id", "timestamp"]
        else:
            logging.error(f"Unknown report kind: {kind}")
            return False
        try:
            with open(out_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                for r in rows:
                    writer.writerow({h: r.get(h, "") for h in headers})
            logging.info(f"Exported {kind} report to {out_path}")
            return True
        except Exception as e:
            logging.exception(f"Failed to export report: {e}")
            return False
