import sys
import pyautogui
from PySide6.QtGui import QIntValidator
from PySide6.QtCore import QSize, QPoint, Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QLabel,
    QWidget,
    QApplication,
    QPushButton,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
)

from click_util import ClickWatcher


class LineWidget(QWidget):

    def __init__(self, line_number: int) -> None:
        super().__init__()

        self._line_number: int = line_number

        self.setMaximumHeight(40)

        self._init_widgets()
        self._init_debug_widget()
        self._place_widgets()

    @property
    def line_number(self):
        return self._line_number

    @line_number.setter
    def line_number(self, line_number):
        self._line_number = line_number
        self.line_number_label.setText(f"{self._line_number}")

    def do_action(self):
        """Clicks screen based on the set coordinates"""
        pyautogui.click(self.click_position.x(), self.click_position.y())

    def _init_widgets(self):

        watcher = ClickWatcher()
        self.click_position = QPoint()
        self.click_position.setX(0)
        self.click_position.setY(0)

        self.line_number_label = QLabel(f"{self._line_number} ")
        self.action_label = QLabel(
            f" CLICK AT x:{self.click_position.x():04}, y:{self.click_position.y():04}"
        )

        def get_coords():
            watcher.wait_for_click()

            self.click_position.setX(watcher.x)
            self.click_position.setY(watcher.y)

            self.action_label.setText(f" CLICK AT x:{watcher.x:04}, y:{watcher.y:04}")

        self.get_coordinates_button = QPushButton("Set Coords")
        self.get_coordinates_button.clicked.connect(get_coords)

    def _init_debug_widget(self):

        self._debug_button = QPushButton("debug")
        self._debug_button.setMaximumWidth(50)
        self._debug_button.clicked.connect(self.do_action)

    def _place_widgets(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

        layout.addWidget(self.line_number_label)
        layout.addWidget(self.get_coordinates_button)
        layout.addWidget(self.action_label)

        layout.addWidget(self._debug_button)


class testingWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.init_widgets()

    def init_widgets(self):
        layout = QVBoxLayout()
        layout.setSpacing(0)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        for i in range(1, 8):
            w = LineWidget(i)
            layout.addWidget(w)


def main():
    app = QApplication(sys.argv)

    window = testingWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
