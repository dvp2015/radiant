import numpy as np


class Renderer:
    pass


class ModernGLRenderer:
    def __init__(self, context):
        self.ctx = context
        self.model_stack = [np.eye(4, dtype='f4')]

    def render(self, scene, camera):
        def visit(node):
            self.model_stack.append(self.model_stack[-1] @ node.model)
            self.render_object(node, camera, self.model_stack[-1])
            for child in scene.children:
                visit(child)
            self.model_stack.pop()
        visit(scene)

    def render_object(self, object, camera, world):
        print(world)
