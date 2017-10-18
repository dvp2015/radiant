from utils.pyqt5 import show_scene

import radiant
from radiant.renderers.moderngl import ModernGLRenderer


def generate_scene():
    scene = radiant.Scene()

    # put up a plane somewhere
    plane_geom = radiant.PlaneGeometry(width=2, height=2)
    red = radiant.MeshPhongMaterial(color=(0.1, 0.5, 0.3, 1.0), shininess=16.0)
    plane = radiant.Mesh(plane_geom, red)
    scene.append_child(plane)

    # create a light
    light = radiant.PointLight(position=[-0.5, -0.5, 4])
    plane.append_child(light)  # follow the plane

    # create a camera
    camera = radiant.PerspectiveCamera(position=[-.5, 0.5, -3], target=[0, 0, 0], up=[0, 1, 0])
    scene.append_child(camera)

    return scene, camera, light


if __name__ == "__main__":
    show_scene("basic scene", *generate_scene(), ModernGLRenderer)
