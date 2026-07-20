import math
import os
import random
import sys

import pygame

WIDTH = 960
HEIGHT = 540
FPS = 60

BG_COLOR = (7, 10, 24)
TEXT_COLOR = (240, 245, 255)
ACCENT_COLOR = (104, 255, 180)
PANEL_COLOR = (20, 31, 58)
PLAYER_COLOR = (92, 214, 255)
ENEMY_COLOR = (255, 92, 92)
PICKUP_COLOR = (255, 214, 102)


class NovaDriftGame:
    def __init__(self):
        self.score = 0
        self.lives = 3
        self.player = Player()
        self.enemies = []
        self.pickups = []
        self.spawn_timer = 0.0
        self.pickup_timer = 0.0
        self.state = "playing"
        self.title = "Nova Drift"
        self.description = "Dodge the storm, collect the shards, and survive the climb."

    def reset(self):
        self.score = 0
        self.lives = 3
        self.player = Player()
        self.enemies = []
        self.pickups = []
        self.spawn_timer = 0.0
        self.pickup_timer = 0.0
        self.state = "playing"

    def update(self, dt, keys):
        if self.state != "playing":
            return
        self.player.update(dt, keys)
        self.spawn_timer += dt
        self.pickup_timer += dt

        if self.spawn_timer > 0.6:
            self.enemies.append(Enemy())
            self.spawn_timer = 0.0
        if self.pickup_timer > 1.2:
            self.pickups.append(Pickup())
            self.pickup_timer = 0.0

        for enemy in list(self.enemies):
            enemy.update(dt)
            if self.collides(self.player, enemy):
                self.enemies.remove(enemy)
                self.lives -= 1
            elif enemy.y - enemy.radius > HEIGHT:
                self.enemies.remove(enemy)

        for pickup in list(self.pickups):
            pickup.update(dt)
            if self.collides(self.player, pickup):
                self.pickups.remove(pickup)
                self.score += 15
            elif pickup.y - pickup.radius > HEIGHT:
                self.pickups.remove(pickup)

        if self.lives <= 0:
            self.state = "game_over"

    def draw(self, screen, fonts):
        screen.fill(BG_COLOR)
        pygame.draw.rect(screen, (15, 24, 45), (0, 0, WIDTH, HEIGHT), border_radius=24)
        pygame.draw.rect(screen, (24, 38, 73), (26, 26, WIDTH - 52, HEIGHT - 52), border_radius=22)
        self.player.draw(screen)
        for enemy in self.enemies:
            enemy.draw(screen)
        for pickup in self.pickups:
            pickup.draw(screen)

        score_text = fonts["font"].render(f"Score: {self.score}", True, TEXT_COLOR)
        lives_text = fonts["font"].render(f"Lives: {self.lives}", True, (255, 184, 92))
        screen.blit(score_text, (28, 24))
        screen.blit(lives_text, (28, 58))
        hint_text = fonts["small_font"].render("Move with WASD or arrows", True, (180, 195, 235))
        screen.blit(hint_text, (28, HEIGHT - 38))

        if self.state == "game_over":
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 170))
            screen.blit(overlay, (0, 0))
            title = fonts["title_font"].render("Run ended", True, TEXT_COLOR)
            score = fonts["font"].render(f"Final score: {self.score}", True, ACCENT_COLOR)
            hint = fonts["font"].render("Press Enter to replay or Esc for menu", True, TEXT_COLOR)
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 80))
            screen.blit(score, (WIDTH // 2 - score.get_width() // 2, HEIGHT // 2 - 10))
            screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 2 + 40))

    def collides(self, player, obj):
        distance = math.hypot(player.x - obj.x, player.y - obj.y)
        return distance < player.radius + getattr(obj, "radius", 10)


