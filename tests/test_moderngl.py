import os

import ModernGL

from PIL import Image

import radiant
from radiant.renderers.moderngl import ModernGLRenderer


def test_moderngl_renderer():
    # create context
    ctx = ModernGL.create_standalone_context()
    
    # create renderer
    renderer = ModernGLRenderer(ctx)

    # create scene
    scene = radiant.Scene()

    cube_geom = radiant.CubeGeometry()
    red = radiant.MeshBasicMaterial(color=(1.0, 0.0, 0.0, 0.0))
    cube = radiant.Mesh(cube_geom, red)

    scene.children.append(cube)

    # create camera
    camera = radiant.PerspectiveCamera([10, 10, 10], [0, 0, 0], up=[0, 1, 0])

    # create framebuffer and render into it
    fbo = ctx.framebuffer(ctx.renderbuffer((512, 512)))
    fbo.use()
    renderer.render(scene, camera)

    # read from the framebuffer and write to an image file
    data = fbo.read(components=3, alignment=1)
    img = Image.frombytes('RGB', fbo.size, data).transpose(Image.FLIP_TOP_BOTTOM)
    filename = "screen.png"
    with open(filename, mode="wb") as fh:
        img.save(fh)

    # complete the test
    assert os.path.exists(filename)
