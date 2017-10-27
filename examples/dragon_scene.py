from utils.pyqt5 import show_scene

import radiant
from radiant.moderngl import ModernGLRenderer


# class PanZoomCameraBehaviour:
#     def __init__(self):
#         self.last_mouse = (0, 0)

#     def update(self, object3d):
#         if radiant.inputs.mouse_button_held["Middle"]:
#             x = radiant.inputs.mouse_position[0]

#             radiant.pan_camera(object3d, x, y)


def generate_scene():
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
    #camera.behaviours.append(PanZoomCameraBehaviour())

    # create a light
    light = radiant.PointLight()
    camera.append_child(light)  # follow the camera

    return scene, camera, light


if __name__ == "__main__":
    renderer = ModernGLRenderer()
    show_scene("dragon scene", *generate_scene(), renderer)
