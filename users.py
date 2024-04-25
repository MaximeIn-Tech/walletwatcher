from dataclasses import dataclass


@dataclass
class user:
    id: int
    subscription: bool
    language: str
