from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.models import Emulator, Game


class AddEmulatorDialog(QDialog):
    def __init__(self, project_root: Path, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.project_root = project_root
        self.setWindowTitle("Ajouter un émulateur")

        self.name_input = QLineEdit()
        self.platform_input = QLineEdit()
        self.executable_input = QLineEdit()
        executable_button = QPushButton("Parcourir…")
        executable_button.clicked.connect(self._select_executable)

        executable_layout = QHBoxLayout()
        executable_layout.addWidget(self.executable_input)
        executable_layout.addWidget(executable_button)

        form = QFormLayout()
        form.addRow("Nom :", self.name_input)
        form.addRow("Plateforme :", self.platform_input)
        form.addRow("Exécutable :", executable_layout)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(buttons)

    def _select_executable(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Sélectionner l’exécutable de l’émulateur",
            str(self.project_root),
            "Programmes (*.exe);;Tous les fichiers (*)",
        )
        if path:
            self.executable_input.setText(path)

    def accept(self) -> None:
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Champ requis", "Le nom est obligatoire.")
            return
        if not self.platform_input.text().strip():
            QMessageBox.warning(self, "Champ requis", "La plateforme est obligatoire.")
            return
        if not self.executable_input.text().strip():
            QMessageBox.warning(
                self, "Champ requis", "L’exécutable est obligatoire."
            )
            return
        super().accept()

    def emulator(self) -> Emulator:
        return Emulator(
            id=uuid4().hex,
            name=self.name_input.text().strip(),
            platform=self.platform_input.text().strip(),
            executable=_catalog_path(self.project_root, self.executable_input.text()),
        )


class AddGameDialog(QDialog):
    def __init__(
        self,
        project_root: Path,
        emulators: list[Emulator],
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.project_root = project_root
        self.setWindowTitle("Ajouter un jeu")

        self.name_input = QLineEdit()
        self.platform_input = QLineEdit()
        self.rom_input = QLineEdit()
        rom_button = QPushButton("Parcourir…")
        rom_button.clicked.connect(self._select_rom)
        self.emulator_input = QComboBox()
        for emulator in emulators:
            self.emulator_input.addItem(
                f"{emulator.name} — {emulator.platform}", emulator
            )

        rom_layout = QHBoxLayout()
        rom_layout.addWidget(self.rom_input)
        rom_layout.addWidget(rom_button)

        form = QFormLayout()
        form.addRow("Nom :", self.name_input)
        form.addRow("Plateforme :", self.platform_input)
        form.addRow("Fichier du jeu :", rom_layout)
        form.addRow("Émulateur :", self.emulator_input)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(buttons)

    def _select_rom(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Sélectionner le fichier du jeu",
            str(self.project_root),
            "Tous les fichiers (*)",
        )
        if path:
            self.rom_input.setText(path)
            if not self.name_input.text().strip():
                self.name_input.setText(Path(path).stem)

    def accept(self) -> None:
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Champ requis", "Le nom est obligatoire.")
            return
        if not self.platform_input.text().strip():
            QMessageBox.warning(self, "Champ requis", "La plateforme est obligatoire.")
            return
        if not self.rom_input.text().strip():
            QMessageBox.warning(
                self, "Champ requis", "Le fichier du jeu est obligatoire."
            )
            return
        if self.emulator_input.currentIndex() < 0:
            QMessageBox.warning(
                self, "Champ requis", "Sélectionnez un émulateur."
            )
            return
        super().accept()

    def game(self) -> Game:
        emulator = self.emulator_input.currentData()
        if not isinstance(emulator, Emulator):
            raise ValueError("Émulateur invalide.")
        return Game(
            id=uuid4().hex,
            name=self.name_input.text().strip(),
            platform=self.platform_input.text().strip(),
            rom=_catalog_path(self.project_root, self.rom_input.text()),
            emulator_id=emulator.id,
        )


def _catalog_path(project_root: Path, selected_path: str) -> str:
    path = Path(selected_path).expanduser().resolve()
    try:
        return path.relative_to(project_root.resolve()).as_posix()
    except ValueError:
        return str(path)
