from dataclasses import dataclass


@dataclass(frozen=True)
class Message:
    role: str
    content: str

    @classmethod
    def from_user(cls, content: str) -> "Message":
        return cls(role="user", content=content)