class StarCollectorGame:
    def __init__(self):
        self.score = 0
        self.lives = 3
        self.player_x = WIDTH // 2
        self.player_y = HEIGHT - 70
        self.player_speed = 320
        self.stars = []
        self.hazards = []
        self.time = 0.0
        self.spawn_timer = 0.0
        self.state = "playing"
        self.title = "Star Collector"
        self.description = "Gather stars while dodging the falling meteors."

    def reset(self):
        self.score = 0
        self.lives = 3
        self.player_x = WIDTH // 2
        self.player_y = HEIGHT - 70
        self.stars = []
        self.hazards = []
        self.time = 0.0
        self.spawn_timer = 0.0
        self.state = "playing"

    def update(self, dt, keys):
        if self.state != "playing":
            return
        move_x = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])
        move_y = int(keys[pygame.K_DOWN] or keys[pygame.K_s]) - int(keys[pygame.K_UP] or keys[pygame.K_w])
        if move_x != 0 and move_y != 0:
            move_x *= 0.7071
            move_y *= 0.7071
        self.player_x += move_x * self.player_speed * dt
        self.player_y += move_y * self.player_speed * dt
        self.player_x = max(30, min(WIDTH - 30, self.player_x))
        self.player_y = max(30, min(HEIGHT - 30, self.player_y))

        self.time += dt
        self.spawn_timer += dt
        if self.spawn_timer > 0.5:
            if random.random() < 0.7:
                self.stars.append((random.randint(30, WIDTH - 30), -20))
            else:
                self.hazards.append((random.randint(30, WIDTH - 30), -20))
            self.spawn_timer = 0.0

        for star in list(self.stars):
            x, y = star
            y += 220 * dt
            if y > HEIGHT + 20:
                self.stars.remove(star)
            elif self.distance((self.player_x, self.player_y), (x, y)) < 28:
                self.stars.remove(star)
                self.score += 20
            else:
                self.stars[self.stars.index(star)] = (x, y)

        for hazard in list(self.hazards):
            x, y = hazard
            y += 260 * dt
            if y > HEIGHT + 20:
                self.hazards.remove(hazard)
            elif self.distance((self.player_x, self.player_y), (x, y)) < 30:
                self.hazards.remove(hazard)
                self.lives -= 1
            else:
                self.hazards[self.hazards.index(hazard)] = (x, y)

        if self.lives <= 0:
            self.state = "game_over"

    def distance(self, a, b):
        return math.hypot(a[0] - b[0], a[1] - b[1])

    def draw(self, screen, fonts):
        screen.fill(BG_COLOR)
        pygame.draw.rect(screen, (15, 24, 45), (0, 0, WIDTH, HEIGHT), border_radius=24)
        pygame.draw.rect(screen, (24, 38, 73), (26, 26, WIDTH - 52, HEIGHT - 52), border_radius=22)
        pygame.draw.circle(screen, PLAYER_COLOR, (int(self.player_x), int(self.player_y)), 18)
        for x, y in self.stars:
            pygame.draw.circle(screen, PICKUP_COLOR, (int(x), int(y)), 10)
        for x, y in self.hazards:
            pygame.draw.circle(screen, ENEMY_COLOR, (int(x), int(y)), 12)

        score_text = fonts["font"].render(f"Score: {self.score}", True, TEXT_COLOR)
        lives_text = fonts["font"].render(f"Lives: {self.lives}", True, (255, 184, 92))
        screen.blit(score_text, (28, 24))
        screen.blit(lives_text, (28, 58))
        hint_text = fonts["small_font"].render("Collect stars and avoid meteors", True, (180, 195, 235))
        screen.blit(hint_text, (28, HEIGHT - 38))

        if self.state == "game_over":
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 170))
            screen.blit(overlay, (0, 0))
            title = fonts["title_font"].render("Mission failed", True, TEXT_COLOR)
            score = fonts["font"].render(f"Final score: {self.score}", True, ACCENT_COLOR)
            hint = fonts["font"].render("Press Enter to replay or Esc for menu", True, TEXT_COLOR)
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 80))
            screen.blit(score, (WIDTH // 2 - score.get_width() // 2, HEIGHT // 2 - 10))
            screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 2 + 40))


