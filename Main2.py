import pygame
import random
import time

pygame.init()

# Set up fullscreen window
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = screen.get_size()

# Load images
player_img = pygame.transform.scale(pygame.image.load("JetFighter.png"), (80, 80))
enemy_img = pygame.transform.scale(pygame.image.load("Enemy.png"), (120, 120))
bullet_img = pygame.transform.scale(pygame.image.load("Bullet2.png"), (60, 40))
powerup_img = pygame.transform.scale(pygame.image.load("PowerUp.png"), (90, 90))
boss_img = pygame.transform.scale(pygame.image.load("Boss.png"), (200, 200)) 
backgroundimg = pygame.transform.scale(pygame.image.load("Sky.jpg"), (width, height)) # Full Screen

# Load sound effects
shoot_sound = pygame.mixer.Sound("Drums.mp3")
reward_sound = pygame.mixer.Sound("Drums.mp3")
powerup_sound = pygame.mixer.Sound("Drums.mp3")
explosion_sound = pygame.mixer.Sound("Drums.mp3")
combo_sound = pygame.mixer.Sound("Drums.mp3")
triple_sound = pygame.mixer.Sound("Drums.mp3")
quad_sound = pygame.mixer.Sound("Drums.mp3")
unstoppable_sound = pygame.mixer.Sound("Drums.mp3")

# Fonts
font = pygame.font.SysFont(None, 40)
big_font = pygame.font.SysFont(None, 80)

# High score functions
def load_high_score():
    try:
        with open("highscore.txt", "r") as file:
            return int(file.read())
    except:
        return 0

def save_high_score(score):
    with open("highscore.txt", "w") as file:
        file.write(str(score))

# Function to draw text
def show_text(text, x, y, color=(255, 255, 255), font_obj=font):
    image = font_obj.render(text, True, color)
    screen.blit(image, (x, y))

