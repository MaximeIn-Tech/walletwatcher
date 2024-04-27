from dataclasses import dataclass


@dataclass
class User:
    id: int
    subscription: bool
    language: str
