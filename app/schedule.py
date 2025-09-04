import json
import datetime
from pathlib import Path

from .student import StudentUser
from .teacher import TeacherUser, Course

class ScheduleManager:
    def __init__(self, data_path: str = "data/msms.json"):
        # save where the data file lives
        self.data_path = Path(data_path)
        # empty lists to hold objects
        self.students = []
        self.teachers = []
        self.courses = []
        # attendance log (important for PST3)
        self.attendance_log = []
        # load existing data
        self._load_data()

    def _load_data(self):
        """Load students, teachers, courses, attendance from JSON file"""
        if not self.data_path.exists():
            # no file yet, just start empty
            self.students = []
            self.teachers = []
            self.courses = []
            self.attendance_log = []
            return

        with open(self.data_path, "r", encoding="utf-8") as f:
            raw = json.load(f)

        # build Python objects from JSON
        self.students = []
        for s in raw.get("students", []):
            self.students.append(StudentUser.from_dict(s))

        self.teachers = []
        for t in raw.get("teachers", []):
            self.teachers.append(TeacherUser.from_dict(t))

        self.courses = []
        for c in raw.get("courses", []):
            self.courses.append(Course.from_dict(c))

        self.attendance_log = raw.get("attendance", [])

    def _save_data(self):
        """Save everything back into JSON"""
        payload = {
            "students": [],
            "teachers": [],
            "courses": [],
            "attendance": self.attendance_log
        }

        for s in self.students:
            payload["students"].append(s.to_dict())
        for t in self.teachers:
            payload["teachers"].append(t.to_dict())
        for c in self.courses:
            payload["courses"].append(c.to_dict())

        with open(self.data_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)

    # ===== helper find methods =====
    def find_student_by_id(self, student_id: int):
        for s in self.students:
            if s.id == student_id:
                return s
        return None

    def find_teacher_by_id(self, teacher_id: int):
        for t in self.teachers:
            if t.id == teacher_id:
                return t
        return None

    def find_course_by_id(self, course_id: int):
        for c in self.courses:
            if c.id == course_id:
                return c
        return None

    # ===== roster helpers =====
    def get_daily_roster(self, day: str):
        result = []
        for c in self.courses:
            for les in c.lessons:
                if les.get("day", "").lower() == day.lower():
                    info = {
                        "lesson_id": les.get("lesson_id"),
                        "day": les.get("day"),
                        "time": les.get("start_time"),
                        "room": les.get("room"),
                        "course": c,
                        "teacher": self.find_teacher_by_id(c.teacher_id),
                        "students": []
                    }
                    for sid in c.enrolled_student_ids:
                        st = self.find_student_by_id(sid)
                        if st:
                            info["students"].append(st)
                    result.append(info)
        return result

    def get_courses_for_teacher(self, teacher_id: int, day: str = None):
        result = []
        for c in self.courses:
            if c.teacher_id == teacher_id:
                if day:
                    for les in c.lessons:
                        if les.get("day", "").lower() == day.lower():
                            result.append(c)
                            break
                else:
                    result.append(c)
        return result

    def get_courses_for_student(self, student_id: int, day: str = None):
        result = []
        for c in self.courses:
            if student_id in c.enrolled_student_ids:
                if day:
                    for les in c.lessons:
                        if les.get("day", "").lower() == day.lower():
                            result.append(c)
                            break
                else:
                    result.append(c)
        return result

    # ===== Fragment 3.3 check_in (from template) =====
    def check_in(self, student_id, course_id):
        student = self.find_student_by_id(student_id)
        course = self.find_course_by_id(course_id)

        if not student or not course:
            print("Error: Check-in failed. Invalid Student or Course ID.")
            return False

        timestamp = datetime.datetime.now().isoformat()
        record = {"student_id": student_id, "course_id": course_id, "timestamp": timestamp}
        self.attendance_log.append(record)
        self._save_data()
        print("Checked in", student.name, "for", course.name, "at", timestamp)
        return True