# Main game function
def run_game():
    # Play gameplay background music
    pygame.mixer.music.load("Drums.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.3)

    # Game variables
    player_x = width // 2
    player_y = height - 100
    player_speed = 10
    bullets = []
    enemies = []
    powerups = []
    score = 0
    high_score = load_high_score()
    level = 1
    enemy_speed = 2
    shield = False
    double_shot = False
    boss_active = False
    boss_health = 20
    combo = 0
    combo_active = False
    combo_label = ""
    combo_show_time = 0
    combo_timer = 0
    start_time = time.time()
    paused = False
    clock = pygame.time.Clock()
    
# Spawn Function
    def spawn_enemy():
        x = random.randint(0, width - 50)
        y = random.randint(-200, -50) 
        enemies.append(pygame.Rect(x, y, 50, 50)) 

    def spawn_powerup():
        x = random.randint(0, width - 30)
        y = random.randint(-300, -100)
        powerups.append(pygame.Rect(x, y, 30, 30))

# Main Loop
    running = True
    while running:
        screen.blit(backgroundimg, (0,0))

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                paused = not paused
                if paused:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not paused:
                bullets.append(pygame.Rect(player_x + 25, player_y, 10, 20))
                if double_shot:
                    bullets.append(pygame.Rect(player_x + 5, player_y, 10, 20))
                shoot_sound.play()

        if paused:
            show_text("Paused", width // 2 - 100, height // 2, (255, 255, 255), big_font)
            pygame.display.flip()
            clock.tick(60)
            continue
 # Player Movement
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player_x > 0:
            player_x -= player_speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player_x < width - 60:
            player_x += player_speed
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and player_y > 0:
            player_y -= player_speed
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player_y < height - 60:
            player_y += player_speed

        player_rect = pygame.Rect(player_x, player_y, 60, 60)
        screen.blit(player_img, player_rect)

        for bullet in bullets[:]:
            bullet.y -= 10
            screen.blit(bullet_img, bullet)
            if bullet.y < 0:
                bullets.remove(bullet)

                # Enemies 

        if len(enemies) < 5 + level and not boss_active: 
            spawn_enemy() 
        for enemy in enemies[:]: 
            enemy.y += enemy_speed 
            screen.blit(enemy_img, enemy) 
            if enemy.y > height: 
                enemies.remove(enemy) 
            if enemy.colliderect(player_rect):
                if shield: 
                    shield = False 
                    enemies.remove(enemy) 
                else: 
                    if score > high_score: 
                        high_score = score
                        save_high_score(high_score) 
                    score, level, enemy_speed = 0, 1, 2 
                    bullets.clear()
                    enemies.clear() 
                    powerups.clear()
                    boss_active = False  
                    start_time = time.time() 
# Power Ups
        if random.randint(1, 300) == 1:
            spawn_powerup()
        for p in powerups[:]:
            p.y += 3
            screen.blit(powerup_img, p)
            if p.colliderect(player_rect):
                powerup_sound.play()
                if random.choice([True, False]):
                    shield = True
                else:
                    double_shot = True
                    combo_timer = pygame.time.get_ticks()
                powerups.remove(p)

            # Boss Appereance 
        if score > 0 and score % 30 == 0 and not boss_active: 
            boss_rect = pygame.Rect(width // 2 - 50, -100, 100, 100)
            boss_active = True
            boss_health = 20

# Boss Behavior

        if boss_active:
            boss_rect.y += 2
            screen.blit(boss_img, boss_rect)
            if boss_rect.colliderect(player_rect):
                explosion_sound.play()
                if score > high_score:
                    high_score = score
                    save_high_score(high_score)
                score, level, enemy_speed = 0, 1, 2
                bullets.clear()
                enemies.clear()
                boss_active = False
            for bullet in bullets[:]:
                if boss_rect.colliderect(bullet):
                    boss_health -= 1
                    bullets.remove(bullet)
                    if boss_health <= 0:
                        reward_sound.play()
                        score += 10
                        boss_active = False

# Bullet Collisin for enemys 

        for bullet in bullets[:]: 
            for enemy in enemies[:]: 
                if bullet.colliderect(enemy): 
                    bullets.remove(bullet) 
                    enemies.remove(enemy) 
                    explosion_sound.play() 
                    score += 1 
                    combo += 1 
                    if combo == 3:
                        combo_label = "Combo x2!" 
                        score += 1
                        combo_sound.play()
                    elif combo == 4:
                        combo_label = "Triple Combo!!!"
                        score += 2
                        triple_sound.play()
                    elif combo == 5:
                        combo_label = "Quad Combo!!!"
                        score += 3
                        quad_sound.play()
                    elif combo >= 6:
                        combo_label = "!!!UNSTOPPABLE!!!"
                        score += 5 
                        unstoppable_sound.play()
                    if combo >= 3:
                        combo_active = True
                        combo_show_time = pygame.time.get_ticks()
                    break 

        # Power Up Timers

        if double_shot and pygame.time.get_ticks() - combo_timer > 5000:
            double_shot = False
        if combo_active:
            if pygame.time.get_ticks() - combo_show_time < 2500:
                show_text(combo_label, player_x, player_y - 30)
            else:
                combo_active = False
                combo = 0

         # Difficulty Scaling

        if score > 0 and score % 10 == 0: 
            level = score // 10 + 1 
            enemy_speed = 2 + level 

        # HUD

        elapsed = int(time.time() - start_time) 
        show_text(f"Score: {score}", 10, 10)
        show_text(f"Time: {elapsed}s", 10, 50)
        show_text(f"High Score: {high_score}", 10, 90)
        if shield: 
            show_text("Shield ON", 10, 130)
        if double_shot: 
            show_text("Double Shot", 10, 170)

        pygame.display.flip() 
        clock.tick(60) 
    
# Start Menu with Music 
pygame.mixer.music.load("Pufino_Rush_Metal.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)

in_menu = True
while in_menu:
    screen.fill((20, 20, 40))
    show_text("Welcome, Player.", width // 2 - 150, height // 2 - 150, (100, 255, 200), font)
    show_text("Title: Combo Rush", width // 2 - 180, height // 2 - 100, (255, 255, 255), big_font)
    show_text("Press ENTER to Begin Your Mission", width // 2 - 200, height // 2 - 30, (200, 200, 200))
    show_text("Move: WASD / Arrows | Shoot: Right Click | Pause: P", width // 2 - 300, height // 2 + 30, (180, 180, 180))
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            in_menu = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            in_menu = False
            pygame.mixer.music.stop()
            run_game()

pygame.quit()
