import pygame
import random
import sys
import math

# Initialize Pygame
pygame.init()

# Game Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
ORANGE = (255, 165, 0)
BROWN = (139, 69, 19)
SILVER = (192, 192, 192)
GOLD = (255, 215, 0)
CYAN = (0, 255, 255)
PURPLE = (128, 0, 128)

class Car:
    def __init__(self, x, y, color, car_type='player'):
        self.x = x
        self.y = y
        self.color = color
        self.car_type = car_type
        self.width = 50
        self.height = 90
        self.vel = 5
        self.image = self.create_car_image()
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
    
    def create_car_image(self):
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        if self.car_type == 'player':
            # Main body
            pygame.draw.rect(surface, self.color, (5, 20, self.width-10, self.height-25), border_radius=10)
            # Roof
            pygame.draw.rect(surface, self.color, (10, 10, self.width-20, 30), border_radius=8)
            # Windows
            pygame.draw.rect(surface, (100, 150, 200), (12, 12, self.width-24, 25), border_radius=5)
            # Wheels
            pygame.draw.circle(surface, BLACK, (10, self.height-10), 8)
            pygame.draw.circle(surface, BLACK, (self.width-10, self.height-10), 8)
            pygame.draw.circle(surface, BLACK, (10, 30), 8)
            pygame.draw.circle(surface, BLACK, (self.width-10, 30), 8)
            # Mercedes logo
            center_x = self.width // 2
            center_y = 35
            pygame.draw.circle(surface, SILVER, (center_x, center_y), 8, 2)
            for angle in [0, 120, 240]:
                rad = math.radians(angle)
                end_x = center_x + 10 * math.cos(rad)
                end_y = center_y + 10 * math.sin(rad)
                pygame.draw.line(surface, SILVER, (center_x, center_y), (end_x, end_y), 2)
        else:
            # Enemy car
            pygame.draw.rect(surface, self.color, (5, 20, self.width-10, self.height-25), border_radius=10)
            pygame.draw.rect(surface, self.color, (10, 10, self.width-20, 30), border_radius=8)
            pygame.draw.rect(surface, (50, 50, 60), (12, 12, self.width-24, 25), border_radius=5)
            pygame.draw.circle(surface, BLACK, (10, self.height-10), 8)
            pygame.draw.circle(surface, BLACK, (self.width-10, self.height-10), 8)
            pygame.draw.circle(surface, BLACK, (10, 30), 8)
            pygame.draw.circle(surface, BLACK, (self.width-10, 30), 8)
        
        return surface
    
    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 50:
            self.x -= self.vel
        if keys[pygame.K_RIGHT] and self.x < SCREEN_WIDTH - self.width - 50:
            self.x += self.vel
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.vel
        if keys[pygame.K_DOWN] and self.y < SCREEN_HEIGHT - self.height:
            self.y += self.vel
        
        self.rect.topleft = (self.x, self.y)
    
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
    
    def get_rect(self):
        return self.rect

