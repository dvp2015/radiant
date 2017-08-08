import signal
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QGuiApplication, QOpenGLWindow, QSurfaceFormat

from radiant.renderers.moderngl import ModernGLRenderer


app = None  # this is scoped out so the garbage collector is forced to clear it last


class GLWindow(QOpenGLWindow):
    def __init__(self, scene, camera, light):
        super().__init__()
        fmt = QSurfaceFormat()
        fmt.setVersion(3, 3)
        fmt.setProfile(QSurfaceFormat.CoreProfile)
        fmt.setStencilBufferSize(8)
        self.setFormat(fmt)
        self.scene, self.camera, self.light = scene, camera, light

    def initializeGL(self):
        self.renderer = ModernGLRenderer()

    def resizeGL(self, width, height):
        self.renderer.viewport = (0, 0, width, height)

    def paintGL(self):
        self.renderer.render(self.scene, self.camera, self.light)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()        


def show_scene(scene, camera, light):
    signal.signal(signal.SIGINT, signal.SIG_DFL)  # support Ctrl+C to quit (without cleanup!)

    global app
    app = QGuiApplication(sys.argv)

    window = GLWindow(scene, camera, light)
    window.resize(640, 480)
    window.show()

    sys.exit(app.exec_())
