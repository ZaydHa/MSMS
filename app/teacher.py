from .user import User

class TeacherUser(User):
    def __init__(self, user_id: int, name: str, email: str = "", speciality: str = ""):
        super().__init__(user_id, name, email)
        self.speciality = speciality

    def to_dict(self) -> dict:
        d = super().to_dict()
        d["speciality"] = self.speciality
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "TeacherUser":
        return cls(
            d["id"],
            d["name"],
            d.get("email", ""),
            d.get("speciality", ""),
        )

class Course:
    def __init__(
        self,
        course_id: int,
        name: str,
        instrument: str,
        teacher_id: int,
        enrolled_student_ids=None,
        lessons=None,
    ):
        self.id = course_id
        self.name = name
        self.instrument = instrument
        self.teacher_id = teacher_id
        self.enrolled_student_ids = list(enrolled_student_ids or [])
        # lessons are dicts: {"lesson_id", "day", "start_time", "room"}
        self.lessons = list(lessons or [])

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "instrument": self.instrument,
            "teacher_id": self.teacher_id,
            "enrolled_student_ids": list(self.enrolled_student_ids),
            "lessons": list(self.lessons),
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Course":
        return cls(
            d["id"],
            d["name"],
            d.get("instrument", ""),
            d["teacher_id"],
            d.get("enrolled_student_ids", []),
            d.get("lessons", []),
        )
