import os

import ModernGL

from PIL import Image

import radiant
from radiant.renderers.moderngl import ModernGLRenderer


def test_render():
    ctx = ModernGL.create_standalone_context()
    fbo = ctx.framebuffer(ctx.renderbuffer((512, 512)))

    renderer = ModernGLRenderer(ctx)

    scene = radiant.Scene()

    cube_geom = radiant.CubeGeometry()
    red = radiant.MeshBasicMaterial(color=(1.0, 0.0, 0.0, 0.0))
    cube = radiant.Mesh(cube_geom, red)

    scene.children.append(cube)

    camera = radiant.PerspectiveCamera([10, 10, 10], [0, 0, 0], up=[0, 1, 0])

    fbo.use()
    renderer.render(scene, camera)

    data = fbo.read(components=3, alignment=1)
    img = Image.frombytes('RGB', fbo.size, data).transpose(Image.FLIP_TOP_BOTTOM)
    filename = "screen.png"
    with open(filename, mode="wb") as fh:
        img.save(fh)

    assert os.path.exists(filename)
