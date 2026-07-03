import resources_rc
import pyautogui
import sys
from PySide6.QtCore import QSize, Qt, QPoint
from PySide6.QtGui import QIntValidator, QIcon
from PySide6.QtWidgets import (
    QMainWindow,
    QLabel,
    QWidget,
    QApplication,
    QPushButton,
    QGridLayout,
    QLineEdit,
)
import keyboard

from modules.click_util import ClickWatcher


class AutoClicker(QMainWindow):

    def __init__(self) -> None:
        super().__init__()

        self.init_window()
        self.init_coordinates_widget()
        self.init_clicker_widget()
        self.place_widgets()

    def init_window(self):
        self.setWindowTitle("Auto Clicker")
        self.setWindowIcon(QIcon(":/app_icon.ico"))
        self.setFixedSize(QSize(self.baseSize()))

    def init_coordinates_widget(self):
        layout = QGridLayout()
        container = QWidget()
        container.setLayout(layout)
        self.coordinates_widget = container

        watcher = ClickWatcher()

        self.click_position = QPoint()

        def on_click():
            watcher.wait_for_click()

            x_value_box.setText(str(watcher.x))
            y_value_box.setText(str(watcher.y))

        widget_label = QLabel("Click Position")
        a = widget_label.font()
        a.setUnderline(True)
        a.setBold(True)
        widget_label.setFont(a)

        x_label = QLabel("x:")
        y_label = QLabel("y:")

        validator = QIntValidator(-9999, 9999)

        x_value_box = QLineEdit()
        x_value_box.setText(str(watcher.x))
        x_value_box.setFixedWidth(45)
        x_value_box.setMaxLength(5)
        x_value_box.setValidator(validator)
        x_value_box.textChanged.connect(
            lambda: self.click_position.setX(int(x_value_box.text()))
        )

        y_value_box = QLineEdit()
        y_value_box.setText(str(watcher.y))
        y_value_box.setFixedWidth(45)
        y_value_box.setMaxLength(5)
        y_value_box.setValidator(validator)
        y_value_box.textChanged.connect(
            lambda: self.click_position.setY(int(y_value_box.text()))
        )

        button = QPushButton("Set Position")
        button.clicked.connect(on_click)

        layout.addWidget(widget_label, 0, 0, 1, 4, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(x_label, 1, 0)
        layout.addWidget(x_value_box, 1, 1)
        layout.addWidget(y_label, 1, 2)
        layout.addWidget(y_value_box, 1, 3)
        layout.addWidget(button, 2, 0, 1, 4)

    def init_clicker_widget(self):
        layout = QGridLayout()
        container = QWidget()
        container.setLayout(layout)
        self.clicker_widget = container

        self.click_amount = 10

        def on_click():

            for _ in range(self.click_amount):

                if keyboard.is_pressed("esc"):
                    return

                pyautogui.click(self.click_position.x(), self.click_position.y())

        def set_click_speed(speed: int):

            pyautogui.PAUSE = 1 / speed

        def set_click_amount():
            self.click_amount = int(click_amount_box.text())

        click_speed_label = QLabel("CPS")

        validator = QIntValidator(0, 9999)

        speed_value_box = QLineEdit()
        speed_value_box.setText("10")
        speed_value_box.setFixedWidth(37)
        speed_value_box.setMaxLength(4)
        speed_value_box.setValidator(validator)
        speed_value_box.textChanged.connect(
            lambda: set_click_speed(int(speed_value_box.text()))
        )

        click_button = QPushButton("Click")
        click_button.clicked.connect(on_click)

        click_ammount_label = QLabel("Clicks")

        click_amount_box = QLineEdit()
        click_amount_box.setText(str(self.click_amount))
        click_amount_box.setFixedWidth(37)
        click_amount_box.setMaxLength(4)
        click_amount_box.setValidator(validator)
        click_amount_box.textChanged.connect(set_click_amount)

        layout.addWidget(click_amount_box, 0, 0)
        layout.addWidget(click_ammount_label, 0, 1)
        layout.addWidget(speed_value_box, 1, 0)
        layout.addWidget(click_speed_label, 1, 1)
        layout.addWidget(click_button, 2, 0, 1, 2)

    def place_widgets(self):

        layout = QGridLayout()
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        layout.addWidget(self.coordinates_widget, 0, 0)
        layout.addWidget(self.clicker_widget, 0, 1)


def main():
    app = QApplication(sys.argv)

    window = AutoClicker()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