class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 25
        self.height = 25
        self.vel = 5
        self.rotation = 0
        self.value = 20
        self.image = self.create_coin_image()
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
    
    def create_coin_image(self):
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.circle(surface, GOLD, (self.width//2, self.height//2), self.width//2)
        pygame.draw.circle(surface, (255, 200, 0), (self.width//2, self.height//2), self.width//2 - 3)
        font = pygame.font.Font(None, 18)
        text = font.render("$", True, (255, 140, 0))
        surface.blit(text, (self.width//2 - 4, self.height//2 - 8))
        return surface
    
    def move(self):
        self.y += self.vel
        self.rotation += 10
        self.rect.topleft = (self.x, self.y)
    
    def draw(self, screen):
        rotated_coin = pygame.transform.rotate(self.image, self.rotation)
        new_rect = rotated_coin.get_rect(center=self.rect.center)
        screen.blit(rotated_coin, new_rect.topleft)
    
    def off_screen(self):
        return self.y > SCREEN_HEIGHT
    
    def get_rect(self):
        return self.rect

class FuelTank:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 40
        self.vel = 5
        self.value = 30
        self.image = self.create_fuel_image()
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
    
    def create_fuel_image(self):
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(surface, RED, (5, 10, 20, 25), border_radius=3)
        pygame.draw.rect(surface, (200, 0, 0), (10, 5, 10, 10), border_radius=2)
        font = pygame.font.Font(None, 14)
        text = font.render("F", True, WHITE)
        surface.blit(text, (12, 18))
        return surface
    
    def move(self):
        self.y += self.vel
        self.rect.topleft = (self.x, self.y)
    
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
    
    def off_screen(self):
        return self.y > SCREEN_HEIGHT
    
    def get_rect(self):
        return self.rect

class Highway:
    def __init__(self):
        self.x = 80
        self.y1 = 0
        self.y2 = -SCREEN_HEIGHT
        self.width = SCREEN_WIDTH - 160
        self.scroll_speed = 5
        self.create_background()
    
    def create_background(self):
        self.background = pygame.Surface((self.width, SCREEN_HEIGHT * 2))
        self.background.fill(DARK_GRAY)
        
        # Lane markers
        lane_count = 4
        lane_width = self.width // lane_count
        for i in range(1, lane_count):
            x_pos = i * lane_width
            for y in range(0, SCREEN_HEIGHT * 2, 60):
                pygame.draw.rect(self.background, WHITE, (x_pos - 3, y, 6, 40))
        
        # Road edges
        pygame.draw.line(self.background, YELLOW, (0, 0), (0, SCREEN_HEIGHT * 2), 5)
        pygame.draw.line(self.background, YELLOW, (self.width, 0), (self.width, SCREEN_HEIGHT * 2), 5)
    
    def update(self):
        self.y1 += self.scroll_speed
        self.y2 += self.scroll_speed
        
        if self.y1 >= SCREEN_HEIGHT:
            self.y1 = -SCREEN_HEIGHT
        if self.y2 >= SCREEN_HEIGHT:
            self.y2 = -SCREEN_HEIGHT
    
    def draw(self, screen):
        screen.blit(self.background, (self.x, self.y1))
        screen.blit(self.background, (self.x, self.y2))

def show_score(screen, score, high_score, fuel, font):
    # Score panel
    pygame.draw.rect(screen, BLACK, (10, 10, 200, 100))
    score_text = font.render(f"Score: {score}", True, WHITE)
    high_score_text = font.render(f"Best: {high_score}", True, YELLOW)
    fuel_text = font.render(f"Fuel: {int(fuel)}%", True, GREEN if fuel > 30 else RED)
    
    screen.blit(score_text, (15, 15))
    screen.blit(high_score_text, (15, 45))
    screen.blit(fuel_text, (15, 75))
    
    # Fuel bar
    pygame.draw.rect(screen, RED, (15, 95, 200, 15))
    pygame.draw.rect(screen, GREEN, (15, 95, int(2 * fuel), 15))

def show_game_over(screen, score, font):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(128)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    title_font = pygame.font.Font(None, 72)
    game_over_text = title_font.render("GAME OVER!", True, RED)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    restart_text = font.render("Press SPACE to play again", True, WHITE)
    quit_text = font.render("Press ESC to quit", True, WHITE)
    
    screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - 100))
    screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, SCREEN_HEIGHT//2 - 30))
    screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 50))
    screen.blit(quit_text, (SCREEN_WIDTH//2 - quit_text.get_width()//2, SCREEN_HEIGHT//2 + 100))

def show_start_screen(screen, font):
    screen.fill(DARK_GRAY)
    
    title_font = pygame.font.Font(None, 80)
    title_text = title_font.render("MERCEDES RACER", True, SILVER)
    subtitle_text = font.render("Collect coins and fuel! Avoid red cars!", True, WHITE)
    controls_text = font.render("Controls: Arrow Keys to move | N for Nitro", True, WHITE)
    start_text = font.render("Press SPACE to Start!", True, GREEN)
    
    # Draw demo car
    demo_car = Car(SCREEN_WIDTH//2 - 25, SCREEN_HEIGHT//2, BLUE, 'player')
    demo_car.draw(screen)
    
    screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 100))
    screen.blit(subtitle_text, (SCREEN_WIDTH//2 - subtitle_text.get_width()//2, 200))
    screen.blit(controls_text, (SCREEN_WIDTH//2 - controls_text.get_width()//2, SCREEN_HEIGHT - 150))
    screen.blit(start_text, (SCREEN_WIDTH//2 - start_text.get_width()//2, SCREEN_HEIGHT - 80))
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                if event.key == pygame.K_ESCAPE:
                    return False
    return True

def main():
    # Set up display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Mercedes Racing Game")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    
    # Show start screen
    if not show_start_screen(screen, font):
        pygame.quit()
        sys.exit()
    
    # Game variables
    running = True
    game_over = False
    score = 0
    fuel = 100
    high_score = 0
    
    # Load high score
    try:
        with open("highscore.txt", "r") as f:
            high_score = int(f.read())
    except:
        high_score = 0
    
    # Create game objects
    player = Car(SCREEN_WIDTH//2 - 25, SCREEN_HEIGHT - 120, BLUE, 'player')
    highway = Highway()
    obstacles = []
    coins = []
    fuel_tanks = []
    
    # Timers
    obstacle_timer = 0
    coin_timer = 0
    fuel_timer = 0
    
    # Nitro
    nitro_active = False
    nitro_time = 0
    normal_vel = 5
    current_vel = normal_vel
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if game_over and event.key == pygame.K_SPACE:
                    # Restart game
                    game_over = False
                    score = 0
                    fuel = 100
                    player = Car(SCREEN_WIDTH//2 - 25, SCREEN_HEIGHT - 120, BLUE, 'player')
                    obstacles = []
                    coins = []
                    fuel_tanks = []
                    obstacle_timer = 0
                    coin_timer = 0
                    fuel_timer = 0
                    nitro_active = False
                    current_vel = normal_vel
                if event.key == pygame.K_ESCAPE:
                    running = False
                if not game_over and event.key == pygame.K_n and nitro_time <= 0:
                    nitro_active = True
                    nitro_time = 180  # 3 seconds
                    current_vel = 12
        
        if not game_over:
            keys = pygame.key.get_pressed()
            
            # Update player velocity
            player.vel = current_vel
            
            # Move player
            if keys[pygame.K_LEFT] and player.x > 50:
                player.x -= player.vel
            if keys[pygame.K_RIGHT] and player.x < SCREEN_WIDTH - player.width - 50:
                player.x += player.vel
            if keys[pygame.K_UP] and player.y > 0:
                player.y -= player.vel
            if keys[pygame.K_DOWN] and player.y < SCREEN_HEIGHT - player.height:
                player.y += player.vel
            
            player.rect.topleft = (player.x, player.y)
            
            # Update nitro
            if nitro_active:
                nitro_time -= 1
                if nitro_time <= 0:
                    nitro_active = False
                    current_vel = normal_vel
            
            # Fuel consumption
            if keys[pygame.K_UP] or keys[pygame.K_DOWN]:
                fuel -= 0.15
            else:
                fuel -= 0.08
            
            if fuel <= 0:
                game_over = True
                if score > high_score:
                    high_score = score
                    with open("highscore.txt", "w") as f:
                        f.write(str(high_score))
            
            # Update highway
            highway.update()
            
            # Spawn obstacles
            obstacle_timer += 1
            if obstacle_timer > random.randint(40, 80):
                enemy = Car(random.randint(highway.x + 10, highway.x + highway.width - 60), 
                           -90, RED, 'enemy')
                obstacles.append(enemy)
                obstacle_timer = 0
            
            # Spawn coins
            coin_timer += 1
            if coin_timer > random.randint(30, 60):
                coin_x = random.randint(highway.x + 20, highway.x + highway.width - 45)
                coins.append(Coin(coin_x, -25))
                coin_timer = 0
            
            # Spawn fuel tanks (in middle of road)
            fuel_timer += 1
            if fuel_timer > random.randint(150, 250):
                middle_x = highway.x + highway.width//2 - 15
                fuel_tanks.append(FuelTank(middle_x + random.randint(-40, 40), -40))
                fuel_timer = 0
            
            # Update and check obstacles
            for obstacle in obstacles[:]:
                obstacle.y += 5
                obstacle.rect.topleft = (obstacle.x, obstacle.y)
                if obstacle.y > SCREEN_HEIGHT:
                    obstacles.remove(obstacle)
                elif player.get_rect().colliderect(obstacle.get_rect()):
                    if nitro_active:
                        obstacles.remove(obstacle)
                        score += 50
                    else:
                        game_over = True
                        if score > high_score:
                            high_score = score
                            with open("highscore.txt", "w") as f:
                                f.write(str(high_score))
            
            # Update and collect coins
            for coin in coins[:]:
                coin.move()
                if coin.off_screen():
                    coins.remove(coin)
                elif player.get_rect().colliderect(coin.get_rect()):
                    coins.remove(coin)
                    score += coin.value
                    fuel += 2
                    if fuel > 100:
                        fuel = 100
            
            # Update and collect fuel tanks
            for fuel_tank in fuel_tanks[:]:
                fuel_tank.move()
                if fuel_tank.off_screen():
                    fuel_tanks.remove(fuel_tank)
                elif player.get_rect().colliderect(fuel_tank.get_rect()):
                    fuel_tanks.remove(fuel_tank)
                    fuel = min(100, fuel + fuel_tank.value)
            
            # Draw everything
            screen.fill((135, 206, 235))  # Sky blue
            highway.draw(screen)
            
            # Draw trees on sides
            for i in range(10):
                pygame.draw.rect(screen, BROWN, (30, (i * 100 + highway.y1) % (SCREEN_HEIGHT * 2), 10, 40))
                pygame.draw.circle(screen, GREEN, (35, (i * 100 + highway.y1) % (SCREEN_HEIGHT * 2)), 25)
                pygame.draw.rect(screen, BROWN, (SCREEN_WIDTH - 40, (i * 100 + highway.y1) % (SCREEN_HEIGHT * 2), 10, 40))
                pygame.draw.circle(screen, GREEN, (SCREEN_WIDTH - 35, (i * 100 + highway.y1) % (SCREEN_HEIGHT * 2)), 25)
            
            for obstacle in obstacles:
                obstacle.draw(screen)
            for coin in coins:
                coin.draw(screen)
            for fuel_tank in fuel_tanks:
                fuel_tank.draw(screen)
            player.draw(screen)
            
            # Show nitro gauge
            if nitro_active:
                pygame.draw.rect(screen, ORANGE, (SCREEN_WIDTH - 120, 10, 100, 20))
                pygame.draw.rect(screen, (255, 100, 0), (SCREEN_WIDTH - 120, 10, int(100 * nitro_time / 180), 20))
            
            show_score(screen, score, high_score, fuel, font)
            
            # Low fuel warning
            if fuel < 30:
                warning_text = font.render("LOW FUEL!", True, RED)
                screen.blit(warning_text, (SCREEN_WIDTH//2 - 50, 50))
            
            # Nitro ready indicator
            if nitro_time <= 0 and not nitro_active:
                nitro_ready = font.render("NITRO READY! Press N", True, CYAN)
                screen.blit(nitro_ready, (SCREEN_WIDTH - 200, 50))
        
        else:
            show_game_over(screen, score, font)
            show_score(screen, score, high_score, fuel, font)
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()