class BrickBreakerGame:
    def __init__(self):
        self.score = 0
        self.lives = 3
        self.paddle_x = WIDTH // 2
        self.paddle_w = 120
        self.paddle_h = 18
        self.ball_x = WIDTH // 2
        self.ball_y = HEIGHT // 2
        self.ball_dx = 240
        self.ball_dy = -240
        self.ball_radius = 10
        self.bricks = []
        self.state = "playing"
        self.title = "Brick Breaker"
        self.description = "Break every brick with a bouncing ball."
        self._build_bricks()

    def reset(self):
        self.score = 0
        self.lives = 3
        self.paddle_x = WIDTH // 2
        self.ball_x = WIDTH // 2
        self.ball_y = HEIGHT // 2
        self.ball_dx = 240
        self.ball_dy = -240
        self.bricks = []
        self.state = "playing"
        self._build_bricks()

    def _build_bricks(self):
        for row in range(4):
            for col in range(8):
                self.bricks.append((40 + col * 110, 90 + row * 40, 90, 24))

    def update(self, dt, keys):
        if self.state != "playing":
            return
        move = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])
        self.paddle_x += move * 420 * dt
        self.paddle_x = max(60, min(WIDTH - 60, self.paddle_x))

        self.ball_x += self.ball_dx * dt
        self.ball_y += self.ball_dy * dt

        if self.ball_x <= self.ball_radius or self.ball_x >= WIDTH - self.ball_radius:
            self.ball_dx *= -1
        if self.ball_y <= self.ball_radius:
            self.ball_dy *= -1

        paddle_left = self.paddle_x - self.paddle_w // 2
        paddle_right = self.paddle_x + self.paddle_w // 2
        if self.ball_y + self.ball_radius >= HEIGHT - 40 and paddle_left <= self.ball_x <= paddle_right:
            self.ball_y = HEIGHT - 40 - self.ball_radius
            self.ball_dy *= -1
            self.ball_dx += (self.ball_x - self.paddle_x) * 0.06
        elif self.ball_y - self.ball_radius > HEIGHT:
            self.lives -= 1
            self.ball_x = WIDTH // 2
            self.ball_y = HEIGHT // 2
            self.ball_dx = 240
            self.ball_dy = -240

        for brick in list(self.bricks):
            bx, by, bw, bh = brick
            if bx <= self.ball_x <= bx + bw and by <= self.ball_y <= by + bh:
                self.bricks.remove(brick)
                self.score += 10
                self.ball_dy *= -1
                break

        if self.lives <= 0:
            self.state = "game_over"
        elif not self.bricks:
            self.state = "won"

    def draw(self, screen, fonts):
        screen.fill(BG_COLOR)
        pygame.draw.rect(screen, (15, 24, 45), (0, 0, WIDTH, HEIGHT), border_radius=24)
        pygame.draw.rect(screen, (24, 38, 73), (26, 26, WIDTH - 52, HEIGHT - 52), border_radius=22)
        for brick in self.bricks:
            bx, by, bw, bh = brick
            pygame.draw.rect(screen, ACCENT_COLOR, (bx, by, bw, bh), border_radius=8)

        pygame.draw.rect(screen, PLAYER_COLOR, (self.paddle_x - self.paddle_w // 2, HEIGHT - 40, self.paddle_w, self.paddle_h), border_radius=8)
        pygame.draw.circle(screen, PICKUP_COLOR, (int(self.ball_x), int(self.ball_y)), self.ball_radius)
        score_text = fonts["font"].render(f"Score: {self.score}", True, TEXT_COLOR)
        lives_text = fonts["font"].render(f"Lives: {self.lives}", True, (255, 184, 92))
        screen.blit(score_text, (28, 24))
        screen.blit(lives_text, (28, 58))
        hint_text = fonts["small_font"].render("Use A/D or arrows to move", True, (180, 195, 235))
        screen.blit(hint_text, (28, HEIGHT - 38))

        if self.state != "playing":
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 170))
            screen.blit(overlay, (0, 0))
            title = fonts["title_font"].render("You cleared the board" if self.state == "won" else "Game over", True, TEXT_COLOR)
            score = fonts["font"].render(f"Final score: {self.score}", True, ACCENT_COLOR)
            hint = fonts["font"].render("Press Enter to replay or Esc for menu", True, TEXT_COLOR)
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 80))
            screen.blit(score, (WIDTH // 2 - score.get_width() // 2, HEIGHT // 2 - 10))
            screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 2 + 40))


class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 90
        self.radius = 20
        self.speed = 320

    def update(self, dt, keys):
        move_x = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])
        move_y = int(keys[pygame.K_DOWN] or keys[pygame.K_s]) - int(keys[pygame.K_UP] or keys[pygame.K_w])
        if move_x != 0 and move_y != 0:
            scale = 1 / math.sqrt(2)
            move_x *= scale
            move_y *= scale
        self.x += move_x * self.speed * dt
        self.y += move_y * self.speed * dt
        self.x = max(self.radius, min(WIDTH - self.radius, self.x))
        self.y = max(self.radius, min(HEIGHT - self.radius, self.y))

    def draw(self, screen):
        pygame.draw.circle(screen, PLAYER_COLOR, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, ACCENT_COLOR, (int(self.x), int(self.y)), self.radius - 7)


