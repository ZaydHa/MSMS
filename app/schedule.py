import json
import datetime
from pathlib import Path

from .student import StudentUser
from .teacher import TeacherUser, Course

class ScheduleManager:
    def __init__(self, data_path: str = "data/msms.json"):
        self.data_path = Path(data_path)

        # core in-memory lists
        self.students = []
        self.teachers = []
        self.courses = []

        # attendance log (now supports status)
        self.attendance_log = []

        # simple counters (auto-increment); safe defaults
        self.next_student_id = 1
        self.next_teacher_id = 1
        self.next_course_id  = 100

        self._load_data()

    # ----------------- persistence -----------------
    def _load_data(self):
        """Load students, teachers, courses, ids, attendance from JSON file"""
        if not self.data_path.exists():
            self.students = []
            self.teachers = []
            self.courses = []
            self.attendance_log = []
            self.next_student_id = 1
            self.next_teacher_id = 1
            self.next_course_id  = 100
            return

        with open(self.data_path, "r", encoding="utf-8") as f:
            raw = json.load(f)

        # objects
        self.students = [StudentUser.from_dict(s) for s in raw.get("students", [])]
        self.teachers = [TeacherUser.from_dict(t) for t in raw.get("teachers", [])]

        self.courses = []
        for c in raw.get("courses", []):
            self.courses.append(
                Course(
                    course_id=c.get("id"),
                    name=c.get("name", ""),
                    instrument=c.get("instrument", ""),
                    teacher_id=c.get("teacher_id"),
                    enrolled_student_ids=c.get("enrolled_student_ids", []),
                    lessons=c.get("lessons", []),
                )
            )

        # attendance: accept old or new shape (with/without status)
        self.attendance_log = raw.get("attendance", [])

        # next ids (fall back if missing)
        self.next_student_id = raw.get("next_student_id", self._calc_next_id(self.students))
        self.next_teacher_id = raw.get("next_teacher_id", self._calc_next_id(self.teachers))
        # if not present, base on existing course ids
        self.next_course_id  = raw.get("next_course_id", self._calc_next_course_id(self.courses))

    def _save_data(self):
        """Save everything back into JSON (including next_id counters)"""
        payload = {
            "students": [s.to_dict() for s in self.students],
            "teachers": [t.to_dict() for t in self.teachers],
            "courses": [c.__dict__ for c in self.courses],  # simple dict save
            "attendance": self.attendance_log,
            "next_student_id": self.next_student_id,
            "next_teacher_id": self.next_teacher_id,
            "next_course_id": self.next_course_id,
        }
        self.data_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.data_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)

    def _calc_next_id(self, objs):
        max_id = 0
        for o in objs:
            if getattr(o, "id", 0) > max_id:
                max_id = o.id
        return max_id + 1 if max_id >= 1 else 1

    def _calc_next_course_id(self, courses):
        max_id = 99
        for c in courses:
            if getattr(c, "id", 0) > max_id:
                max_id = c.id
        # start courses at 100+
        return max_id + 1

    # ----------------- find helpers -----------------
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

    # ----------------- roster & schedules -----------------
    def get_daily_roster(self, day: str):
        """Flatten lessons on the given day with course/teacher/student details."""
        result = []
        if not day:
            return result
        d = day.strip().lower()
        for c in self.courses:
            for les in c.lessons:
                if str(les.get("day", "")).strip().lower() == d:
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
                    d = day.strip().lower()
                    for les in c.lessons:
                        if str(les.get("day", "")).strip().lower() == d:
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
                    d = day.strip().lower()
                    for les in c.lessons:
                        if str(les.get("day", "")).strip().lower() == d:
                            result.append(c)
                            break
                else:
                    result.append(c)
        return result

    # ----------------- Feature 1: attendance status -----------------
    def check_in(self, student_id, course_id, status="present"):
        """
        Records attendance with a simple status: 'present', 'late', or 'absent'.
        Status is optional; defaults to 'present'.
        """
        student = self.find_student_by_id(student_id)
        course = self.find_course_by_id(course_id)

        if not student or not course:
            print("Error: Check-in failed. Invalid Student or Course ID.")
            return False

        timestamp = datetime.datetime.now().isoformat()
        record = {
            "student_id": student_id,
            "course_id": course_id,
            "timestamp": timestamp,
            "status": status
        }
        self.attendance_log.append(record)
        self._save_data()
        print("Checked in", student.name, "for", course.name, "at", timestamp, "| status:", status)
        return True

    def list_attendance(self, student_id=None, course_id=None):
        """Return filtered attendance records (very basic)."""
        results = []
        for r in self.attendance_log:
            if student_id is not None and r.get("student_id") != student_id:
                continue
            if course_id is not None and r.get("course_id") != course_id:
                continue
            results.append(r)
        return results

    # ----------------- Feature 2: add entities -----------------
    def add_student(self, name, email=""):
        new_id = self.next_student_id
        self.next_student_id += 1
        new_student = StudentUser(new_id, name, email, enrolled_course_ids=[])
        self.students.append(new_student)
        self._save_data()
        print("Added student:", new_student.name, "(ID:", new_student.id, ")")
        return new_student

    def add_teacher(self, name, speciality="", email=""):
        new_id = self.next_teacher_id
        self.next_teacher_id += 1
        new_teacher = TeacherUser(new_id, name, email, speciality)
        self.teachers.append(new_teacher)
        self._save_data()
        print("Added teacher:", new_teacher.name, "(ID:", new_teacher.id, ")")
        return new_teacher

    def add_course(self, name, instrument, teacher_id):
        teacher = self.find_teacher_by_id(teacher_id)
        if teacher is None:
            print("Error: teacher not found.")
            return None
        new_id = self.next_course_id
        self.next_course_id += 1
        course = Course(
            course_id=new_id,
            name=name,
            instrument=instrument,
            teacher_id=teacher_id,
            enrolled_student_ids=[],
            lessons=[]
        )
        self.courses.append(course)
        self._save_data()
        print("Added course:", course.name, "(ID:", course.id, ")", "Teacher:", teacher.name)
        return course

    # ----------------- Feature 3: enrol / unenrol -----------------
    def enrol_student(self, course_id, student_id):
        course = self.find_course_by_id(course_id)
        student = self.find_student_by_id(student_id)
        if not course or not student:
            print("Error: invalid course or student id.")
            return False
        if student_id not in course.enrolled_student_ids:
            course.enrolled_student_ids.append(student_id)
            self._save_data()
        print("Enrolled", student.name, "in", course.name)
        return True

    def unenrol_student(self, course_id, student_id):
        course = self.find_course_by_id(course_id)
        student = self.find_student_by_id(student_id)
        if not course or not student:
            print("Error: invalid course or student id.")
            return False
        if student_id in course.enrolled_student_ids:
            course.enrolled_student_ids.remove(student_id)
            self._save_data()
        print("Unenrolled", student.name, "from", course.name)
        return True

    # ----------------- optional: add a lesson to a course -----------------
    def add_lesson(self, course_id, day, start_time, room):
        course = self.find_course_by_id(course_id)
        if not course:
            print("Error: course not found.")
            return False
        # basic lesson_id: 1 + number of lessons
        next_lesson_id = 1
        if course.lessons:
            # find max existing
            mx = 0
            for l in course.lessons:
                if int(l.get("lesson_id", 0)) > mx:
                    mx = int(l.get("lesson_id", 0))
            next_lesson_id = mx + 1
        lesson = {"lesson_id": next_lesson_id, "day": day, "start_time": start_time, "room": room}
        course.lessons.append(lesson)
        self._save_data()
        print("Added lesson to", course.name, "->", day, start_time, room)
        return True
