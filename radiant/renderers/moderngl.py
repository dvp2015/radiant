from collections import OrderedDict
from functools import lru_cache

import ModernGL

import pyrr

from .base import Renderer
from ..materials import MeshBasicMaterial
from ..scenes import Mesh


class ModernGLRenderer(Renderer):
    def __init__(self, context):
        self.ctx = context
        self.model_stack = [pyrr.Matrix44.identity(dtype='f4')]

    def render(self, scene, camera):
        """
        Render scene from the camera viewpoint.
        """
        view_projection = camera.projection * camera.view

        def visit(node):
            self.model_stack.append(self.model_stack[-1] * node.model)
            self.render_object(node, view_projection, self.model_stack[-1])
            for child in node.children:
                visit(child)
            self.model_stack.pop()

        # get going
        self.ctx.enable(ModernGL.DEPTH_TEST)
        self.ctx.clear(0.9, 0.9, 0.9)
        visit(scene)

    @lru_cache(maxsize=None)
    def get_vertex_array(self, node):
        # get the shader program
        mapping = OrderedDict([
            ('vert', self.ctx.vertex_shader),
            ('geom', self.ctx.geometry_shader),
            ('frag', self.ctx.fragment_shader),
        ])
        shaders = [mapping[key](source) for key, source in node.material.shaders.items()]
        prog = self.ctx.program(shaders)

        # build the vertex buffers
        vertex_buffers = [
            (self.ctx.buffer(data.tobytes()), f"{data.shape[-1]}{data.dtype.kind}", [key])
            for key, data in node.geometry.attributes.items()
        ]

        # build the index buffers
        index_buffer = None
        if node.geometry.index is not None:
            index_buffer = self.ctx.buffer(node.geometry.index.tobytes())

        # construct the vertex array
        return self.ctx.vertex_array(prog, vertex_buffers, index_buffer)

    def render_object(self, node, view_projection, world):
        if isinstance(node, Mesh):
            # get the vao
            vao = self.get_vertex_array(node)

            # configure uniforms
            vao.program.uniforms['mvp'].write((view_projection * world).tobytes())
            if isinstance(node.material, MeshBasicMaterial):
                vao.program.uniforms['color'].value = node.material.color

            # do it
            vao.render()
