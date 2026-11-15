from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.models import Emulator, Game


class Catalog:
    def __init__(self, path: Path, project_root: Path) -> None:
        self.path = path
        self.project_root = project_root
        self.emulators: list[Emulator] = []
        self.games: list[Game] = []
        self.load()

    def load(self) -> None:
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            self.save()
            return
        except json.JSONDecodeError as error:
            raise ValueError(f"Le catalogue JSON est invalide : {self.path}") from error

        self.emulators = [Emulator.from_dict(item) for item in data.get("emulators", [])]
        self.games = [Game.from_dict(item) for item in data.get("games", [])]

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        data: dict[str, Any] = {
            "emulators": [
                {
                    "id": emulator.id,
                    "name": emulator.name,
                    "platform": emulator.platform,
                    "executable": emulator.executable,
                    "arguments": list(emulator.arguments),
                }
                for emulator in self.emulators
            ],
            "games": [
                {
                    "id": game.id,
                    "name": game.name,
                    "platform": game.platform,
                    "rom": game.rom,
                    "emulator_id": game.emulator_id,
                }
                for game in self.games
            ],
        }
        self.path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def emulator_for(self, game: Game) -> Emulator:
        for emulator in self.emulators:
            if emulator.id == game.emulator_id:
                return emulator
        raise LookupError(
            f"Aucun émulateur configuré pour le jeu « {game.name} »."
        )

    def resolve_path(self, relative_path: str) -> Path:
        return (self.project_root / relative_path).resolve()
