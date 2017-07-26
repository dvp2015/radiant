import signal
import sys

import ModernGL
from PyQt5.QtGui import QGuiApplication, QOpenGLWindow, QSurfaceFormat

from radiant.renderers.moderngl import ModernGLRenderer


class GLWindow(QOpenGLWindow):
    def __init__(self, scene, camera, light):
        super().__init__()
        fmt = QSurfaceFormat()
        fmt.setVersion(3, 3)
        fmt.setProfile(QSurfaceFormat.CoreProfile)
        self.setFormat(fmt)
        self.scene, self.camera, self.light = scene, camera, light

    def initializeGL(self):
        self.ctx = ModernGL.create_context()
        self.renderer = ModernGLRenderer(self.ctx)

    def resizeGL(self, width, height):
        self.ctx.viewport = (0, 0, width, height)

    def paintGL(self):
        self.renderer.render(self.scene, self.camera, self.light)


def show_scene(scene, camera, light):
    signal.signal(signal.SIGINT, signal.SIG_DFL)  # support Ctrl+C to quit (without cleanup!)

    app = QGuiApplication(sys.argv)

    window = GLWindow(scene, camera, light)
    window.resize(640, 480)
    window.show()

    sys.exit(app.exec_())
