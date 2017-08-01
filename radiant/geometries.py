from enum import Enum

import numpy as np

from pyrr.vector3 import generate_vertex_normals


__all__ = ('Primitives', 'WindingOrders', 'Geometry', 'PlaneGeometry')


class Primitives(Enum):
    TRIANGLES = "TRIANGLES"
    TRIANGLE_STRIP = "TRIANGLE_STRIP"
    TRIANGLE_FAN = "TRIANGLE_FAN"
    LINES = "LINES"
    LINE_STRIP = "LINE_STRIP"
    LINE_LOOP = "LINE_LOOP"
    POINTS = "POINTS"
    LINE_STRIP_ADJACENCY = "LINE_STRIP_ADJACENCY"
    LINES_ADJACENCY = "LINES_ADJACENCY"
    TRIANGLE_STRIP_ADJACENCY = "TRIANGLE_STRIP_ADJACENCY"
    TRIANGLES_ADJACENCY = "TRIANGLES_ADJACENCY"


class WindingOrders(Enum):
    CCW = 'CCW'
    CW = 'CW'


class Geometry:
    def __init__(self, attributes, index=None, primitive=Primitives.TRIANGLES, winding_order=WindingOrders.CCW):
        self.attributes = attributes
        self.index = index
        self.primitive = primitive
        self.winding_order = winding_order


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
