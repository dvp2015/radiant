import sys

from PyQt5.QtCore import QEvent, Qt, QTimer
from PyQt5.QtGui import QSurfaceFormat, QWheelEvent
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QOpenGLWidget, QWidget

import radiant


app = None  # this is the only variable scoped globally so the garbage collector is forced to clear it last


class Window(QWidget):
    def __init__(self, title, scene, camera, light, renderer_type):
        super().__init__()

        self.glWidget = GLWidget()
        self.glWidget.setRendererType(renderer_type)
        self.glWidget.setScene(scene, camera, light)

        self.setWindowTitle(title)

        layout = QHBoxLayout()
        layout.addWidget(self.glWidget)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)


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

    radiant.inputs.mouse_position = (e.globalX(), e.globalY())

    if isinstance(e, QWheelEvent):
        radiant.inputs.mouse_wheel_delta[0] += e.angleDelta().x()
        radiant.inputs.mouse_wheel_delta[1] += e.angleDelta().y()
    else:
        mouse_button_type = type_map.get(e.type())
        mouse_button = button_map.get(e.button())

        if mouse_button_type == "Press":
            radiant.inputs.mouse_button_down[mouse_button] = True
            radiant.inputs.mouse_button_held[mouse_button] = True
            radiant.inputs.mouse_button_up[mouse_button] = False
        elif mouse_button_type == "Release":
            radiant.inputs.mouse_button_down[mouse_button] = False
            radiant.inputs.mouse_button_held[mouse_button] = False
            radiant.inputs.mouse_button_up[mouse_button] = True


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
            radiant.inputs.key_held[modifier_key] = e.modifiers() & qt_modifier
    else:
        if key_type == "Press":
            radiant.inputs.key_down[key] = True
            radiant.inputs.key_held[key] = True
            radiant.inputs.key_up[key] = False
        elif key_type == "Release":
            radiant.inputs.key_down[key] = False
            radiant.inputs.key_held[key] = False
            radiant.inputs.key_up[key] = True
        radiant.inputs.input_string += key


# class PanZoomControls:
#     def __init__(self, gl_widget, camera, mouse_sensitivity=0.005):
#         self.gl_widget = gl_widget
#         self.camera = camera
#         self.panning = False
#         self.mouse_sensitivity = mouse_sensitivity

#     def mouse_event(self, e):
#         e = pyqt_to_radiant_mouse(e)
#         if e["type"] == "Press" and e['button'] == "Middle":
#             self.panning = True
#             self.hide_mouse()
#             self.set_mouse_pos(*self.get_widget_center())
#         elif e["type"] == "Release" and e['button'] == "Middle":
#             self.panning = False
#             self.show_mouse()
#         elif e["type"] == "Move" and self.panning:
#             center = self.get_widget_center()
#             if e['pos'] == center:
#                 return  # ignore events programmatically triggered by centering the mouse

#             dx = (e['pos'][0] - center[0]) * self.mouse_sensitivity
#             dy = (e['pos'][1] - center[1]) * self.mouse_sensitivity
#             radiant.pan_camera(self.camera, -dx, dy)

#             self.set_mouse_pos(*center)

#     def hide_mouse(self):
#         QApplication.setOverrideCursor(QCursor(Qt.BlankCursor))

#     def show_mouse(self):
#         QApplication.setOverrideCursor(QCursor(Qt.ArrowCursor))

#     def set_mouse_pos(self, x, y):
#         QCursor().setPos(x, y)

#     def get_widget_center(self):
#         screen_topleft = self.gl_widget.mapToGlobal(self.gl_widget.pos())
#         size = self.gl_widget.size()
#         return screen_topleft.x() + size.width() / 2, screen_topleft.y() + size.height() / 2

#     def key_event(self, e):
#         e = pyqt_to_radiant_key(e)
#         print(e)


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
        radiant.inputs.reset()
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


def show_scene(title, scene, camera, light, renderer_type):
    global app
    app = QApplication(sys.argv)

    window = Window(title, scene, camera, light, renderer_type)
    window.resize(640, 480)
    window.show()

    sys.exit(app.exec_())
