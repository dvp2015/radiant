import numpy as np

import pyrr

__all__ = ('generate_vertex_normals',)


def generate_vertex_normals(vertices, index):
    face_normals = pyrr.vector3.generate_normals(*np.rollaxis(vertices[index], axis=1))
    vertex_normals = np.zeros_like(vertices)
    for i in range(index.shape[-1]):
        np.add.at(vertex_normals, index[:, i], face_normals)
    return pyrr.vector3.normalize(vertex_normals)
