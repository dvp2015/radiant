import numpy as np
import pyrr

from .scenes import Object3D


__all__ = ('Camera', 'PerspectiveCamera', 'pan_camera')


class Camera(Object3D):
    def __init__(self, target=(0, 0, 0), up=(0, 1, 0), **kwargs):
        super().__init__(**kwargs)
        self._view = None
        self._view_dirty = False
        self.target = target
        self.up = up

    @property
    def view(self):
        if self._view_dirty:
            self._view = pyrr.Matrix44.look_at(self._position, self._target, self._up, dtype='f4')
            self._view.flags.writeable = False
            self._view_dirty = False
        return self._view

    @Object3D.position.setter
    def position(self, value):
        Object3D.position.fset(self, value)  # https://bugs.python.org/issue14965#msg179217
        self._view_dirty = True

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, value):
        self._target = pyrr.Vector3(value, dtype='f4')
        self._target.flags.writeable = False
        self._view_dirty = True

    @property
    def up(self):
        return self._up

    @up.setter
    def up(self, value):
        self._up = pyrr.Vector3(value, dtype='f4')
        self._up.flags.writeable = False
        self._view_dirty = True

    @property
    def view_side(self):
        return pyrr.Vector3(np.asarray(self._view)[0:3, 0])

    @property
    def view_up(self):
        return pyrr.Vector3(np.asarray(self._view)[0:3, 1])

    @property
    def view_forward(self):
        return pyrr.Vector3(-np.asarray(self._view)[0:3, 2])

    def look_at(self, eye, target, up=None):
        self.position = eye
        self.target = target
        if up is not None:
            self.up = up


def pan_camera(camera, x, y, sensitivity=1.0):
    t = camera.view_side * x * sensitivity + camera.view_up * y * sensitivity
    camera.look_at(camera.position + t, camera.target + t)


class PerspectiveCamera(Camera):
    def __init__(self, fov=45.0, aspect=4.0/3.0, near=0.1, far=1000.0, **kwargs):
        super().__init__(**kwargs)
        self._projection = None
        self._projection_dirty = False
        self.fov = fov
        self.aspect = aspect
        self.near = near
        self.far = far

    @property
    def projection(self):
        if self._projection_dirty:
            self._projection = pyrr.Matrix44.perspective_projection(self._fov, self._aspect, self._near, self._far, dtype='f4')
            self._projection.flags.writeable = False
            self._projection_dirty = False
        return self._projection

    @property
    def fov(self):
        return self._fov

    @fov.setter
    def fov(self, value):
        self._fov = value
        self._projection_dirty = True

    @property
    def aspect(self):
        return self._aspect

    @aspect.setter
    def aspect(self, value):
        self._aspect = value
        self._projection_dirty = True

    @property
    def near(self):
        return self._near

    @near.setter
    def near(self, value):
        self._near = value
        self._projection_dirty = True

    @property
    def far(self):
        return self._far

    @far.setter
    def far(self, value):
        self._far = value
        self._projection_dirty = True
