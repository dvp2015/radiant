import pyrr


class Object3D:
    def __init__(self, position=(0, 0, 0)):
        self._position = pyrr.Vector3(position, dtype='f4')
        self._parent = None
        self._children = []
        self._model = None
        self.dirty = True

    def update(self):
        if self.dirty:
            self._model = pyrr.Matrix44.from_translation(self._position)
            if self._parent:
                self._parent.update()
                self._model = self._parent.model * self._model
            self.dirty = False

    @property
    def model(self):
        return self._model

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value
        self.dirty = True

    @property
    def children(self):
        return self._children

    @property
    def parent(self):
        return self._parent

    def append_child(self, child):
        if child.parent is not None:
            raise RuntimeError("Detach from parent first")
        # TODO: detect circular references?
        self._children.append(child)
        child._parent = self
        child.dirty = True

    def remove_child(self, child):
        if child.parent is not self:
            raise RuntimeError("Node is not a child of this object")
        self._children.remove(child)
        child._parent = None
        child.dirty = True


class Scene(Object3D):
    pass


class Mesh(Object3D):
    def __init__(self, geometry, material, **kwargs):
        super().__init__(**kwargs)
        self.geometry = geometry
        self.material = material
