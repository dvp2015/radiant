import numpy as np


class Geometry:
    pass


class BufferGeometry(Geometry):
    def __init__(self):
        self.attributes = dict()
        self.indices = None


class CubeGeometry(BufferGeometry):
    def __init__(self):
        super().__init__()

        # 8 corners
        self.attributes["position"] = np.array([
            [-1.0, -1.0,  1.0],
            [1.0, -1.0,  1.0],
            [-1.0,  1.0,  1.0],
            [1.0,  1.0,  1.0],
            [-1.0, -1.0, -1.0],
            [1.0, -1.0, -1.0],
            [-1.0,  1.0, -1.0],
            [1.0,  1.0, -1.0],
        ], dtype='f4').tobytes()

        # 6 sides, 2 triangles each
        self.indices = np.array([
            0, 6, 4,
            0, 2, 6,
            1, 5, 7,
            1, 7, 3,
            1, 0, 4,
            1, 4, 5,
            3, 7, 6,
            3, 6, 2,
            3, 0, 1,
            3, 2, 0,
            7, 5, 4,
            7, 4, 6,
        ], dtype='i4').tobytes()
