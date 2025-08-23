# player.py
import pygame as pg
from settings import PLAYER_SPEED, FIRE_RATE, BULLET_SPEED, WHITE, ACCENT

class Player(pg.sprite.Sprite):
    def __init__(self, pos, bullet_group, all_sprites):
        super().__init__()
        self.base_image = pg.Surface((40, 28), pg.SRCALPHA)
        pg.draw.rect(self.base_image, WHITE, (0, 6, 40, 16), border_radius=8)
        pg.draw.polygon(self.base_image, ACCENT, [(36, 14), (40, 12), (40, 16)])  # muzzle tip
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect(center=pos)
        self.pos = pg.Vector2(pos)
        self.vel = pg.Vector2()
        self.angle = 0
        self.fire_cooldown = 1.0 / FIRE_RATE
        self.time_since_shot = 0.0
        self.bullet_group = bullet_group
        self.all_sprites = all_sprites
        self.health = 5

    def handle_input(self):
        keys = pg.key.get_pressed()
        self.vel.xy = 0, 0
        if keys[pg.K_w]: self.vel.y = -1
        if keys[pg.K_s]: self.vel.y = 1
        if keys[pg.K_a]: self.vel.x = -1
        if keys[pg.K_d]: self.vel.x = 1
        if self.vel.length_squared() > 0:
            self.vel = self.vel.normalize()

    def aim_to_mouse(self):
        mx, my = pg.mouse.get_pos()
        aim_vec = pg.Vector2(mx, my) - self.pos
        if aim_vec.length_squared() > 0:
            self.angle = aim_vec.angle_to(pg.Vector2(1, 0))
            self.image = pg.transform.rotozoom(self.base_image, -self.angle, 1.0)
            self.rect = self.image.get_rect(center=self.pos)

    def try_shoot(self, dt):
        buttons = pg.mouse.get_pressed(3)
        self.time_since_shot += dt
        if buttons[0] and self.time_since_shot >= self.fire_cooldown:
            self.time_since_shot = 0.0
            dir_vec = pg.Vector2(1, 0).rotate(self.angle)
            from bullet import Bullet
            muzzle = self.pos + dir_vec * 24
            bullet = Bullet(muzzle, dir_vec * BULLET_SPEED)
            self.bullet_group.add(bullet)
            self.all_sprites.add(bullet)

    def update(self, dt, bounds_rect):
        self.handle_input()
        self.pos += self.vel * PLAYER_SPEED * dt
        self.pos.x = max(bounds_rect.left + 20, min(bounds_rect.right - 20, self.pos.x))
        self.pos.y = max(bounds_rect.top + 20, min(bounds_rect.bottom - 20, self.pos.y))
        self.rect.center = self.pos
        self.aim_to_mouse()
        self.try_shoot(dt)
