from array import array
import time

import arcade
import arcade.gl as gl

import constants as c
import planets
import images


class FullScreenShader(arcade.View):

    def __init__(self):
        super().__init__()
        self.ctx = self.window.ctx

        self.program = self.ctx.load_program(
            vertex_shader="shaders/planet_shaders/vertex_fullscreen.glsl",
            fragment_shader="shaders/planet_shaders/fragment_fullscreen.glsl"
        )

        self.program['planet_data'] = planets.Earth.shader_data

        self.featureless_texture = self.ctx.texture((720, 720), data=images.earth.tobytes(), components=4,
                                                    wrap_x=gl.CLAMP_TO_EDGE, wrap_y=gl.CLAMP_TO_EDGE,
                                                    filter=(gl.NEAREST, gl.NEAREST))

        self.buffer = self.ctx.buffer(data=array('f', (-1, -1, -1, 3, 3, -1)))
        self.geometry = self.ctx.geometry([gl.BufferDescription(self.buffer, "2f", ['vert_pos'])])

        self.animation_start = None

    def on_update(self, delta_time: float):
        planets.Earth.on_update(delta_time)

    def on_draw(self):
        arcade.start_render()

        if self.animation_start is None:
            self.animation_start = time.time()
            time_start = 0
        else:
            time_start = time.time() - self.animation_start

        self.program['zoom'] = self.window.zoom
        self.program['time'] = time_start

        self.program['camera_data'] = (self.window.view_x, self.window.view_y,
                                       c.SCREEN_WIDTH, c.SCREEN_HEIGHT)
        self.program['planet_data'] = planets.Earth.shader_data

        self.featureless_texture.use(0)

        self.geometry.render(self.program, mode=self.ctx.TRIANGLES)
