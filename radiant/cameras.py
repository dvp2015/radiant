import numpy as np
import pyrr

from .scenes import Object3D


__all__ = ('Camera', 'PerspectiveCamera', 'pan_camera')


class Camera(Object3D):
    def __init__(self, target=(0, 0, 0), up=(0, 1, 0), **kwargs):
        super().__init__(**kwargs)
        self.target = target
        self.up = up
        self._view = None

    @property
    def view(self):
        return self._view

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, value):
        self._target = pyrr.Vector3(value, dtype='f4')
        self._target.flags.writeable = False
        self.dirty = True

    @property
    def up(self):
        return self._up

    @up.setter
    def up(self, value):
        self._up = pyrr.Vector3(value, dtype='f4')
        self._up.flags.writeable = False
        self.dirty = True

    @property
    def view_side(self):
        return pyrr.Vector3(np.asarray(self._view)[0:3, 0])

    @property
    def view_up(self):
        return pyrr.Vector3(np.asarray(self._view)[0:3, 1])

    @property
    def view_forward(self):
        return pyrr.Vector3(-np.asarray(self._view)[0:3, 2])

    def update(self):
        if self.dirty:
            self._view = pyrr.Matrix44.look_at(self._position, self._target, self._up, dtype='f4')
            self._view.flags.writeable = False
        super().update()

    def look_at(self, eye, target, up=None):
        self.position = eye
        self.target = target
        if up is not None:
            self.up = up


def pan_camera(camera, x, y):
    t = camera.view_side * x + camera.view_up * y
    camera.look_at(camera.position + t, camera.target + t)


class PerspectiveCamera(Camera):
    def __init__(self, fov=45.0, aspect=4.0/3.0, near=0.1, far=1000.0, **kwargs):
        super().__init__(**kwargs)
        self._projection = None
        self._fov = fov
        self._aspect = aspect
        self._near = near
        self._far = far

    @property
    def projection(self):
        return self._projection

    @property
    def fov(self):
        return self._fov

    @fov.setter
    def fov(self, value):
        self._fov = value
        self.dirty = True

    @property
    def near(self):
        return self._near

    @near.setter
    def near(self, value):
        self._near = value
        self.dirty = True

    @property
    def far(self):
        return self._far

    @far.setter
    def far(self, value):
        self._far = value
        self.dirty = True

    def update(self):
        if self.dirty:
            self._projection = pyrr.Matrix44.perspective_projection(self._fov, self._aspect, self._near, self._far, dtype='f4')
            self._projection.flags.writeable = False
        super().update()
