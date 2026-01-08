import os
import json
from pathlib import Path
from PyQt5 import QtGui
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QTabWidget)
from PyQt5.QtCore import Qt

from core.hotkey_manager import HotkeySignals, HotkeyManager
from ui.forest_extend_widget import ForestExtendWidget
from ui.surge_extend_widget import SurgeExtendWidget
from ui.dialogs import HotkeyDialog

from version import __version__
from core.data_loader import get_temp_path

REDEXTTOOL_DIR = Path.home() / "AppData/Roaming/RedExtTool"
CURR_IGT_FILE = REDEXTTOOL_DIR / "curr_igt.json"
ICON_FILE = get_temp_path("favicon.ico")


class PathFinder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"Red Extended Path Tool v{__version__}")
        self.setWindowIcon(QtGui.QIcon(ICON_FILE))
        self.setGeometry(100, 100, 700, 900)

        self.hotkey_signals = HotkeySignals()
        self.hotkey_manager = HotkeyManager(self.hotkey_signals)
        self.hotkey_manager.start()

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)

        # First tab: original UI as a widget
        self.forest_widget = ForestExtendWidget(hotkey_signals=self.hotkey_signals, parent=self)
        self.tab_widget.addTab(self.forest_widget, "Forest Extend")

        # Second tab: new UI
        self.surge_widget = SurgeExtendWidget(hotkey_signals=self.hotkey_signals, parent=self)
        self.tab_widget.addTab(self.surge_widget, "Surge Extend")

        self.setup_hotkey_connections()
        
        self.hotkey_manager.start()


    def setup_hotkey_connections(self):
        self.hotkey_signals.hp_increase.connect(self.handle_hp_increase)
        self.hotkey_signals.hp_decrease2.connect(self.handle_hp_decrease2)
        self.hotkey_signals.hp_decrease3.connect(self.handle_hp_decrease3)
        self.hotkey_signals.maxhp_increase.connect(self.handle_maxhp_increase)
        self.hotkey_signals.maxhp_decrease.connect(self.handle_maxhp_decrease)
        self.hotkey_signals.atk_increase.connect(self.handle_atk_increase)
        self.hotkey_signals.atk_decrease.connect(self.handle_atk_decrease)
        self.hotkey_signals.def_increase.connect(self.handle_def_increase)
        self.hotkey_signals.def_decrease.connect(self.handle_def_decrease)
        self.hotkey_signals.main_tab_cycle.connect(self.handle_tab_cycle)


    def get_current_widget(self):
        return self.tab_widget.currentWidget()


    def handle_hp_increase(self):
        widget = self.get_current_widget()
        if hasattr(widget, 'change_stat'):
            widget.change_stat('hp', 1)


    def handle_hp_decrease2(self):
        widget = self.get_current_widget()
        if hasattr(widget, 'change_stat'):
            widget.change_stat('hp', -2)


    def handle_hp_decrease3(self):
        widget = self.get_current_widget()
        if hasattr(widget, 'change_stat'):
            widget.change_stat('hp', -3)


    def handle_maxhp_increase(self):
        widget = self.get_current_widget()
        if hasattr(widget, 'change_stat'):
            widget.change_stat('maxhp', 1)


    def handle_maxhp_decrease(self):
        widget = self.get_current_widget()
        if hasattr(widget, 'change_stat'):
            widget.change_stat('maxhp', -1)


    def handle_atk_increase(self):
        widget = self.get_current_widget()
        if hasattr(widget, 'change_stat'):
            widget.change_stat('atk', 1)


    def handle_atk_decrease(self):
        widget = self.get_current_widget()
        if hasattr(widget, 'change_stat'):
            widget.change_stat('atk', -1)


    def handle_def_increase(self):
        widget = self.get_current_widget()
        if hasattr(widget, 'change_stat'):
            widget.change_stat('def', 1)


    def handle_def_decrease(self):
        widget = self.get_current_widget()
        if hasattr(widget, 'change_stat'):
            widget.change_stat('def', -1)


    def handle_tab_cycle(self):
        current_index = self.tab_widget.currentIndex()
        next_index = (current_index + 1) % self.tab_widget.count()
        self.tab_widget.setCurrentIndex(next_index)


    def closeEvent(self, event):
        self.hotkey_manager.stop()
        with open(CURR_IGT_FILE, 'w') as file:
           json.dump({ 'Frame': 0, 'IGTSeconds': "" }, file)
        event.accept()


    def open_hotkey_dialog(self):
        dialog = HotkeyDialog(self.hotkey_manager, self)
        dialog.exec_()
