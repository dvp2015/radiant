import numpy as np
import pyrr

from .scenes import Object3D


__all__ = ('Camera', 'PerspectiveCamera', 'OrthographicCamera', 'pan_camera', 'dolly_camera', 'rotate_camera')


class Camera(Object3D):
    def __init__(self, target=(0, 0, 0), up=(0, 1, 0), **kwargs):
        super().__init__(**kwargs)
        self._view = None
        self._view_dirty = False
        self.target = target
        self.up = up

    def model_dirty(self):
        super().model_dirty()
        self._view_dirty = True

    @property
    def view(self):
        if self._view_dirty:
            self._view = pyrr.Matrix44.look_at(self.position, self.target, self._up, dtype='f4')
            self._view.flags.writeable = False
            self._view_dirty = False
        return self._view

    @property
    def target(self):
        return self._target

    @property
    def target_world(self):
        return self.position_world + (self.target - self.position)

    @target.setter
    def target(self, value):
        self._target = pyrr.Vector3(value, dtype='f4')
        self._target.flags.writeable = False
        self.model_dirty()

    @property
    def up(self):
        return self._up

    @up.setter
    def up(self, value):
        self._up = pyrr.Vector3(value, dtype='f4')
        self._up.flags.writeable = False
        self.model_dirty()

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


class PerspectiveCamera(Camera):
    def __init__(self, fov=45.0, aspect=4.0/3.0, near=0.1, far=1000.0, **kwargs):
        super().__init__(**kwargs)
        self._projection = None
        self._projection_dirty = False
        self._view_projection = None
        self._view_projection_dirty = False
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

    def model_dirty(self):
        super().model_dirty()
        self._view_projection_dirty = True

    @property
    def view_projection(self):
        if self._view_projection_dirty:
            self._view_projection = self.projection * self.view
            self._view_projection.flags.writeable = False
            self._view_projection_dirty = False
        return self._view_projection

    @property
    def fov(self):
        return self._fov

    @fov.setter
    def fov(self, value):
        self._fov = value
        self._projection_dirty = True
        self._view_projection_dirty = True

    def zoom(self, amount):
        self.fov -= amount
        if self.fov < 0.00000001:
            self.fov = 0.00000001
        if self.fov > 179.0:
            self.fov = 179.0

    @property
    def aspect(self):
        return self._aspect

    @aspect.setter
    def aspect(self, value):
        self._aspect = value
        self._projection_dirty = True
        self._view_projection_dirty = True

    @property
    def near(self):
        return self._near

    @near.setter
    def near(self, value):
        self._near = value
        self._projection_dirty = True
        self._view_projection_dirty = True

    @property
    def far(self):
        return self._far

    @far.setter
    def far(self, value):
        self._far = value
        self._projection_dirty = True
        self._view_projection_dirty = True


class OrthographicCamera(Camera):
    def __init__(self, left=-10.0, right=10.0, bottom=-10.0, top=10.0, near=0.1, far=1000.0, **kwargs):
        super().__init__(**kwargs)
        self._projection = None
        self._projection_dirty = False
        self._view_projection = None
        self._view_projection_dirty = False
        self.left = left
        self.right = right
        self.bottom = bottom
        self.top = top
        self.near = near
        self.far = far

    @property
    def projection(self):
        if self._projection_dirty:
            self._projection = pyrr.Matrix44.orthogonal_projection(self._left, self._right, self._bottom, self._top, self._near, self._far, dtype='f4')
            self._projection.flags.writeable = False
            self._projection_dirty = False
        return self._projection

    def model_dirty(self):
        super().model_dirty()
        self._view_projection_dirty = True

    @property
    def view_projection(self):
        if self._view_projection_dirty:
            self._view_projection = self.projection * self.view
            self._view_projection.flags.writeable = False
            self._view_projection_dirty = False
        return self._view_projection

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, value):
        self._left = value
        self._projection_dirty = True
        self._view_projection_dirty = True

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, value):
        self._right = value
        self._projection_dirty = True
        self._view_projection_dirty = True

    @property
    def bottom(self):
        return self._bottom

    @bottom.setter
    def bottom(self, value):
        self._bottom = value
        self._projection_dirty = True
        self._view_projection_dirty = True

    @property
    def top(self):
        return self._top

    @top.setter
    def top(self, value):
        self._top = value
        self._projection_dirty = True
        self._view_projection_dirty = True

    @property
    def near(self):
        return self._near

    @near.setter
    def near(self, value):
        self._near = value
        self._projection_dirty = True
        self._view_projection_dirty = True

    @property
    def far(self):
        return self._far

    @far.setter
    def far(self, value):
        self._far = value
        self._projection_dirty = True
        self._view_projection_dirty = True

    def zoom(self, amount):
        raise NotImplementedError()


def pan_camera(camera, x, y, sensitivity=1.0):
    t = camera.view_side * x * sensitivity + camera.view_up * y * sensitivity
    camera.look_at(camera.position + t, camera.target + t)


def dolly_camera(camera, amount, sensitivity=1.0):
    """Move the camera towards (positive amount) or away from (negative amount) the target by a fraction of the current distance."""
    camera.position = camera.position + (camera.position - camera.target) * amount * sensitivity


def rotate_camera(camera, azimuth, elevation, sensitivity=1.0):
    # rotate camera about view_up centered at target
    t_a = (pyrr.Matrix44.from_translation(camera.target) *
           pyrr.Matrix44(pyrr.matrix44.create_from_axis_rotation(camera.view_up, azimuth * sensitivity)) *
           pyrr.Matrix44.from_translation(-camera.target))
    camera.position = t_a * camera.position
    # rotate camera about view_side centered at target
    t_e = (pyrr.Matrix44.from_translation(camera.target) *
           pyrr.Matrix44(pyrr.matrix44.create_from_axis_rotation(camera.view_side, elevation * sensitivity)) *
           pyrr.Matrix44.from_translation(-camera.target))
    camera.position = t_e * camera.position
