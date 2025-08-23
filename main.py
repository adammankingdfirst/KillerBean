# main.py
import random
import pygame as pg
from settings import WIDTH, HEIGHT, FPS, BLACK, WHITE, GREEN, ENEMY_SPAWN_EVERY, PLAYER_MAX_HEALTH
from player import Player
from enemy import Enemy

class Game:
    def __init__(self):
        pg.init()
        pg.display.set_caption("Killer Bean (Pygame)")
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.running = True

        self.all_sprites = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.enemies = pg.sprite.Group()

        self.player = Player((WIDTH // 2, HEIGHT // 2), self.bullets, self.all_sprites)
        self.all_sprites.add(self.player)

        self.spawn_timer = 0.0
        self.score = 0
        self.font = pg.font.SysFont("consolas", 20)
        self.play_area = self.screen.get_rect()

    def spawn_enemy(self):
        e = Enemy(self.player)
        self.enemies.add(e)
        self.all_sprites.add(e)

    def handle_events(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.running = False
            if e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
                self.running = False

    def update(self, dt):
        self.all_sprites.update(dt)

        # collisions: bullets -> enemies
        for enemy in pg.sprite.groupcollide(self.enemies, self.bullets, False, True):
            enemy.hit(1)
            if not enemy.alive():
                self.score += 10

        # collisions: enemies -> player
        hits = pg.sprite.spritecollide(self.player, self.enemies, False, pg.sprite.collide_rect_ratio(0.8))
        if hits:
            self.player.health -= 1
            for h in hits:
                # knock back a bit on hit
                away = (h.pos - self.player.pos)
                if away.length_squared() > 0:
                    h.pos += away.normalize() * 30
                    h.rect.center = h.pos
            if self.player.health <= 0:
                self.running = False

        # spawn enemies over time
        self.spawn_timer += dt
        if self.spawn_timer >= ENEMY_SPAWN_EVERY:
            self.spawn_timer = 0.0
            self.spawn_enemy()

    def draw_ui(self):
        # score
        txt = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(txt, (12, 10))
        # health
        for i in range(self.player.health):
            pg.draw.rect(self.screen, GREEN, (12 + i * 18, 36, 14, 10), border_radius=3)

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.draw_ui()
        pg.display.flip()

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()

if __name__ == "__main__":
    Game().run()
    pg.quit()
