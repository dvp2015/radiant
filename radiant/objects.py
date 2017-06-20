class Object3D:
    pass

class Mesh(Object3D):
    def __init__(self, geometry, material):
        self.geometry = geometry
        self.material = material
