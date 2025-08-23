# bullet.py
import pygame as pg
from settings import ACCENT, WIDTH, HEIGHT

class Bullet(pg.sprite.Sprite):
    def __init__(self, pos, vel):
        super().__init__()
        self.image = pg.Surface((12, 4), pg.SRCALPHA)
        pg.draw.rect(self.image, ACCENT, (0, 0, 12, 4), border_radius=2)
        self.rect = self.image.get_rect(center=pos)
        self.pos = pg.Vector2(pos)
        self.vel = pg.Vector2(vel)
        self.lifetime = 1.5
        self.age = 0.0

        # rotate visual to direction
        angle = self.vel.angle_to(pg.Vector2(1, 0))
        self.image = pg.transform.rotozoom(self.image, -angle, 1.0)
        self.rect = self.image.get_rect(center=pos)

    def update(self, dt):
        self.age += dt
        if self.age > self.lifetime:
            self.kill()
            return
        self.pos += self.vel * dt
        self.rect.center = self.pos
        if self.rect.right < 0 or self.rect.left > WIDTH or self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()
