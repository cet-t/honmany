from typing_extensions import TypedDict


class BetDict(TypedDict):
    enable: bool
    points: int


class UserDict(TypedDict):
    name: str
    id: int
    created: str
    nicks: list[str]
    bet: BetDict
