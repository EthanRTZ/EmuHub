from __future__ import annotations

import subprocess
from pathlib import Path

from app.models import Emulator, Game


def launch_game(emulator: Emulator, game: Game, project_root: Path) -> None:
    executable = (project_root / emulator.executable).resolve()
    rom = (project_root / game.rom).resolve()

    if not executable.is_file():
        raise FileNotFoundError(f"Émulateur introuvable : {executable}")
    if not rom.is_file():
        raise FileNotFoundError(f"Jeu introuvable : {rom}")

    subprocess.Popen(
        [str(executable), *emulator.arguments, str(rom)],
        cwd=executable.parent,
    )
