import os
from functools import lru_cache


@lru_cache(maxsize=None)
def load_shader_sources(key):
    """
    Load all built-in shaders from filesystem.

    Returns
    -------
    dict of dict
        Mapping of shader key to mapping of shader type to shader source.
    """
    shader_sources = {}
    shader_path = os.path.join(os.path.dirname(__file__), 'shaders')
    for filename in filter(lambda fn: fn.startswith(f"{key}."), os.listdir(shader_path)):
        _, ext = os.path.splitext(filename)
        with open(os.path.join(shader_path, filename)) as fh:
            shader_sources[ext[1:]] = fh.read()
    return shader_sources


class Material:
    def __init__(self, shaders=None):
        self.shaders = shaders or {}


class MeshBasicMaterial(Material):
    def __init__(self, color=(1.0, 0.0, 0.0, 1.0)):
        super().__init__(load_shader_sources('meshbasic'))
        self.color = color
