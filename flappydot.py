import tkinter as tk

from gamelib import Sprite, GameApp, Text
import random

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 500

UPDATE_DELAY = 33
GRAVITY = 2.5
STARTING_VELOCITY = -30
JUMP_VELOCITY = -20
PILLAR_SPEED = 5


class Dot(Sprite):
    def init_element(self):
        self.vy = STARTING_VELOCITY
        self.is_started = False

    def update(self):
        if self.is_started:
            self.y += self.vy
            self.vy += GRAVITY

    def start(self):
        self.is_started = True

    def jump(self):
        self.vy = JUMP_VELOCITY

    def is_out_of_screen(self):
        if self.y >= 500 or self.y <= -20:
            return True
        return False

    def is_hit(self, pillar_pair):
        if (pillar_pair.x - 40 <= self.x + 15 <= pillar_pair.x + 40) or (pillar_pair.x - 40 <= self.x - 15 <= pillar_pair.x + 40):
            if (self.y - 15 <= pillar_pair.y - 100) or (pillar_pair.y + 100 <= self.y + 15):
                return True
        return False


class PillarPair(Sprite):
    def init_element(self):
        self.vx = PILLAR_SPEED
        self.is_started = False

    def update(self):
        if self.is_started:
            self.x -= self.vx

    def is_out_of_screen(self):
        if self.x == -40:
            return True
        return False

    def start(self):
        self.is_started = True

    def reset_position(self):
        self.x = CANVAS_WIDTH + 40

    def random_height(self):
        self.y = random.randrange(100, CANVAS_HEIGHT - 100)

    def is_hit(self, dot):
        if (self.x - 40 <= dot.x + 15 <= self.x + 40) or (self.x - 40 <= dot.x - 15 <= self.x + 40):
            if (dot.y - 15 <= self.y - 100) or (self.y + 100 <= dot.y + 15):
                return True
        return False


class FlappyGame(GameApp):
    def create_sprites(self):
        self.pillar_pair_list = []
        self.dot = Dot(self, 'images/dot.png', CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2)
        self.elements.append(self.dot)

        self.pillar_pair1 = PillarPair(self, 'images/pillar-pair.png', CANVAS_WIDTH, random.randrange(100, CANVAS_HEIGHT - 100))
        self.pillar_pair_list.append(self.pillar_pair1)
        self.elements.append(self.pillar_pair1)

        self.pillar_pair2 = PillarPair(self, 'images/pillar-pair.png', CANVAS_WIDTH + 300, random.randrange(100, CANVAS_HEIGHT - 100))
        self.pillar_pair_list.append(self.pillar_pair2)
        self.elements.append(self.pillar_pair2)

        self.pillar_pair3 = PillarPair(self, 'images/pillar-pair.png', CANVAS_WIDTH + 600, random.randrange(100, CANVAS_HEIGHT - 100))
        self.pillar_pair_list.append(self.pillar_pair3)
        self.elements.append(self.pillar_pair3)

        self.score_text = Text(self, 'Score: XX', 40, 20)
        self.elements.append(self.score_text)

    def update_score_text(self):
        self.score_text.set_text(f'Score: {self.score}')
        self.score += 1

    def init_game(self):
        self.create_sprites()

        self.score = 0
        self.update_score_text()
        self.game_over = False

    def pre_update(self):
        pass

    def post_update(self):
        for pillar_pair in self.pillar_pair_list:
            if pillar_pair.is_out_of_screen():
                pillar_pair.reset_position()
                pillar_pair.random_height()
                pillar_pair.passed = False
        for pillar_pair in self.pillar_pair_list:
            if self.dot.is_out_of_screen() or (self.dot.is_hit(pillar_pair) or pillar_pair.is_hit(self.dot)):
                self.game_over = True
                self.dot.is_started = False
                for pillar_pair in self.pillar_pair_list:
                    pillar_pair.is_started = False
        for pillar_pair in self.pillar_pair_list:
            if pillar_pair.x == (CANVAS_WIDTH // 2) - 20:
                self.update_score_text()

    def on_key_pressed(self, event):
        if not self.game_over:
            if event.char == " ":
                if self.dot.is_started:
                    self.dot.jump()
                else:
                    self.dot.start()
                    for pillar_pair in self.pillar_pair_list:
                        pillar_pair.start()
        else:
            if event.char == " ":
                refresh()


def game():
    global root
    root = tk.Tk()
    root.title("Flappy Dot Game")
    # do not allow window resizing
    root.resizable(False, False)
    app = FlappyGame(root, CANVAS_WIDTH, CANVAS_HEIGHT, UPDATE_DELAY)
    app.start()
    root.mainloop()


if __name__ == '__main__':
    def refresh():
        root.destroy()
        game()

    game()
