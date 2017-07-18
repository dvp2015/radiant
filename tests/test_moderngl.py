import os

import ModernGL
from PIL import Image
import pytest

import radiant
from radiant.renderers.moderngl import ModernGLRenderer


@pytest.mark.skipif(os.environ.get('TRAVIS') == 'true', reason="travis does not support opengl 3.3")
def test_basic_material():
    # create context
    ctx = ModernGL.create_standalone_context()

    # create renderer
    renderer = ModernGLRenderer(ctx)

    # create scene
    scene = radiant.Scene()

    cube_geom = radiant.CubeGeometry()
    red = radiant.MeshBasicMaterial(color=(1.0, 0.0, 0.0, 0.0))
    cube = radiant.Mesh(cube_geom, red)
    scene.append_child(cube)

    # create camera
    camera = radiant.PerspectiveCamera(position=[10, 10, 10], target=[0, 0, 0], up=[0, 1, 0])
    scene.append_child(camera)

    # create framebuffer and render into it
    fbo = ctx.framebuffer(ctx.renderbuffer((512, 512)))
    fbo.use()
    renderer.render(scene, camera)

    # read from the framebuffer and write to an image file
    data = fbo.read(components=3, alignment=1)
    img = Image.frombytes('RGB', fbo.size, data).transpose(Image.FLIP_TOP_BOTTOM)
    filename = "test_basic.png"
    with open(filename, mode="wb") as fh:
        img.save(fh)

    # complete the test
    assert os.path.exists(filename)


@pytest.mark.skipif(os.environ.get('TRAVIS') == 'true', reason="travis does not support opengl 3.3")
def test_phong():
    # create context
    ctx = ModernGL.create_standalone_context()

    # create renderer
    renderer = ModernGLRenderer(ctx)

    # create scene
    scene = radiant.Scene()

    plane_geom = radiant.PlaneGeometry(width=2, height=2)
    red = radiant.MeshPhongMaterial(color=(0.1, 0.5, 0.3, 1.0), shininess=16.0)
    plane = radiant.Mesh(plane_geom, red)
    scene.append_child(plane)

    # create a light
    light = radiant.Light(position=[-0.5, -0.5, 4])
    plane.append_child(light)  # follow the plane

    # create camera
    camera = radiant.PerspectiveCamera(position=[0.5, 0.5, 2], target=[0, 0, 0], up=[0, 1, 0])
    scene.append_child(camera)

    # create framebuffer and render into it
    fbo = ctx.framebuffer(ctx.renderbuffer((512, 512)))
    fbo.use()
    renderer.render(scene, camera, light=light)

    # read from the framebuffer and write to an image file
    data = fbo.read(components=3, alignment=1)
    img = Image.frombytes('RGB', fbo.size, data).transpose(Image.FLIP_TOP_BOTTOM)
    filename = "test_phong.png"
    with open(filename, mode="wb") as fh:
        img.save(fh)

    # complete the test
    assert os.path.exists(filename)
