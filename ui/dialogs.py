from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                             QFormLayout)
from PyQt5.QtCore import Qt
from ui.widgets import HotkeyLineEdit

class HotkeyDialog(QDialog):
    def __init__(self, hotkey_manager, parent=None):
        super().__init__(parent)
        self.hotkey_manager = hotkey_manager
        self.setWindowTitle("Configure Hotkeys")
        self.setModal(True)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.init_ui()
        self.setFocus()


    def init_ui(self):
        layout = QVBoxLayout()
        
        form_layout = QFormLayout()
        
        self.inputs = {}
        hotkey_labels = {
            'hp_increase': '+ HP:',
            'hp_decrease2': '-2 HP:',
            'hp_decrease3': '-3 HP:',
            'maxhp_increase': '+ Max HP:',
            'maxhp_decrease': '- Max HP:',
            'atk_increase': '+ Atk:',
            'atk_decrease': '- Atk:',
            'def_increase': '+ Def:',
            'def_decrease': '- Def:',
            'tab_cycle': 'Cycle Paths:'
        }

        for key, label in hotkey_labels.items():
            input_field = HotkeyLineEdit()
            input_field.setText(self.hotkey_manager.hotkeys.get(key, ''))
            input_field.setPlaceholderText("e.g., ctrl+up or alt+a")
            input_field.setFocusPolicy(Qt.ClickFocus)
            self.inputs[key] = input_field
            form_layout.addRow(label, input_field)

        for input_field in self.inputs.values():
            input_field.all_inputs = self.inputs

        layout.addLayout(form_layout)

        button_layout = QHBoxLayout()

        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_hotkeys)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)

        reset_btn = QPushButton("Reset to Default")
        reset_btn.clicked.connect(self.reset_defaults)

        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(reset_btn)

        layout.addLayout(button_layout)

        self.setLayout(layout)


    def save_hotkeys(self):
        for key, input_field in self.inputs.items():
            self.hotkey_manager.hotkeys[key] = input_field.text().strip().lower()

        self.hotkey_manager.save_hotkeys()
        self.accept()


    def get_label_text(self, key):
        labels = {
            'hp_increase': '+ HP',
            'hp_decrease2': '-2 HP:',
            'hp_decrease3': '-3 HP:',
            'maxhp_increase': '+ Max HP',
            'maxhp_decrease': '- Max HP',
            'atk_increase': '+ Atk',
            'atk_decrease': '- Atk',
            'def_increase': '+ Def',
            'def_decrease': '- Def',
            'tab_cycle': 'Cycle Paths'
        }
        return labels.get(key, key)


    def reset_defaults(self):
        defaults = {
            'hp_increase': 'f1',
            'hp_decrease2': 'f2',
            'hp_decrease3': 'f3',
            'maxhp_increase': 'f4',
            'maxhp_decrease': 'f5',
            'atk_increase': 'f6',
            'atk_decrease': 'f7',
            'def_increase': 'f8',
            'def_decrease': 'f9',
            'tab_cycle': 'tab'
        }

        for key, default_value in defaults.items():
            self.inputs[key].setText(default_value)
