import signal
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QSurfaceFormat, QCursor
from PyQt5.QtWidgets import QApplication, QWidget, QOpenGLWidget, QHBoxLayout

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


class GLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        fmt = QSurfaceFormat()
        fmt.setVersion(3, 3)
        fmt.setProfile(QSurfaceFormat.CoreProfile)
        fmt.setStencilBufferSize(8)
        self.setFormat(fmt)

        self.setMouseTracking(True)

    def initializeGL(self):
        self.renderer = ModernGLRenderer()

    def resizeGL(self, width, height):
        self.renderer.viewport = (0, 0, width, height)

    def paintGL(self):
        self.renderer.render(self.scene, self.camera, self.light)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    def mouseMoveEvent(self, e):
        pass

    def leaveEvent(self, e):
        size = self.geometry()
        pos = QCursor.pos()
        pass


def show_scene(title, scene, camera, light):
    signal.signal(signal.SIGINT, signal.SIG_DFL)  # support Ctrl+C to quit (without cleanup!)

    global app
    app = QApplication(sys.argv)

    window = Window(title, scene, camera, light)
    window.resize(640, 480)
    window.show()

    sys.exit(app.exec_())
