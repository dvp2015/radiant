import sys

from PyQt5.QtWidgets import QApplication, QHBoxLayout, QWidget

from radiant.pyqt5 import RadiantWidget


app = None  # this is the only variable scoped globally so the garbage collector is forced to clear it last


class Window(QWidget):
    def __init__(self, title, scene, camera, light, renderer_type):
        super().__init__()

        self.glWidget = RadiantWidget()
        self.glWidget.setRendererType(renderer_type)
        self.glWidget.setScene(scene, camera, light)

        self.setWindowTitle(title)

        layout = QHBoxLayout()
        layout.addWidget(self.glWidget)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)


def show_scene(title, scene, camera, light, renderer_type):
    global app
    app = QApplication(sys.argv)

    window = Window(title, scene, camera, light, renderer_type)
    window.resize(640, 480)
    window.show()

    sys.exit(app.exec_())
