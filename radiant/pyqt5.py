from PyQt5.QtCore import QEvent, Qt, QTimer
from PyQt5.QtGui import QSurfaceFormat, QWheelEvent
from PyQt5.QtWidgets import QOpenGLWidget

from . import inputs


def handle_pyqt5_mouse(e):
    """Update radiant.inputs based on a PyQt5 mouse event."""
    type_map = {
        QEvent.MouseButtonPress: "Press",
        QEvent.MouseButtonRelease: "Release",
    }

    button_map = {
        Qt.LeftButton: "Left",
        Qt.RightButton: "Right",
        Qt.MiddleButton: "Middle",
    }

    inputs.mouse_position = (e.globalX(), e.globalY())

    if isinstance(e, QWheelEvent):
        inputs.mouse_wheel_delta[0] += e.angleDelta().x()
        inputs.mouse_wheel_delta[1] += e.angleDelta().y()
    else:
        mouse_button_type = type_map.get(e.type())
        mouse_button = button_map.get(e.button())

        if mouse_button_type == "Press":
            inputs.mouse_button_down[mouse_button] = True
            inputs.mouse_button_held[mouse_button] = True
            inputs.mouse_button_up[mouse_button] = False
        elif mouse_button_type == "Release":
            inputs.mouse_button_down[mouse_button] = False
            inputs.mouse_button_held[mouse_button] = False
            inputs.mouse_button_up[mouse_button] = True


def handle_pyqt5_key(e):
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

    key_type = type_map[e.type()]
    key = e.text()

    if not key:
        for modifier_key, qt_modifier in modifier_map.items():
            inputs.key_held[modifier_key] = e.modifiers() & qt_modifier
    else:
        if key_type == "Press":
            inputs.key_down[key] = True
            inputs.key_held[key] = True
            inputs.key_up[key] = False
        elif key_type == "Release":
            inputs.key_down[key] = False
            inputs.key_held[key] = False
            inputs.key_up[key] = True
        inputs.input_string += key


class RadiantWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFocusPolicy(Qt.StrongFocus)

        fmt = QSurfaceFormat()
        fmt.setVersion(3, 3)
        fmt.setProfile(QSurfaceFormat.CoreProfile)
        fmt.setStencilBufferSize(8)
        self.setFormat(fmt)

        self.setMouseTracking(True)

    def setScene(self, scene, camera, light):
        self._scene = scene
        self._camera = camera
        self._light = light

    def getScene(self):
        return self._scene, self._camera, self._light

    def setRendererType(self, renderer_type):
        self._renderer_type = renderer_type

    def getRendererType(self):
        return self._renderer_type

    def loop(self):
        # process input
        self._scene.update()
        inputs.tick()
        # schedule draw event
        self.update()
        # schedule next loop iteration
        QTimer.singleShot(0, self.loop)

    def initializeGL(self):
        self._renderer = self._renderer_type()
        # start game loop
        QTimer.singleShot(0, self.loop)

    def resizeGL(self, width, height):
        self._renderer.viewport = (0, 0, width, height)
        if hasattr(self._camera, 'aspect'):
            self._camera.aspect = width / height

    def paintGL(self):
        self._renderer.render(self._scene, self._camera, self._light)

    def keyPressEvent(self, e):
        handle_pyqt5_key(e)

    def keyReleaseEvent(self, e):
        handle_pyqt5_key(e)

    def mousePressEvent(self, e):
        handle_pyqt5_mouse(e)

    def mouseReleaseEvent(self, e):
        handle_pyqt5_mouse(e)

    def mouseMoveEvent(self, e):
        handle_pyqt5_mouse(e)

    def wheelEvent(self, e):
        handle_pyqt5_mouse(e)
