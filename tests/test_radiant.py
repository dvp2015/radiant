import radiant
import ModernGL


def test_render():
    ctx = ModernGL.create_standalone_context()
    renderer = radiant.ModernGLRenderer(ctx)
    scene = radiant.Scene()

