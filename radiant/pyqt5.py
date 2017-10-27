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


def handle_pyqt5_mouse(e):
    """Update radiant.inputs based on a PyQt5 mouse event."""
    inputs.event_occurred = True
    inputs.mouse_position = (e.globalX(), e.globalY())
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
    inputs.event_occurred = True
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

        self.setMouseTracking(True)

        self._animated = False

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

    def loop(self):
        # (1) if the scene is animated, we actively keep running behaviours and redrawing
        # (2) otherwise, we wait for inputs to occur
        # (3) alternatively, users can schedule a redraw manually by calling .update()
        if self._animated or inputs.event_occurred:
            # process input
            self._scene.update()
            inputs.tick()
            # schedule draw event
            self.update()
        # schedule next loop iteration
        QTimer.singleShot(0, self.loop)

    def initializeGL(self):
        self._renderer.init_gl()
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
