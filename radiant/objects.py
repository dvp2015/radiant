class Object3D:
    def __init__(self):
        self.world = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]

class Mesh(Object3D):
    def __init__(self, geometry, material):
        super().__init__()
        self.geometry = geometry
        self.material = material
