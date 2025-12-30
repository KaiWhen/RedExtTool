import os
import json
from pathlib import Path
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QGroupBox, QScrollArea, QTabWidget,
                             QTextEdit, QPushButton)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont

from core.hotkey_manager import HotkeySignals
from core.data_loader import get_resource_path, get_temp_path, load_forest_path_data
from core.file_utils import save_curr_igt
from ui.widgets import HoverSpinBox

from version import __version__

REDEXTTOOL_DIR = Path.home() / "AppData/Roaming/RedExtTool"
CURR_IGT_FILE = REDEXTTOOL_DIR / "curr_igt.json"
ICON_FILE = get_temp_path("favicon.ico")


class ForestExtendWidget(QWidget):
    def __init__(self, hotkey_signals: HotkeySignals = None, parent=None):
        super().__init__(parent)

        self.path_data = load_forest_path_data()
        self.current_path = 2

        self.hotkey_signals = hotkey_signals
        if self.hotkey_signals is not None:
            self.setup_hotkey_connections()

        self.init_ui()
        self.update_display()


    def setup_hotkey_connections(self):
        self.hotkey_signals.hp_increase.connect(lambda: self.change_stat('hp', 1))
        self.hotkey_signals.hp_decrease2.connect(lambda: self.change_stat('hp', -2))
        self.hotkey_signals.hp_decrease3.connect(lambda: self.change_stat('hp', -3))
        self.hotkey_signals.maxhp_increase.connect(lambda: self.change_stat('maxhp', 1))
        self.hotkey_signals.maxhp_decrease.connect(lambda: self.change_stat('maxhp', -1))
        self.hotkey_signals.atk_increase.connect(lambda: self.change_stat('atk', 1))
        self.hotkey_signals.atk_decrease.connect(lambda: self.change_stat('atk', -1))
        self.hotkey_signals.def_increase.connect(lambda: self.change_stat('def', 1))
        self.hotkey_signals.def_decrease.connect(lambda: self.change_stat('def', -1))
        self.hotkey_signals.tab_cycle.connect(lambda: self.cycle_tab(False))
        self.hotkey_signals.tab_cycle_reverse.connect(lambda: self.cycle_tab(True))


    def change_stat(self, stat_name, delta):
        spinbox_map = {
            'hp': self.hp_spin,
            'maxhp': self.maxhp_spin,
            'atk': self.atk_spin,
            'def': self.def_spin
        }

        spinbox = spinbox_map.get(stat_name)
        if spinbox:
            new_value = spinbox.value() + delta
            if spinbox.minimum() <= new_value <= spinbox.maximum():
                spinbox.setValue(new_value)


    def cycle_tab(self, reverse: bool):
        current_index = self.tab_widget.currentIndex()
        next_index = (current_index + (-1 if reverse else 1)) % self.tab_widget.count()
        self.tab_widget.setCurrentIndex(next_index)


    def init_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        content_layout = QHBoxLayout()

        left_layout = self.create_left_section()
        content_layout.addLayout(left_layout)

        right_layout = self.create_right_section()
        content_layout.addWidget(right_layout, stretch=1)

        main_layout.addLayout(content_layout)

        bottom_bar = QHBoxLayout()

        self.hotkey_btn = QPushButton("⚙ Configure Hotkeys")
        self.hotkey_btn.clicked.connect(self._request_open_hotkey_dialog)

        bottom_bar.addWidget(self.hotkey_btn)
        bottom_bar.addStretch()
        main_layout.addLayout(bottom_bar)


    def _request_open_hotkey_dialog(self):
        win = self.window()
        if win and hasattr(win, "open_hotkey_dialog"):
            win.open_hotkey_dialog()
        else:
            print("open_hotkey_dialog not found on parent/window")


    def create_left_section(self):
        layout = QVBoxLayout()

        stats_group = QGroupBox("Squirtle Stats")
        stats_form = QVBoxLayout()

        label_minw = 80
        box_height = 30

        # HP
        hp_layout = QHBoxLayout()
        hp_label = QLabel("HP:")
        hp_label.setMinimumWidth(label_minw)
        self.hp_spin = HoverSpinBox()
        self.hp_spin.setFixedHeight(box_height)
        self.hp_spin.setRange(12, 23)
        self.hp_spin.setValue(22)
        self.hp_spin.valueChanged.connect(self.update_display)
        hp_layout.addWidget(hp_label)
        hp_layout.addWidget(self.hp_spin)
        stats_form.addLayout(hp_layout)

        # Max HP
        maxhp_layout = QHBoxLayout()
        maxhp_label = QLabel("Max HP:")
        maxhp_label.setMinimumWidth(label_minw)
        self.maxhp_spin = HoverSpinBox()
        self.maxhp_spin.setFixedHeight(box_height)
        self.maxhp_spin.setRange(21, 23)
        self.maxhp_spin.setValue(22)
        self.maxhp_spin.valueChanged.connect(self.update_display)
        maxhp_layout.addWidget(maxhp_label)
        maxhp_layout.addWidget(self.maxhp_spin)
        stats_form.addLayout(maxhp_layout)

        # Atk
        atk_layout = QHBoxLayout()
        atk_label = QLabel("Attack:")
        atk_label.setMinimumWidth(label_minw)
        self.atk_spin = HoverSpinBox()
        self.atk_spin.setFixedHeight(box_height)
        self.atk_spin.setRange(10, 12)
        self.atk_spin.setValue(11)
        self.atk_spin.valueChanged.connect(self.update_display)
        atk_layout.addWidget(atk_label)
        atk_layout.addWidget(self.atk_spin)
        stats_form.addLayout(atk_layout)

        # Def
        def_layout = QHBoxLayout()
        def_label = QLabel("Defense:")
        def_label.setMinimumWidth(label_minw)
        self.def_spin = HoverSpinBox()
        self.def_spin.setFixedHeight(box_height)
        self.def_spin.setRange(12, 14)
        self.def_spin.setValue(13)
        self.def_spin.valueChanged.connect(self.update_display)
        def_layout.addWidget(def_label)
        def_layout.addWidget(self.def_spin)
        stats_form.addLayout(def_layout)

        stats_group.setLayout(stats_form)
        layout.addWidget(stats_group)

        # target frames
        frames_group = QGroupBox("Target IGT Frames")
        frames_layout = QVBoxLayout()

        self.frames_label = QLabel("Nothing found for this turtle :(")
        self.frames_label.setStyleSheet("font-size: 12pt; font-weight: bold;")
        self.frames_label.setWordWrap(True)
        frames_layout.addWidget(self.frames_label)

        frames_group.setLayout(frames_layout)
        layout.addWidget(frames_group)

        # igt sec failures
        igtsec_group = QGroupBox("IGT Second Failures")
        igtsec_layout = QVBoxLayout()

        self.igtsec_label = QLabel("Nothing found for this turtle :(")
        self.igtsec_label.setStyleSheet("font-size: 10pt; font-weight: semibold;")
        self.igtsec_label.setWordWrap(True)
        igtsec_layout.addWidget(self.igtsec_label)

        igtsec_group.setLayout(igtsec_layout)
        layout.addWidget(igtsec_group)

        # postfight
        postfight_group = QGroupBox("Post Fight A Press Tiles")
        postfight_layout = QVBoxLayout()

        self.postfight_label = QLabel("Nothing found for this turtle :(")
        self.postfight_label.setStyleSheet("font-size: 11pt; font-family: monospace;")
        self.postfight_label.setWordWrap(True)
        postfight_layout.addWidget(self.postfight_label)

        postfight_group.setLayout(postfight_layout)
        layout.addWidget(postfight_group)

        # frame turn logs
        logs_group = QGroupBox("Turn Logs")
        logs_layout = QVBoxLayout()

        self.logs_text = QTextEdit()
        self.logs_text.setReadOnly(True)
        self.logs_text.setMinimumHeight(400)
        font = QFont("Courier New", 9)
        self.logs_text.setFont(font)
        logs_layout.addWidget(self.logs_text)

        logs_group.setLayout(logs_layout)
        layout.addWidget(logs_group)

        layout.addStretch()

        return layout


    def create_right_section(self):
        self.tab_widget = QTabWidget()
        self.tab_widget.currentChanged.connect(self.on_tab_changed)

        # create path tabs
        self.image_labels = {}
        i = 1
        for _, data in self.path_data.items():
            tab = QWidget()
            tab_layout = QVBoxLayout()

            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)

            image_label = QLabel("No path image available")
            image_label.setAlignment(Qt.AlignCenter)
            image_label.setMinimumSize(300, 500)
            image_label.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc;")

            scroll_area.setWidget(image_label)
            tab_layout.addWidget(scroll_area)
            tab.setLayout(tab_layout)

            self.tab_widget.addTab(tab, f"P{data[next(iter(data))]['path']}")
            self.image_labels[i] = image_label

            i+=1

        return self.tab_widget


    def on_tab_changed(self, index):
        self.current_path = index + 1
        self.update_display()


    def get_stats_key(self):
        hp = self.hp_spin.value()
        maxhp = self.maxhp_spin.value()
        atk = self.atk_spin.value()
        defense = self.def_spin.value()
        return f"({hp},{maxhp},{atk},{defense})"


    def update_display(self):
        if not hasattr(self, 'image_labels') or not self.image_labels:
            return

        stats_key = self.get_stats_key()

        igtDict = {
            'Frame': 0,
            'IGTSeconds': ""
        }

        # get current path data
        path_data = self.path_data.get(self.current_path, {})
        stats_data = path_data.get(stats_key, None)

        if stats_data:
            # update igt frames
            frames = stats_data.get("frames", [])
            if frames:
                frames_str = ", ".join(map(str, frames))
                igtDict["Frame"] = float(frames[0]) + float((len(frames)-1.0) / 2.0)
                self.frames_label.setText(frames_str)
            else:
                self.frames_label.setText("No frames available")

            # update igt secs
            igtsecs = stats_data.get("igtSecs", [])
            if igtsecs:
                igtsecs_str = ", ".join(map(str, igtsecs))
                igtsec_filestr = "/".join(map(str, igtsecs))
                igtDict["IGTSeconds"] = igtsec_filestr
                self.igtsec_label.setText(igtsecs_str)
            else:
                self.igtsec_label.setText("No IGT seconds available")

            save_curr_igt(CURR_IGT_FILE, igtDict)

            # update postfight
            postfight = stats_data.get("postFight", "")
            if postfight and postfight != "":
                apress_list = []
                i = 0
                postfight = postfight.replace('L', '')
                for c in postfight:
                    if c == 'A':
                        apress_list.append(i)
                    else:
                        i += 1
                postfight_str = ", ".join(map(str, apress_list))
                self.postfight_label.setText(f"{postfight_str}")
            else:
                self.postfight_label.setText("No Post Fight Path data")

            # update frame logs
            frame_logs = stats_data.get("frameLogs", {})
            if frame_logs:
                log_text = ""
                for frame, logs in frame_logs.items():
                    log_text += f"=== Frame {frame} ===\n"
                    for i, log_entry in enumerate(logs, 1):
                        log_text += f"  {i-1}: {log_entry}\n"
                    log_text += "\n"
                self.logs_text.setPlainText(log_text.strip())
            else:
                self.logs_text.setPlainText("No frame logs available")

            path = stats_data.get("path", self.current_path)
            stats = [int(x) for x in stats_key.strip("()").split(",")]
            stats_str = "_".join(str(x) for x in stats)
            image_path = get_resource_path(f"path_data/forest/p{path}/path_images/{stats_str}.png")

            if os.path.exists(image_path):
                pixmap = QPixmap(image_path)
                image_label = self.image_labels[self.current_path]
                scaled_pixmap = pixmap.scaled(
                    image_label.size(), 
                    Qt.KeepAspectRatio, 
                    Qt.SmoothTransformation
                )
                image_label.setPixmap(scaled_pixmap)
            else:
                self.image_labels[self.current_path].setText(f"Image not found:\n{image_path}")
        else:
            self.frames_label.setText("No data for this turtle/path :(")
            self.igtsec_label.setText("No data for this turtle/path :(")
            self.postfight_label.setText("No data for this turtle/path :(")
            self.logs_text.setPlainText("No data for this turtle/path :(")
            self.image_labels[self.current_path].setText("No matching path found for these stats")
