from PyQt5.QtWidgets import QSpinBox, QLineEdit
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QWheelEvent


class HoverSpinBox(QSpinBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setMouseTracking(True)


    def wheelEvent(self, event: QWheelEvent):
        """Allow scroll without focus"""
        had_focus = self.hasFocus()
        if not had_focus:
            self.setFocus()

        super().wheelEvent(event)

        if not had_focus:
            self.clearFocus()


class HotkeyLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.recording = False
        self.original_hotkey = ""
        self.pressed_keys = set()
        self.all_inputs = {}
        self.setPlaceholderText("Click to record hotkey")
        self.setReadOnly(True)


    def event(self, event):
        if self.recording and event.type() == event.KeyPress:
            key_event = event
            if key_event.key() == Qt.Key_Tab or key_event.key() == Qt.Key_Backtab:
                self.keyPressEvent(key_event)
                return True
        elif self.recording and event.type() == event.KeyRelease:
            key_event = event
            if key_event.key() == Qt.Key_Tab or key_event.key() == Qt.Key_Backtab:
                self.keyReleaseEvent(key_event)
                return True 
        
        return super().event(event)


    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.recording = True
        self.original_hotkey = self.text()
        self.setText("")
        self.pressed_keys.clear()
        self.setPlaceholderText("Press keys...")


    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.recording = False
        self.pressed_keys.clear()
        
        if not self.text().strip():
            self.setText(self.original_hotkey)
        
        self.setPlaceholderText("Click to record hotkey")


    def keyPressEvent(self, event):
        if not self.recording:
            super().keyPressEvent(event)
            return

        event.accept()

        if event.key() == Qt.Key_Escape:
            self.recording = False
            self.setText(self.original_hotkey)
            self.clearFocus()
            self.setPlaceholderText("Click to record hotkey")
            return

        key = event.key()

        key_map = {
            # F keys
            Qt.Key_F1: "f1", Qt.Key_F2: "f2", Qt.Key_F3: "f3", Qt.Key_F4: "f4",
            Qt.Key_F5: "f5", Qt.Key_F6: "f6", Qt.Key_F7: "f7", Qt.Key_F8: "f8",
            Qt.Key_F9: "f9", Qt.Key_F10: "f10", Qt.Key_F11: "f11", Qt.Key_F12: "f12",
            # Special keys
            Qt.Key_Tab: "tab",
            Qt.Key_Up: "up", Qt.Key_Down: "down", 
            Qt.Key_Left: "left", Qt.Key_Right: "right",
            Qt.Key_Space: "space",
            Qt.Key_Return: "enter",
            Qt.Key_Backspace: "backspace",
            Qt.Key_Delete: "delete",
            # Modifiers
            Qt.Key_Control: "ctrl",
            Qt.Key_Shift: "shift",
            Qt.Key_Alt: "alt"
        }

        if key in key_map:
            key_str = key_map[key]
        elif event.text() and event.text().isprintable():
            key_str = event.text().lower()
        else:
            return

        self.pressed_keys.add(key_str)
        
        self.update_hotkey_display()


    def keyReleaseEvent(self, event):
        if not self.recording:
            super().keyReleaseEvent(event)
            return

        event.accept()

        if self.pressed_keys:
            parts = []
            modifier_order = ["ctrl", "shift", "alt"]
            for mod in modifier_order:
                if mod in self.pressed_keys:
                    parts.append(mod)
            other_keys = sorted([k for k in self.pressed_keys if k not in modifier_order])
            parts.extend(other_keys)
            hotkey_str = "+".join(parts).lower()
            
            if self.is_duplicate(hotkey_str):
                self.setText(self.original_hotkey)
                self.setStyleSheet("QLineEdit { background-color: #ffcccc; }")
                QTimer.singleShot(500, lambda: self.setStyleSheet(""))
            else:
                self.setText(hotkey_str)
            
            self.recording = False
            self.clearFocus()


    def is_duplicate(self, hotkey_str):
        if not self.all_inputs:
            return False
        
        for input_field in self.all_inputs.values():
            if input_field is not self:
                if input_field.text().strip().lower() == hotkey_str:
                    return True
        return False


    def update_hotkey_display(self):
        parts = []
        
        modifier_order = ["ctrl", "shift", "alt"]
        
        for mod in modifier_order:
            if mod in self.pressed_keys:
                parts.append(mod)

        # Add non-modifier keys
        other_keys = sorted([k for k in self.pressed_keys if k not in modifier_order])
        parts.extend(other_keys)

        hotkey_str = "+".join(parts)
        self.setText(hotkey_str)
