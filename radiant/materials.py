class Material:
    pass


class MeshBasicMaterial(Material):
    def __init__(self, color=(255, 255, 255)):
        self.color = color
