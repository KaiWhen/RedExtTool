import os
#import json
from pathlib import Path
from PyQt5 import QtGui
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QTabWidget)
from PyQt5.QtCore import Qt
#from PyQt5.QtGui import QPixmap, QFont

from core.hotkey_manager import HotkeySignals, HotkeyManager
from ui.forest_extend_widget import ForestExtendWidget
from ui.surge_extend_widget import SurgeExtendWidget
#from core.data_loader import get_resource_path, get_temp_path, load_all_path_data
#from ui.widgets import HoverSpinBox
from ui.dialogs import HotkeyDialog

from version import __version__
from core.data_loader import get_temp_path

REDEXTTOOL_DIR = Path.home() / "AppData/Roaming/RedExtTool"
#CURR_IGT_FILE = REDEXTTOOL_DIR / "curr_igt.json"
ICON_FILE = get_temp_path("favicon.ico")


class PathFinder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"Red Extended Path Tool v{__version__}")
        self.setWindowIcon(QtGui.QIcon(ICON_FILE))
        self.setGeometry(100, 100, 700, 900)

        #self.path_data = load_all_path_data()
        #self.current_path = 2

        self.hotkey_signals = HotkeySignals()
        self.hotkey_manager = HotkeyManager(self.hotkey_signals)
        #self.setup_hotkey_connections()
        self.hotkey_manager.start()

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)

        # First tab: original UI as a widget
        forest_widget = ForestExtendWidget(hotkey_signals=self.hotkey_signals, parent=self)
        self.tab_widget.addTab(forest_widget, "Forest Extend")


        # Second tab: new UI
        surge_widget = SurgeExtendWidget(hotkey_signals=self.hotkey_signals, parent=self)
        self.tab_widget.addTab(surge_widget, "Surge Extend")

        #self.init_ui()
        #self.update_display()

    def closeEvent(self, event):
        self.hotkey_manager.stop()
        #with open(CURR_IGT_FILE, 'w') as file:
        #    json.dump({ 'Frame': 0, 'IGTSeconds': "" }, file)
        #event.accept()

    def open_hotkey_dialog(self):
        dialog = HotkeyDialog(self.hotkey_manager, self)
        dialog.exec_()
