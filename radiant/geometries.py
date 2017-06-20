class Geometry:
    pass

class BufferGeometry(Geometry):
    def __init__(self):
        self.attributes = dict()
        self.indices = None
