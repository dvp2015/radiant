from functools import lru_cache

import ModernGL
import numpy as np

from .base import Renderer
from ..scenes import Mesh


class ModernGLRenderer(Renderer):
    def __init__(self, context):
        self.ctx = context

    def render(self, scene, camera, light=None):
        """
        Render scene from the camera viewpoint.
        """
        camera.update()
        if light:
            light.update()

        def visit(node):
            node.update()
            self.render_object(node, camera, light=light)
            for child in node.children:
                visit(child)

        # get going
        self.ctx.enable(ModernGL.DEPTH_TEST)
        self.ctx.clear(0.9, 0.9, 0.9)
        visit(scene)
        self.ctx.finish()

    @lru_cache(maxsize=None)
    def get_vertex_array(self, node):
        # get the shader program
        mapping = {
            'vert': self.ctx.vertex_shader,
            'geom': self.ctx.geometry_shader,
            'frag': self.ctx.fragment_shader,
        }
        shaders = [mapping[key](source) for key, source in node.material.shaders.items()]
        prog = self.ctx.program(shaders)

        # build the vertex buffers
        vertex_buffers = [
            (self.ctx.buffer(data.tobytes()), f"{data.shape[-1]}{data.dtype.kind}", [key])
            for key, data in node.geometry.attributes.items() if key in prog.attributes
        ]

        # build the index buffers
        index_buffer = None
        if node.geometry.index is not None:
            index_buffer = self.ctx.buffer(node.geometry.index.tobytes())

        # construct the vertex array
        return self.ctx.vertex_array(prog, vertex_buffers, index_buffer)

    def render_object(self, node, camera, light=None):
        if isinstance(node, Mesh):
            # get the vao
            vao = self.get_vertex_array(node)

            # compute transforms for this node
            model_view_matrix = camera.view * node.model
            normal_matrix = model_view_matrix.inverse.T

            # set the transformation uniforms
            uniforms = {
                'model_view_matrix': model_view_matrix,
                'projection_matrix': camera.projection,
                'normal_matrix': normal_matrix,
            }
            if light:
                # add the light uniforms
                uniforms['light_pos'] = light.position
            # add the material uniforms
            uniforms.update(node.material.uniforms)

            # assign them based on the program needs
            for key, _ in vao.program.uniforms:
                value = uniforms[key]
                if isinstance(value, np.ndarray):
                    vao.program.uniforms[key].write(value.tobytes())
                elif isinstance(value, (tuple, float, int)):
                    vao.program.uniforms[key].value = value
                else:
                    raise ValueError(f"{type(value)} is not a supported type as a uniform value")

            # do it
            mgl_primitive = getattr(ModernGL, node.geometry.primitive.name)
            vao.render(mgl_primitive)
