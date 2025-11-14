import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import QApplication
from ui.main_window import PathFinder

REDEXTTOOL_DIR = Path.home() / "AppData/Roaming/RedExtTool"


def main():
    if not os.path.exists(REDEXTTOOL_DIR):
        os.mkdir(REDEXTTOOL_DIR)
    app = QApplication(sys.argv)
    window = PathFinder()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()