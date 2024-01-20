from typing import TypedDict


class GambleDict(TypedDict):
    enable: bool
    points: int


class UserDict(TypedDict):
    name: str
    id: int
    created: str
    nicks: list[str]
    bet: GambleDict
