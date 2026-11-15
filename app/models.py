from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Emulator:
    id: str
    name: str
    platform: str
    executable: str
    arguments: tuple[str, ...] = ()

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Emulator:
        return cls(
            id=str(data["id"]),
            name=str(data["name"]),
            platform=str(data["platform"]),
            executable=str(data["executable"]),
            arguments=tuple(str(argument) for argument in data.get("arguments", [])),
        )


@dataclass(frozen=True)
class Game:
    id: str
    name: str
    platform: str
    rom: str
    emulator_id: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Game:
        return cls(
            id=str(data["id"]),
            name=str(data["name"]),
            platform=str(data["platform"]),
            rom=str(data["rom"]),
            emulator_id=str(data["emulator_id"]),
        )
