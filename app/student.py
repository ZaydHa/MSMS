from .user import User

class StudentUser(User):
    def __init__(self, user_id: int, name: str, email: str = "", enrolled_course_ids=None):
        super().__init__(user_id, name, email)
        self.enrolled_course_ids = list(enrolled_course_ids or [])

    def to_dict(self) -> dict:
        d = super().to_dict()
        d["enrolled_course_ids"] = list(self.enrolled_course_ids)
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "StudentUser":
        return cls(
            d["id"],
            d["name"],
            d.get("email", ""),
            d.get("enrolled_course_ids", []),
        )

