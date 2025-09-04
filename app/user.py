class User:
    def __init__(self, user_id: int, name: str, email: str = ""):
        self.id = user_id
        self.name = name
        self.email = email

    def to_dict(self) -> dict:
        d = {"id": self.id, "name": self.name}
        if self.email:
            d["email"] = self.email
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "User":
        # Email is optional in JSON
        return cls(d["id"], d["name"], d.get("email", ""))
