import json
import os
from pathlib import Path
from PyQt5.QtCore import QObject, pyqtSignal
from pynput import keyboard
from pynput.keyboard import Key, KeyCode


REDEXTTOOL_DIR = Path.home() / "AppData/Roaming/RedExtTool"
CONFIG_DIR = REDEXTTOOL_DIR / "config"
CONFIG_FILE = CONFIG_DIR / "hotkeys.json"


class HotkeySignals(QObject):
    hp_increase = pyqtSignal()
    hp_decrease2 = pyqtSignal()
    hp_decrease3 = pyqtSignal()
    maxhp_decrease = pyqtSignal()
    maxhp_increase = pyqtSignal()
    atk_decrease = pyqtSignal()
    atk_increase = pyqtSignal()
    def_decrease = pyqtSignal()
    def_increase = pyqtSignal()
    tab_cycle = pyqtSignal()
    tab_cycle_reverse = pyqtSignal()
    main_tab_cycle = pyqtSignal()


class HotkeyManager:
    def __init__(self, signals):
        self.signals = signals
        self.listener = None
        self.hotkeys = self.load_default_hotkeys()
        self.current_keys = set()


    def load_default_hotkeys(self):
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r') as f:
                    return json.load(f)
        except:
            os.mkdir(CONFIG_FILE)
        
        return {
            'hp_increase': 'f1',
            'hp_decrease2': 'f2',
            'hp_decrease3': 'f3',
            'maxhp_decrease': 'f4',
            'maxhp_increase': 'f5',
            'atk_decrease': 'f6',
            'atk_increase': 'f7',
            'def_decrease': 'f8',
            'def_increase': 'f9',
            'tab_cycle': 'tab',
            'tab_cycle_reverse': 'shift+tab',
            'main_tab_cycle': 'ctrl+tab'
        }


    def save_hotkeys(self):
        try:
            os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
            with open(CONFIG_FILE, 'w') as f:
                json.dump(self.hotkeys, f, indent=4)
        except Exception as e:
            print(f"Error saving hotkeys: {e}")


    def parse_hotkey(self, hotkey_string):
        parts = hotkey_string.lower().split('+')
        keys = set()

        for part in parts:
            part = part.strip()

            # Modifiers
            if part == 'ctrl':
                keys.add(Key.ctrl_l)
                keys.add(Key.ctrl_r)
            elif part == 'shift':
                keys.add(Key.shift_l)
                keys.add(Key.shift_r)
            elif part == 'alt':
                keys.add(Key.alt_l)
                keys.add(Key.alt_r)
            # F keys
            elif part in ['f1', 'f2', 'f3', 'f4', 'f5', 'f6', 
                         'f7', 'f8', 'f9', 'f10', 'f11', 'f12']:
                keys.add(getattr(Key, part))
            # Arrow keys
            elif part == 'up':
                keys.add(Key.up)
            elif part == 'down':
                keys.add(Key.down)
            elif part == 'left':
                keys.add(Key.left)
            elif part == 'right':
                keys.add(Key.right)
            # Special keys
            elif part == 'tab':
                keys.add(Key.tab)
            elif part == 'space':
                keys.add(Key.space)
            elif part == 'enter':
                keys.add(Key.enter)
            elif part == 'backspace':
                keys.add(Key.backspace)
            elif part == 'delete':
                keys.add(Key.delete)
            # Single character keys
            elif len(part) == 1 and part.isalnum():
                keys.add(KeyCode.from_char(part))

        return keys


    def check_hotkey(self, hotkey_name):
        hotkey_string = self.hotkeys.get(hotkey_name, '')
        if not hotkey_string:
            return False

        required_keys = self.parse_hotkey(hotkey_string)

        if len(required_keys) == 0:
            return False

        for req_key in required_keys:
            if req_key not in self.current_keys:
                if isinstance(req_key, Key):
                    if req_key == Key.ctrl_l or req_key == Key.ctrl_r:
                        if Key.ctrl_l not in self.current_keys and Key.ctrl_r not in self.current_keys:
                            return False
                    elif req_key == Key.shift_l or req_key == Key.shift_r:
                        if Key.shift_l not in self.current_keys and Key.shift_r not in self.current_keys:
                            return False
                    elif req_key == Key.alt_l or req_key == Key.alt_r:
                        if Key.alt_l not in self.current_keys and Key.alt_r not in self.current_keys:
                            return False
                    else:
                        return False
                else:
                    return False

        required_has_ctrl = any(k in required_keys for k in [Key.ctrl_l, Key.ctrl_r])
        required_has_shift = any(k in required_keys for k in [Key.shift_l, Key.shift_r])
        required_has_alt = any(k in required_keys for k in [Key.alt_l, Key.alt_r])

        current_has_ctrl = any(k in self.current_keys for k in [Key.ctrl_l, Key.ctrl_r])
        current_has_shift = any(k in self.current_keys for k in [Key.shift_l, Key.shift_r])
        current_has_alt = any(k in self.current_keys for k in [Key.alt_l, Key.alt_r])

        if current_has_ctrl and not required_has_ctrl:
            return False
        if current_has_shift and not required_has_shift:
            return False
        if current_has_alt and not required_has_alt:
            return False

        return True


    def on_press(self, key):
        self.current_keys.add(key)

        if self.check_hotkey('hp_increase'):
            self.signals.hp_increase.emit()
        elif self.check_hotkey('hp_decrease2'):
            self.signals.hp_decrease2.emit()
        elif self.check_hotkey('hp_decrease3'):
            self.signals.hp_decrease3.emit()
        elif self.check_hotkey('maxhp_increase'):
            self.signals.maxhp_increase.emit()
        elif self.check_hotkey('maxhp_decrease'):
            self.signals.maxhp_decrease.emit()
        elif self.check_hotkey('atk_increase'):
            self.signals.atk_increase.emit()
        elif self.check_hotkey('atk_decrease'):
            self.signals.atk_decrease.emit()
        elif self.check_hotkey('def_increase'):
            self.signals.def_increase.emit()
        elif self.check_hotkey('def_decrease'):
            self.signals.def_decrease.emit()
        elif self.check_hotkey('tab_cycle'):
            self.signals.tab_cycle.emit()
        elif self.check_hotkey('tab_cycle_reverse'):
            self.signals.tab_cycle_reverse.emit()
        elif self.check_hotkey('main_tab_cycle'):
            self.signals.main_tab_cycle.emit()


    def on_release(self, key):
        if key in self.current_keys:
            self.current_keys.remove(key)


    def start(self):
        if self.listener is None:
            self.listener = keyboard.Listener(
                on_press=self.on_press,
                on_release=self.on_release
            )
            self.listener.start()


    def stop(self):
        if self.listener:
            self.listener.stop()
            self.listener = None
