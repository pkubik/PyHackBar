#! python3

import datetime

from PySide2.QtCore import Qt, QPoint, QSize, QRect, QTimer
from PySide2.QtGui import QScreen
from PySide2.QtWidgets import QApplication, QLabel, QHBoxLayout, QFrame

from bspwm import State

BAR_HEIGHT = 32
AUX_COLOR = "orange"

STYLE_SHEET = """
* {
    color: #ffffff;
    font-size: 14px; 
    background-color: #222222;
}

Window {
    border-top: 3px solid orange;
}

"""


def size_to_point(size: QSize) -> QPoint:
    return QPoint(size.width(), size.height())


class Workspaces(QLabel):
    def __init__(self, screen_geo_id: str, *args, **kwargs):
        super().__init__("...desktops...", *args, **kwargs)

        self.screen_geo_id = screen_geo_id
        self.update_state(State())
        State.subscribe_in_new_thread(self.update_state)

    def update_state(self, state: State):
        monitor = state.monitor_by_geo_id(self.screen_geo_id)
        self.setText(" ".join(d.name if not d.focused else f'<span style="color: {AUX_COLOR};">{d.name}</span>'
                              for d in monitor.desktops()))


class Clock(QLabel):
    TIME_FORMAT = f'%Y-%m-%d <span style="color: {AUX_COLOR};">W%W</span> <b>%H:%M:%S</b>'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.update_time()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

    def update_time(self):
        self.setText(datetime.datetime.now().strftime(self.TIME_FORMAT))


class Window(QFrame):
    def __init__(self, screen: QScreen, parent=None):
        super().__init__(parent)

        self.screen = screen
        self.screen_geo_id = f'{screen.geometry().x()},{screen.geometry().y()}'
        self.setWindowFlags(Qt.BypassWindowManagerHint)
        self._build_interface()

    def _build_interface(self):
        self.setWindowTitle("PyHackBar")

        screen_rect: QRect = self.screen.geometry()
        self.resize(screen_rect.width(), BAR_HEIGHT + 1)
        self.move(screen_rect.left(), screen_rect.bottom() - BAR_HEIGHT)

        self.setStyleSheet(STYLE_SHEET)
        self.setProperty("windowOpacity", 0.7)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addSpacing(8)

        workspaces = Workspaces(self.screen_geo_id)
        layout.addWidget(workspaces)

        layout.addStretch(5)

        tray = QLabel("Δ", self)
        layout.addWidget(tray)

        layout.addSpacing(8)

        clock = Clock()
        layout.addWidget(clock)

        layout.addSpacing(8)

        self.show()


def main():
    import sys

    app = QApplication(sys.argv)

    for screen in app.screens():
        window = Window(screen)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
