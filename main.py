from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from app.catalog import Catalog
from app.main_window import MainWindow


def main() -> int:
    application = QApplication(sys.argv)
    project_root = Path(__file__).resolve().parent
    catalog = Catalog(project_root / "data" / "library.json", project_root)
    window = MainWindow(catalog)
    window.show()
    return application.exec()


if __name__ == "__main__":
    raise SystemExit(main())
