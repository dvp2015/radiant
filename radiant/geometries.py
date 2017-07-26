from enum import Enum

import numpy as np

from pyrr.vector3 import generate_vertex_normals


__all__ = ('Primitives', 'Geometry', 'PlaneGeometry', 'CubeGeometry')


class Primitives(Enum):
    TRIANGLES = "TRIANGLES"
    LINES = "LINES"
    POINTS = "POINTS"


class Geometry:
    def __init__(self, attributes, index=None, primitive=Primitives.TRIANGLES):
        self.attributes = attributes
        self.index = index
        self.primitive = primitive


class PlaneGeometry(Geometry):
    def __init__(self, width=1, height=1, width_segments=1, height_segments=1):
        attributes = {}

        # vertices; construct cartesian linspace along sides
        vx, vy = np.linspace(-width/2, width/2, num=width_segments+1, dtype='f4'), np.linspace(-height/2, height/2, num=height_segments+1, dtype='f4')
        # preallocate memory
        n_vertices = (width_segments+1) * (height_segments+1)
        vertices = np.zeros((n_vertices, 3), dtype='f4')
        # assign combined linspaces to x, y coords
        vertices[:, :2] = np.asarray(np.meshgrid(vx, vy)).T.reshape((-1, 2))
        # assign result to attribute
        attributes["pos"] = vertices

        # texture coords; drop z coord & rescale to [0, 1] range
        attributes["uv"] = (vertices[:, :2] / [width, height]) + 0.5

        # get the lower left vertice index of each quad on the plane
        t = np.arange(n_vertices, dtype='i4').reshape((width_segments+1, height_segments+1))[:-1, :-1].ravel()
        # construct the index offset template for a triangle
        t_offset = np.array([
            [0, height_segments+1, 1],
            [height_segments+1, height_segments+2, 1],
        ], dtype='i4')
        # broadcast and reshape to get the final result
        index = (t[:, None, None] + t_offset).reshape((-1, 3))

        # generate normals
        attributes["normal"] = generate_vertex_normals(vertices, index)

        super().__init__(attributes, index=index)


class CubeGeometry(Geometry):
    def __init__(self):
        attributes = {}

        # 8 corners
        attributes["pos"] = np.array([
            [-1.0, -1.0,  1.0],
            [1.0, -1.0,  1.0],
            [-1.0,  1.0,  1.0],
            [1.0,  1.0,  1.0],
            [-1.0, -1.0, -1.0],
            [1.0, -1.0, -1.0],
            [-1.0,  1.0, -1.0],
            [1.0,  1.0, -1.0],
        ], dtype='f4') * 0.5

        # 6 sides, 2 triangles each
        index = np.array([
            [0, 6, 4],
            [0, 2, 6],
            [1, 5, 7],
            [1, 7, 3],
            [1, 0, 4],
            [1, 4, 5],
            [3, 7, 6],
            [3, 6, 2],
            [3, 0, 1],
            [3, 2, 0],
            [7, 5, 4],
            [7, 4, 6],
        ], dtype='i4')

        super().__init__(attributes, index=index)
