import tkinter as tk

from gamelib import Sprite, GameApp, Text
import random

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 500

UPDATE_DELAY = 33
GRAVITY = 2.5
STARTING_VELOCITY = -30
PILLAR_SPEED = 10


class Dot(Sprite):
    def init_element(self):
        self.vy = STARTING_VELOCITY

    def update(self):
        self.y += self.vy
        self.vy += GRAVITY


class PillarPair(Sprite):
    def init_element(self):
        self.vx = PILLAR_SPEED

    def update(self):
        if self.is_out_of_screen():
            self.reset_position()
        self.x -= self.vx

    def is_out_of_screen(self):
        if self.x == -40:
            return True
        return False

    def reset_position(self):
        self.x = CANVAS_WIDTH + 40

    def random_height(self):
        pass


class FlappyGame(GameApp):
    def create_sprites(self):
        self.dot = Dot(self, 'images/dot.png', CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2)
        self.pillar_pair = PillarPair(self, 'images/pillar-pair.png', CANVAS_WIDTH, CANVAS_HEIGHT // 2)
        self.elements.append(self.dot)
        self.elements.append(self.pillar_pair)

    def init_game(self):
        self.create_sprites()

    def pre_update(self):
        pass

    def post_update(self):
        pass

    def on_key_pressed(self, event):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Monkey Banana Game")
 
    # do not allow window resizing
    root.resizable(False, False)
    app = FlappyGame(root, CANVAS_WIDTH, CANVAS_HEIGHT, UPDATE_DELAY)
    app.start()
    root.mainloop()
