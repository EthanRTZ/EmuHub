from __future__ import annotations

from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.catalog import Catalog
from app.dialogs import AddEmulatorDialog, AddGameDialog
from app.launcher import launch_game
from app.models import Game


class MainWindow(QMainWindow):
    def __init__(self, catalog: Catalog) -> None:
        super().__init__()
        self.catalog = catalog
        self.setWindowTitle("EmuHub")
        self.resize(720, 480)
        self._create_menu_bar()

        self.game_list = QListWidget()
        self.launch_button = QPushButton("Lancer le jeu sélectionné")
        self.launch_button.clicked.connect(self._launch_selected_game)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Bibliothèque de jeux"))
        layout.addWidget(self.game_list)
        layout.addWidget(self.launch_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self._populate_games()

    def _create_menu_bar(self) -> None:
        file_menu = self.menuBar().addMenu("Fichier")
        add_game_action = file_menu.addAction("Ajouter un jeu…")
        add_game_action.setShortcut("Ctrl+N")
        add_game_action.triggered.connect(self._add_game)
        self.delete_game_action = file_menu.addAction("Supprimer le jeu sélectionné")
        self.delete_game_action.setShortcut("Delete")
        self.delete_game_action.triggered.connect(self._delete_selected_game)
        file_menu.addSeparator()
        file_menu.addAction("Quitter", self.close, "Ctrl+Q")

        options_menu = self.menuBar().addMenu("Options")
        options_menu.addAction("Ajouter un émulateur…", self._add_emulator)
        options_menu.addAction("Recharger le catalogue", self._reload_catalog)

    def _populate_games(self) -> None:
        self.game_list.clear()
        self.launch_button.setEnabled(bool(self.catalog.games))
        self.delete_game_action.setEnabled(bool(self.catalog.games))
        for game in self.catalog.games:
            item = QListWidgetItem(f"{game.name}  —  {game.platform}")
            item.setData(256, game)
            self.game_list.addItem(item)

        if not self.catalog.games:
            self.game_list.addItem(
                "Aucun jeu configuré. Ajoutez vos jeux dans data/library.json."
            )
            self.launch_button.setEnabled(False)
            self.delete_game_action.setEnabled(False)

    def _add_game(self) -> None:
        if not self.catalog.emulators:
            QMessageBox.information(
                self,
                "Aucun émulateur",
                "Ajoutez d’abord un émulateur depuis le menu Options.",
            )
            return

        dialog = AddGameDialog(
            self.catalog.project_root, self.catalog.emulators, self
        )
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.catalog.add_game(dialog.game())
            self._populate_games()

    def _delete_selected_game(self) -> None:
        item = self.game_list.currentItem()
        game = item.data(256) if item else None
        if not isinstance(game, Game):
            return

        answer = QMessageBox.question(
            self,
            "Supprimer le jeu",
            f"Supprimer « {game.name} » du catalogue ?\nLe fichier du jeu ne sera pas supprimé.",
        )
        if answer == QMessageBox.StandardButton.Yes:
            self.catalog.remove_game(game)
            self._populate_games()

    def _add_emulator(self) -> None:
        dialog = AddEmulatorDialog(self.catalog.project_root, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.catalog.add_emulator(dialog.emulator())

    def _reload_catalog(self) -> None:
        try:
            self.catalog.load()
            self._populate_games()
        except ValueError as error:
            QMessageBox.critical(self, "Catalogue invalide", str(error))

    def _launch_selected_game(self) -> None:
        item = self.game_list.currentItem()
        if item is None:
            return

        game = item.data(256)
        if not isinstance(game, Game):
            return

        try:
            emulator = self.catalog.emulator_for(game)
            launch_game(emulator, game, self.catalog.project_root)
        except (FileNotFoundError, LookupError) as error:
            QMessageBox.critical(self, "Impossible de lancer le jeu", str(error))
