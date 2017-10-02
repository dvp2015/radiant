import collections

import numpy as np
import pyrr

from .maths import decompose


class Object3D:
    def __init__(self, position=(0, 0, 0), scale=(1, 1, 1), rotation=(0, 0, 0)):
        self._parent = None
        self._children = tuple()
        self._model = None
        self.dirty = True
        self.position = position
        self.scale = scale
        self.rotation = rotation

    def update(self):
        if self.dirty:
            scale = pyrr.Matrix44.from_scale(self._scale, dtype='f4')
            translate = pyrr.Matrix44.from_translation(self._position, dtype='f4')
            # Scale -> Rotate -> Translate
            self._model = translate * self._rotation.matrix44.astype('f4') * scale
            if self._parent:
                self._parent.update()
                self._model = self._parent.model * self._model
            self._model.flags.writeable = False
            self.dirty = False

    def mark_as_dirty(self):
        self.dirty = True
        for child in self._children:
            child.mark_as_dirty()

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        self.scale, self.rotation, self.position = decompose(value)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = pyrr.Vector3(value, dtype='f4')
        self._position.flags.writeable = False
        self.mark_as_dirty()

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = pyrr.Vector3(value, dtype='f4')
        self._scale.flags.writeable = False
        self.mark_as_dirty()

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, value):
        value = np.asanyarray(value, dtype='f4')
        if isinstance(value, pyrr.Quaternion):
            self._rotation = value.astype('f4')
        elif isinstance(value, (np.ndarray, collections.Iterable)):
            value = np.asanyarray(value, dtype='f4')
            if value.shape in ((3, 3), (4, 4)):
                self._rotation = pyrr.Quaternion.from_matrix(value, dtype='f4')
            elif value.shape == (3,):
                self._rotation = pyrr.Quaternion.from_eulers(pyrr.euler.create(*value, dtype='f4'))
            elif value.shape == (4,):
                self._rotation = pyrr.Quaternion(value, dtype='f4')
            else:
                raise ValueError(f"unexpected shape {value.shape} for rotation")
        else:
            raise ValueError(f"unexpected type {type(value)} for rotation")
        self._rotation.flags.writeable = False
        self.mark_as_dirty()

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
        self._children = self._children + tuple([child])
        child._parent = self
        child.mark_as_dirty()

    def remove_child(self, child):
        if child.parent is not self:
            raise RuntimeError("Node is not a child of this object")
        children = list(self._children)
        children.remove(child)
        self._children = tuple(children)
        child._parent = None
        child.mark_as_dirty()


class Scene(Object3D):
    pass


class Mesh(Object3D):
    def __init__(self, geometry, material, **kwargs):
        super().__init__(**kwargs)
        self.geometry = geometry
        self.material = material
