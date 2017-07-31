from .scenes import Object3D


__all__ = ('PointLight', 'Light')


class Light(Object3D):
    def __init__(self, uniforms=None, **kwargs):
        super().__init__(**kwargs)
        self.uniforms = uniforms or {}


class PointLight(Light):
    def update(self):
        if self.dirty:
            super().update()
            self.uniforms["light_pos"] = self._model * self._position
