from __future__ import annotations

from PySide6.QtWidgets import (
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
from app.launcher import launch_game
from app.models import Game


class MainWindow(QMainWindow):
    def __init__(self, catalog: Catalog) -> None:
        super().__init__()
        self.catalog = catalog
        self.setWindowTitle("EmuHub")
        self.resize(720, 480)

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

    def _populate_games(self) -> None:
        self.game_list.clear()
        for game in self.catalog.games:
            item = QListWidgetItem(f"{game.name}  —  {game.platform}")
            item.setData(256, game)
            self.game_list.addItem(item)

        if not self.catalog.games:
            self.game_list.addItem(
                "Aucun jeu configuré. Ajoutez vos jeux dans data/library.json."
            )
            self.launch_button.setEnabled(False)

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