class Enemy:
    def __init__(self):
        self.x = random.randint(30, WIDTH - 30)
        self.y = -random.randint(20, 120)
        self.radius = random.randint(14, 24)
        self.speed = random.uniform(180, 320)
        self.drift = random.uniform(-120, 120)

    def update(self, dt):
        self.y += self.speed * dt
        self.x += self.drift * dt
        if self.x < self.radius:
            self.x = self.radius
            self.drift *= -1
        if self.x > WIDTH - self.radius:
            self.x = WIDTH - self.radius
            self.drift *= -1

    def draw(self, screen):
        pygame.draw.circle(screen, ENEMY_COLOR, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, (255, 162, 162), (int(self.x), int(self.y)), self.radius - 7)


class Pickup:
    def __init__(self):
        self.x = random.randint(30, WIDTH - 30)
        self.y = -random.randint(40, 140)
        self.radius = 12
        self.speed = random.uniform(140, 240)

    def update(self, dt):
        self.y += self.speed * dt

    def draw(self, screen):
        pygame.draw.circle(screen, PICKUP_COLOR, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, (255, 240, 180), (int(self.x), int(self.y)), self.radius - 4)


class GameApp:
    def __init__(self, headless=False):
        self.headless = headless
        self.running = True
        self.current_game = None
        self.current_index = None
        self.games = [NovaDriftGame, StarCollectorGame, BrickBreakerGame]
        pygame.init()
        self.font = pygame.font.SysFont("Segoe UI", 28)
        self.title_font = pygame.font.SysFont("Segoe UI", 54, bold=True)
        self.small_font = pygame.font.SysFont("Segoe UI", 20)
        self.clock = pygame.time.Clock()
        self.screen = None
        self.frame_count = 0

    def start(self):
        if self.headless:
            os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
        if not self.headless:
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
            pygame.display.set_caption("NovaPlay Arcade")
        else:
            self.screen = pygame.Surface((WIDTH, HEIGHT))
        self.main_loop()

    def main_loop(self):
        while self.running:
            dt = min(self.clock.tick(FPS) / 1000.0, 0.03)
            self.handle_events()
            self.update(dt)
            self.draw()
            self.frame_count += 1
            if self.headless and self.frame_count >= 120:
                break
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if self.current_game is None:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                        self.start_game(event.key - pygame.K_1)
                else:
                    if event.key == pygame.K_ESCAPE:
                        self.current_game = None
                    elif event.key == pygame.K_RETURN and self.current_game.state != "playing":
                        self.current_game.reset()

    def update(self, dt):
        keys = pygame.key.get_pressed()
        if self.current_game is not None:
            self.current_game.update(dt, keys)

    def draw(self):
        if self.current_game is None:
            self.draw_menu()
        else:
            self.current_game.draw(self.screen, {"font": self.font, "title_font": self.title_font, "small_font": self.small_font})
        if not self.headless:
            pygame.display.flip()

    def start_game(self, index):
        self.current_index = index
        game_class = self.games[index]
        self.current_game = game_class()
        self.current_game.reset()

    def draw_menu(self):
        self.screen.fill(BG_COLOR)
        pygame.draw.rect(self.screen, (15, 24, 45), (0, 0, WIDTH, HEIGHT), border_radius=24)
        pygame.draw.rect(self.screen, (24, 38, 73), (26, 26, WIDTH - 52, HEIGHT - 52), border_radius=22)

        title = self.title_font.render("NovaPlay Arcade", True, TEXT_COLOR)
        subtitle = self.small_font.render("Pick a game and jump in.", True, (180, 195, 235))
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 90))
        self.screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 150))

        for idx, game_class in enumerate(self.games):
            game = game_class()
            rect = pygame.Rect(110 + (idx * 240), 220, 180, 180)
            pygame.draw.rect(self.screen, PANEL_COLOR, rect, border_radius=22)
            label = self.font.render(f"{idx + 1}", True, ACCENT_COLOR)
            name = self.font.render(game.title, True, TEXT_COLOR)
            desc = self.small_font.render(game.description, True, (180, 195, 235))
            self.screen.blit(label, (rect.x + 18, rect.y + 18))
            self.screen.blit(name, (rect.x + 18, rect.y + 60))
            self.screen.blit(desc, (rect.x + 18, rect.y + 95))

        footer = self.small_font.render("Press 1, 2, or 3 to start. Esc to quit.", True, (180, 195, 235))
        self.screen.blit(footer, (WIDTH // 2 - footer.get_width() // 2, HEIGHT - 70))


def main():
    headless = len(sys.argv) > 1 and sys.argv[1] == "--headless"
    app = GameApp(headless=headless)
    app.start()


if __name__ == "__main__":
    main()
