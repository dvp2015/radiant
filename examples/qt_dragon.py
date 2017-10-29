import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
import radiant
from radiant.pyqt5 import RadiantWidget
from radiant.moderngl import ModernGLRenderer


app = None  # this is the only variable scoped globally so the garbage collector is forced to clear it last


class PanZoomCameraBehaviour:
    def __init__(self, gl_widget):
        self.gl_widget = gl_widget
        self.last_mouse = None

    def update(self, object3d):
        if radiant.inputs.mouse_button_down["Middle"]:
            self.last_mouse = (
                radiant.inputs.mouse_position[0],
                radiant.inputs.mouse_position[1])
        elif radiant.inputs.mouse_button_held["Middle"]:
            delta = (
                self.last_mouse[0] - radiant.inputs.mouse_position[0],
                -(self.last_mouse[1] - radiant.inputs.mouse_position[1]))
            radiant.pan_camera(object3d, *delta, sensitivity=0.005)
            self.last_mouse = (
                radiant.inputs.mouse_position[0],
                radiant.inputs.mouse_position[1])
            self.gl_widget.update()


if __name__ == "__main__":
    # scene setup
    scene = radiant.Scene()

    # load a cool mesh
    with open("examples/resources/dragon.obj", mode="r") as fh:
        dragon_geometry = radiant.load_obj(fh)

    # put up a mesh somewhere
    red = radiant.MeshPhongMaterial(color=(0.1, 0.5, 0.3, 1.0), shininess=16.0)
    dragon = radiant.Mesh(dragon_geometry, red)
    scene.append_child(dragon)

    # create a camera
    camera = radiant.PerspectiveCamera(position=[-5, 2, -5], target=[0, 0, 0], near=0.1, far=15.0)
    scene.append_child(camera)

    # create a light
    light = radiant.PointLight()
    camera.append_child(light)  # light follows the camera as a "headlight"

    # Qt app
    app = QApplication(sys.argv)

    # renderer
    renderer = ModernGLRenderer()

    # create Qt Radiant widget
    gl_widget = RadiantWidget()
    gl_widget.setRenderer(renderer)
    gl_widget.setScene(scene, camera, light)

    # now we can set up interaction on our scene, with the widget reference in hand
    camera.behaviours.append(PanZoomCameraBehaviour(gl_widget))

    # show & run
    window = QMainWindow()
    window.resize(640, 480)
    window.setWindowTitle(__file__)
    window.setCentralWidget(gl_widget)
    window.show()
    sys.exit(app.exec_())
