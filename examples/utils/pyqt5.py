import sys

from PyQt5.QtWidgets import QApplication, QHBoxLayout, QWidget

from radiant.pyqt5 import RadiantWidget


app = None  # this is the only variable scoped globally so the garbage collector is forced to clear it last


class Window(QWidget):
    def __init__(self, title, scene, camera, light, renderer):
        super().__init__()

        self.glWidget = RadiantWidget()
        self.glWidget.setRenderer(renderer)
        self.glWidget.setScene(scene, camera, light)

        self.setWindowTitle(title)

        layout = QHBoxLayout()
        layout.addWidget(self.glWidget)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)


def show_scene(title, scene, camera, light, renderer):
    global app
    app = QApplication(sys.argv)

    window = Window(title, scene, camera, light, renderer)
    window.resize(640, 480)
    window.show()

    sys.exit(app.exec_())
