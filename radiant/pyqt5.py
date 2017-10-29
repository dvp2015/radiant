from PyQt5.QtCore import QEvent, Qt, QTimer
from PyQt5.QtGui import QSurfaceFormat, QWheelEvent
from PyQt5.QtWidgets import QOpenGLWidget

from . import inputs


# lookup tables to convert Qt events to native Python objects
mouse_type_map = {
    QEvent.MouseButtonPress: "Press",
    QEvent.MouseButtonRelease: "Release",
}
mouse_button_map = {
    Qt.LeftButton: "Left",
    Qt.RightButton: "Right",
    Qt.MiddleButton: "Middle",
}
key_type_map = {
    QEvent.KeyPress: "Press",
    QEvent.KeyRelease: "Release",
}
modifier_map = {
    "Shift": Qt.ShiftModifier,
    "Ctrl": Qt.ControlModifier,
    "Alt": Qt.AltModifier,
}


def handle_pyqt5_mouse(e, widget):
    """Update radiant.inputs based on a PyQt5 mouse event."""
    inputs.mouse_position_global = (e.globalX(), e.globalY())
    inputs.mouse_position = (
        e.x() / widget.width() * 2 - 1,
        -(e.y() / widget.height() * 2 - 1),
    )
    if isinstance(e, QWheelEvent):
        inputs.mouse_wheel_delta[0] += e.angleDelta().x()
        inputs.mouse_wheel_delta[1] += e.angleDelta().y()
    else:
        mouse_button_type = mouse_type_map.get(e.type())
        mouse_button = mouse_button_map.get(e.button())
        if mouse_button_type == "Press":
            inputs.mouse_button_down[mouse_button] = True
            inputs.mouse_button_held[mouse_button] = True
            inputs.mouse_button_up[mouse_button] = False
        elif mouse_button_type == "Release":
            inputs.mouse_button_down[mouse_button] = False
            inputs.mouse_button_held[mouse_button] = False
            inputs.mouse_button_up[mouse_button] = True


def handle_pyqt5_key(e):
    """Update radiant.inputs based on a PyQt5 key event."""
    key = e.text()
    if not key:
        for modifier_key, qt_modifier in modifier_map.items():
            inputs.key_held[modifier_key] = e.modifiers() & qt_modifier
    else:
        key_type = key_type_map[e.type()]
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

        # self.setMouseTracking(True) users need to determine if this is what they want or not

        self._animated = False
        self._process_input_requested = False

    def setScene(self, scene, camera, light):
        self._scene = scene
        self._camera = camera
        self._light = light

    def getScene(self):
        return self._scene, self._camera, self._light

    def setRenderer(self, renderer):
        self._renderer = renderer

    def getRenderer(self):
        return self._renderer

    def setAnimated(self, animated):
        """
        Setting animated to True will configure this widget to continuously run behaviours and redraw,
        independent of user input occurring or not. Default is False.
        """
        self._animated = animated

    def initializeGL(self):
        self._renderer.init_gl()

    def resizeGL(self, width, height):
        self._renderer.viewport = (0, 0, width, height)
        if hasattr(self._camera, 'aspect'):
            self._camera.aspect = width / height

    def paintGL(self):
        self._renderer.render(self._scene, self._camera, self._light)
        self.animation_loop()

    def animation_loop(self):
        if self._animated:
            self.request_process_input()
            self.update()
            QTimer.singleShot(0, self.animation_loop)

    def process_input(self):
        self._scene.update()
        inputs.tick()
        self._process_input_requested = False

    def request_process_input(self):
        if not self._process_input_requested:
            QTimer.singleShot(0, self.process_input)
            self._process_input_requested = True

    def keyPressEvent(self, e):
        handle_pyqt5_key(e, self)
        self.request_process_input()

    def keyReleaseEvent(self, e):
        handle_pyqt5_key(e, self)
        self.request_process_input()

    def mousePressEvent(self, e):
        handle_pyqt5_mouse(e, self)
        self.request_process_input()

    def mouseReleaseEvent(self, e):
        handle_pyqt5_mouse(e, self)
        self.request_process_input()

    def mouseMoveEvent(self, e):
        handle_pyqt5_mouse(e, self)
        self.request_process_input()

    def wheelEvent(self, e):
        handle_pyqt5_mouse(e, self)
        self.request_process_input()
