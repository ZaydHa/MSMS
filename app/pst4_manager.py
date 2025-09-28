# app/pst4_manager.py
from __future__ import annotations
import json
from pathlib import Path
from typing import Optional, Tuple, List

DATA_FILE = Path("data/msms.json")

class Student:
    def __init__(self, _id: int, name: str):
        self.id = _id
        self.name = name
        self.enrolled_course_ids: List[int] = []

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "enrolled_course_ids": self.enrolled_course_ids,
        }

class Course:
    def __init__(self, _id: int, name: str, instrument: str, teacher_id: int):
        self.id = _id
        self.name = name
        self.instrument = instrument
        self.teacher_id = teacher_id
        self.enrolled_student_ids: List[int] = []
        # lessons: list of {"day": "...", "time": "..."}
        self.lessons: List[dict] = []

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "instrument": self.instrument,
            "teacher_id": self.teacher_id,
            "enrolled_student_ids": self.enrolled_student_ids,
            "lessons": self.lessons,
        }

class Teacher:
    def __init__(self, _id: int, name: str, speciality: str):
        self.id = _id
        self.name = name
        self.speciality = speciality

    def to_dict(self):
        return {"id": self.id, "name": self.name, "speciality": self.speciality}

class ScheduleManager:
    """
    Minimal, PST4-friendly manager with the exact methods the GUI calls.
    Self-contained and safe: does not modify your PST3 code.
    """

    def __init__(self, data_path: str | None = None):
        self.data_path = Path(data_path) if data_path else DATA_FILE
        self.students: List[Student] = []
        self.teachers: List[Teacher] = []
        self.courses:  List[Course]  = []
        self._load_or_seed()

    # ------------- persistence -------------
    def _load_or_seed(self):
        if not self.data_path.exists():
            # seed demo data
            self.students = [Student(1, "Ava Wong"), Student(2, "Ben Lee")]
            self.teachers = [Teacher(1, "Ms Smith", "Piano"), Teacher(2, "Mr Khan", "Guitar")]
            self.courses  = [Course(1, "Beginner Piano A", "Piano", 1),
                             Course(2, "Guitar Jam 101", "Guitar", 2)]
            self.courses[0].lessons = [
                {"day": "Monday", "time": "16:00"},
                {"day": "Wednesday", "time": "17:00"},
            ]
            self.courses[1].lessons = [{"day": "Tuesday", "time": "15:30"}]
            self._save()
            return

        data = json.loads(self.data_path.read_text())
        self.students = []
        for s in data.get("students", []):
            st = Student(int(s["id"]), s["name"])
            st.enrolled_course_ids = s.get("enrolled_course_ids", [])
            self.students.append(st)

        self.teachers = [Teacher(int(t["id"]), t["name"], t.get("speciality", ""))
                         for t in data.get("teachers", [])]

        self.courses = []
        for c in data.get("courses", []):
            cr = Course(int(c["id"]), c["name"], c.get("instrument", ""), int(c["teacher_id"]))
            cr.enrolled_student_ids = c.get("enrolled_student_ids", [])
            cr.lessons = c.get("lessons", [])
            self.courses.append(cr)

    def _save(self):
        self.data_path.parent.mkdir(parents=True, exist_ok=True)
        self.data_path.write_text(json.dumps({
            "students": [s.to_dict() for s in self.students],
            "teachers": [t.to_dict() for t in self.teachers],
            "courses":  [c.to_dict() for c in self.courses],
        }, indent=2))

    # ------------- helpers -------------
    def _next_student_id(self) -> int:
        return (max((s.id for s in self.students), default=0) + 1)

    def _get_student_by_id(self, sid: int) -> Optional[Student]:
        return next((s for s in self.students if s.id == sid), None)

    def _get_course_by_id(self, cid: int) -> Optional[Course]:
        return next((c for c in self.courses if c.id == cid), None)

    # ------------- GUI API (what Streamlit calls) -------------
    def get_student_by_name(self, name: str) -> Optional[Student]:
        n = (name or "").strip().lower()
        return next((s for s in self.students if s.name.lower() == n), None)

    def register_new_student(self, name: str, instrument: str) -> Tuple[bool, str, Optional[int]]:
        if not name.strip() or not instrument.strip():
            return False, "Name and instrument are required.", None
        if self.get_student_by_name(name):
            return False, "A student with that name already exists.", None
        st = Student(self._next_student_id(), name.strip())
        self.students.append(st)
        self._save()
        return True, f"Registered {name} for {instrument}.", st.id

    def enroll_student_in_course(self, student_id: int, course_id: int) -> Tuple[bool, str]:
        s = self._get_student_by_id(student_id)
        c = self._get_course_by_id(course_id)
        if not s or not c:
            return False, "Invalid student or course."
        if student_id in c.enrolled_student_ids:
            return False, "Student already enrolled in this course."
        c.enrolled_student_ids.append(student_id)
        if course_id not in s.enrolled_course_ids:
            s.enrolled_course_ids.append(course_id)
        self._save()
        return True, "Enrollment successful."

    def check_in(self, student_id: int, course_id: int) -> Tuple[bool, str]:
        c = self._get_course_by_id(course_id)
        if not c:
            return False, "Course not found."
        if student_id not in c.enrolled_student_ids:
            return False, "Student is not enrolled in this course."
        return True, "Check-in recorded."

    def roster_for_day(self, day: str) -> List[dict]:
        rows: List[dict] = []
        for c in self.courses:
            for ls in c.lessons:
                if ls.get("day") == day:
                    tname = next((t.name for t in self.teachers if t.id == c.teacher_id), "?")
                    rows.append({
                        "Course": c.name,
                        "Instrument": c.instrument,
                        "Teacher": tname,
                        "Day": ls.get("day"),
                        "Time": ls.get("time"),
                        "Course ID": c.id,
                    })
        return rows
