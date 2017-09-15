import signal
import sys

from PyQt5.QtCore import QEvent, Qt, QTimer
from PyQt5.QtGui import QCursor, QSurfaceFormat, QWheelEvent
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QOpenGLWidget, QWidget

from radiant.renderers.moderngl import ModernGLRenderer


app = None  # this is scoped out so the garbage collector is forced to clear it last


class Window(QWidget):
    def __init__(self, title, scene, camera, light):
        super().__init__()

        self.glWidget = GLWidget()
        self.glWidget.scene = scene
        self.glWidget.camera = camera
        self.glWidget.light = light

        self.setWindowTitle(f"PyQt5 + ModernGL: {title}")

        layout = QHBoxLayout()
        layout.addWidget(self.glWidget)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        QApplication.setOverrideCursor(QCursor(Qt.BlankCursor))


def mouse_event(e):
    """Map a PyQt5 mouse event to a radiant event."""
    type_map = {
        QEvent.MouseButtonPress: "Press",
        QEvent.MouseButtonRelease: "Release",
        QEvent.MouseButtonDblClick: "DblClick",
        QEvent.MouseMove: "Move",
    }

    button_map = {
        "Left": Qt.LeftButton,
        "Right": Qt.RightButton,
        "Middle": Qt.MiddleButton,
    }

    modifier_map = {
        "Shift": Qt.ShiftModifier,
        "Ctrl": Qt.ControlModifier,
        "Alt": Qt.AltModifier,
    }

    re = {
        'pos': (e.x(), e.y()),
        'buttons': [button for button, qt_button in button_map.items() if e.buttons() & qt_button],
        'modifiers': [key for key, qt_modifier in modifier_map.items() if e.modifiers() & qt_modifier],
    }

    if isinstance(e, QWheelEvent):
        re['type'] = "Wheel"
        re['delta'] = (e.angleDelta().x(), e.angleDelta().y())
    else:
        re['type'] = type_map[e.type()]

    return re


def key_event(e):
    """Map a PyQt5 key event to a radiant event."""
    type_map = {
        QEvent.KeyPress: "Press",
        QEvent.KeyRelease: "Release",
    }

    modifier_map = {
        "Shift": Qt.ShiftModifier,
        "Ctrl": Qt.ControlModifier,
        "Alt": Qt.AltModifier,
    }

    return {
        'type': type_map[e.type()],
        'key': e.text(),
        'modifiers': [key for key, qt_modifier in modifier_map.items() if e.modifiers() & qt_modifier],
    }


class GLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFocusPolicy(Qt.StrongFocus)

        fmt = QSurfaceFormat()
        fmt.setVersion(3, 3)
        fmt.setProfile(QSurfaceFormat.CoreProfile)
        fmt.setStencilBufferSize(8)
        self.setFormat(fmt)

        self.setMouseTracking(True)

        self.render_loop = QTimer()
        self.render_loop.timeout.connect(self.update)
        self.render_loop.start(1000/30)  # 30 FPS!

    def initializeGL(self):
        self.renderer = ModernGLRenderer()

    def resizeGL(self, width, height):
        self.renderer.viewport = (0, 0, width, height)

    def paintGL(self):
        print("rendering")
        self.renderer.render(self.scene, self.camera, self.light)

    def keyPressEvent(self, e):
        print(key_event(e))

    def keyReleaseEvent(self, e):
        print(key_event(e))

    def mousePressEvent(self, e):
        print(mouse_event(e))

    def mouseReleaseEvent(self, e):
        print(mouse_event(e))

    def mouseMoveEvent(self, e):
        print(mouse_event(e))

    def wheelEvent(self, e):
        print(mouse_event(e))


def show_scene(title, scene, camera, light):
    signal.signal(signal.SIGINT, signal.SIG_DFL)  # support Ctrl+C to quit (without cleanup!)

    global app
    app = QApplication(sys.argv)

    window = Window(title, scene, camera, light)
    window.resize(640, 480)
    window.show()

    sys.exit(app.exec_())
