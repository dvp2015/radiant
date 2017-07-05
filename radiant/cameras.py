import pyrr


UP = [0, 1, 0]


class Camera:
    def __init__(self, eye, target, up=None):
        self.view = None
        self.projection = None

        self.look_at(eye, target, up=up)

    def look_at(self, eye, target, up=None):
        self.view = pyrr.Matrix44.look_at(eye, target, up or UP).astype('f4')


class PerspectiveCamera(Camera):
    def __init__(self, eye, target, up=None, fov=45.0, aspect=4.0/3.0, near=0.1, far=1000.0):
        super().__init__(eye, target, up=up)
        self.projection = pyrr.Matrix44.perspective_projection(
            fov, aspect, near, far, dtype='f4')
