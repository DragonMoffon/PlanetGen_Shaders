from array import array

import arcade
import arcade.gl as gl

import constants
import planets
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from shaderview import FullScreenShader


class ShaderWindow(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Planet Shaders", fullscreen=True)
        self.view_x, self.view_y = 0, 0
        arcade.set_viewport(self.view_x, SCREEN_WIDTH, self.view_y, SCREEN_HEIGHT)
        self.fullscreen_view = FullScreenShader()

        self.show_view(self.fullscreen_view)

        self.horizontal = 0
        self.vertical = 0

        self.zoom = 1
        self.shift = False

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            self.close()
        elif symbol == arcade.key.TAB:
            self.minimize()
        elif symbol == arcade.key.LSHIFT:
            self.shift = True
        elif symbol == arcade.key.LEFT or symbol == arcade.key.A:
            self.horizontal -= 1
        elif symbol == arcade.key.RIGHT or symbol == arcade.key.D:
            self.horizontal += 1
        elif symbol == arcade.key.UP or symbol == arcade.key.W:
            self.vertical += 1
        elif symbol == arcade.key.DOWN or symbol == arcade.key.S:
            self.vertical -= 1

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.LSHIFT:
            self.shift = False
        if symbol == arcade.key.LEFT or symbol == arcade.key.A:
            self.horizontal += 1
        elif symbol == arcade.key.RIGHT or symbol == arcade.key.D:
            self.horizontal -= 1
        elif symbol == arcade.key.UP or symbol == arcade.key.W:
            self.vertical -= 1
        elif symbol == arcade.key.DOWN or symbol == arcade.key.S:
            self.vertical += 1

    def on_update(self, delta_time: float):
        last_x = self.view_x
        self.view_x = (self.view_x + int(self.horizontal * SCREEN_WIDTH * self.zoom * delta_time))

        last_y = self.view_y
        self.view_y = (self.view_y + int(self.vertical * SCREEN_HEIGHT * self.zoom * delta_time))

        if self.view_x - last_x or self.view_y - last_y:
            arcade.set_viewport(self.view_x, self.view_x + SCREEN_WIDTH*self.zoom,
                                self.view_y, self.view_y + SCREEN_HEIGHT*self.zoom)

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        last_z = self.zoom
        zoom_speed = 100 if not self.shift else 1
        self.zoom = min(max(self.zoom - scroll_y*zoom_speed, 1), 10000000000.0)
        if self.zoom - last_z:
            print(self.zoom)
            self.view_x = self.view_x + x*last_z - x*self.zoom
            self.view_y = self.view_y + y*last_z - y*self.zoom

            arcade.set_viewport(self.view_x, self.view_x + SCREEN_WIDTH * self.zoom,
                                self.view_y, self.view_y + SCREEN_HEIGHT * self.zoom)

    def on_draw(self):
        arcade.draw_text("bruh", SCREEN_WIDTH//2, SCREEN_HEIGHT//2, arcade.color.WINE)

        earth_pos = planets.Earth.pos
        arcade.draw_point(*earth_pos, arcade.color.WINE, 15)

        arcade.draw_line(*earth_pos,
                         self.view_x+((SCREEN_WIDTH*self.zoom)//2), self.view_y + (SCREEN_HEIGHT*self.zoom)//2,
                         arcade.color.WINE, 1)
