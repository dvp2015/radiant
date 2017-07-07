import pyrr


class Object3D:
    def __init__(self):
        self.model = pyrr.Matrix44.identity(dtype='f4')
        self.children = []


class Scene(Object3D):
    pass


class Mesh(Object3D):
    def __init__(self, geometry, material):
        super().__init__()
        self.geometry = geometry
        self.material = material
