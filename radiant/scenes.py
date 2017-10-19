import collections

import numpy as np
import pyrr

from .maths import decompose


class Object3D:
    def __init__(self, position=(0, 0, 0), scale=(1, 1, 1), rotation=(0, 0, 0)):
        self._parent = None
        self._children = tuple()
        self._transform = None
        self._model = None
        self._model_dirty = True
        self.position = position
        self.scale = scale
        self.rotation = rotation
        self.behaviours = []

    def model_dirty(self):
        self._model_dirty = True
        for child in self._children:
            child.model_dirty()

    @property
    def model(self):
        """Transforms to world coordinate space."""
        if self._model_dirty:
            scale = pyrr.Matrix44.from_scale(self._scale, dtype='f4')
            translate = pyrr.Matrix44.from_translation(self._position, dtype='f4')
            # Scale -> Rotate -> Translate
            self._transform = translate * self._rotation.matrix44.astype('f4') * scale
            self._transform.flags.writeable = False
            if self._parent:
                self._model = self._parent.model * self._transform
                self._model.flags.writeable = False
            self._model_dirty = False
        return self._model

    @property
    def transform(self):
        """Transforms to local coordinate space."""
        if self._model_dirty:
            _ = self.model  # noqa: recomputing the transform happens as part of recomputing the model matrix
        return self._transform

    @transform.setter
    def transform(self, value):
        self.scale, self.rotation, self.position = decompose(value)

    @property
    def position(self):
        return self._position

    @property
    def position_world(self):
        return pyrr.Vector3(np.asarray(self.model)[3, :3])

    @position.setter
    def position(self, value):
        self._position = pyrr.Vector3(value, dtype='f4')
        self._position.flags.writeable = False
        self.model_dirty()

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = pyrr.Vector3(value, dtype='f4')
        self._scale.flags.writeable = False
        self.model_dirty()

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
        self.model_dirty()

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
        child.model_dirty()

    def remove_child(self, child):
        if child.parent is not self:
            raise RuntimeError("Node is not a child of this object")
        children = list(self._children)
        children.remove(child)
        self._children = tuple(children)
        child._parent = None
        child.model_dirty()

    def update(self):
        for behaviour in self.behaviours:
            behaviour.update(self)
        for child in self._children:
            child.update()


class Scene(Object3D):
    pass


class Mesh(Object3D):
    def __init__(self, geometry, material, **kwargs):
        super().__init__(**kwargs)
        self.geometry = geometry
        self.material = material
