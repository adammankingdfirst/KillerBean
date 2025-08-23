# enemy.py
import random
import pygame as pg
from settings import ENEMY_SPEED, RED, WHITE, WIDTH, HEIGHT

class Enemy(pg.sprite.Sprite):
    def __init__(self, player, pos=None):
        super().__init__()
        self.base_image = pg.Surface((32, 24), pg.SRCALPHA)
        pg.draw.rect(self.base_image, RED, (0, 4, 32, 16), border_radius=8)
        pg.draw.rect(self.base_image, WHITE, (6, 8, 6, 6), border_radius=3)
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect()

        self.player = player
        self.pos = pg.Vector2(pos or self._spawn_pos())
        self.rect.center = self.pos
        self.health = 2

    def _spawn_pos(self):
        side = random.choice(["top", "bottom", "left", "right"])
        margin = 20
        if side == "top":
            return (random.randint(margin, WIDTH - margin), -margin)
        if side == "bottom":
            return (random.randint(margin, WIDTH - margin), HEIGHT + margin)
        if side == "left":
            return (-margin, random.randint(margin, HEIGHT - margin))
        return (WIDTH + margin, random.randint(margin, HEIGHT - margin))

    def update(self, dt):
        to_player = self.player.pos - self.pos
        if to_player.length_squared() > 1:
            dir_vec = to_player.normalize()
            self.pos += dir_vec * ENEMY_SPEED * dt
            self.rect.center = self.pos

    def hit(self, dmg=1):
        self.health -= dmg
        if self.health <= 0:
            self.kill()
