import pygame
import random



# Initialize pygame
pygame.init()

# Screen dimensions and settings
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("caffine")





# Images
bg = pygame.transform.scale(pygame.image.load("images/bg.png").convert_alpha(), (SCREEN_WIDTH, SCREEN_HEIGHT))
platform_image = pygame.image.load("images/platform.png").convert_alpha()
coin_img = pygame.image.load("images/coin.png").convert_alpha()
enemy_img = pygame.image.load("images/enemy.png").convert_alpha()
idle_sprite_sheet = pygame.image.load("images/idle_animation.png").convert_alpha()
bat_flight = pygame.image.load("images/bat_flight.png")
portal = pygame.image.load("images/portal.png")
golem_walk = pygame.image.load("images/golem_walk.png")


# global variables
FPS = 60
GRAVITY = 0.5
RED = (255, 0, 0)
GREEN = (0, 255, 0)
font = pygame.font.SysFont('Arial', 30)


player_score = 0

#define  font
font = pygame.font.SysFont("arialblack", 20)

#define colors
TEXT_COL = (255, 255, 255)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))








#Classes 
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        super().__init__()
        self.image = pygame.transform.scale(platform_image, (115, 15))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y



class Door(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.image.load("images/portal.png")
        self.image = pygame.transform.scale(self.image,(75, 75))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Bossdoor(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.image.load("images/bossportal.png")
        self.image = pygame.transform.scale(self.image,(50, 75))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class screenfade():
    def __init__(self, direction, color, speed):
        self.direction = direction
        self.color = color
        self.speed = speed
        self.fade_counter = 0
    def fade(self):
        fade_complte = False
        self.fade_counter += self.speed
        pygame.draw.rect(screen, self.color, (0, 0, SCREEN_WIDTH, 0 + self.fade_counter))
        if self.fade_counter >= SCREEN_WIDTH:
            fade_complte = True
        return fade_complte


deathfade = screenfade(10, "BLACK", 4)
        


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, speed, scale, sprite_sheet, animation_type="walk", num_frames=8):
        super().__init__()
        self.flip = False
        self.animation_type = animation_type
        self.animations = self.load_animation(sprite_sheet, scale, num_frames)
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.animation_speed = 400  # Milliseconds per frame

        self.image = self.animations[self.current_frame]
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.direction = 1

        # Adjust hitbox for the Golem
        self.hitbox = self.rect.inflate(70, 10)  # Slightly smaller than the sprite's rectangle

    @staticmethod
    def load_animation(sheet, scale, num_frames):
        frames = []
        frame_width = sheet.get_width() // 7
        frame_height = sheet.get_height()
        for i in range(7):
            frame = sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            frames.append(pygame.transform.scale(frame, (frame_width * scale, frame_height * scale)))
        return frames

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.animations)
            self.image = self.animations[self.current_frame]

    def move(self):
        self.rect.x += self.speed * self.direction
        self.hitbox.topleft = self.rect.topleft

        # Check collision with the player
        if self.rect.colliderect(player.rect):
            current_time = pygame.time.get_ticks()
            if current_time - player.last_hit_time > player.hit_cooldown:  # Check if cooldown has passed
                player.health -= 10
                player.last_hit_time = current_time  # Reset the cooldown timer

        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.direction *= -1
            self.flip = not self.flip

    def draw(self):
        self.animate()
        pygame.draw.rect(screen, RED, self.hitbox, 2)  # Visualize the hitbox
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect.topleft)











class Enemy2(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, speed, scale, sprite_sheet, animation_type="fly", num_frames=8):
        super().__init__()
        self.flip = False
        self.animation_type = animation_type
        self.animations = self.load_animation(sprite_sheet, scale, num_frames)
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.animation_speed = 100  # Faster for a flying creature

        self.image = self.animations[self.current_frame]
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.direction = 1

        # Adjust hitbox for the Bat
        self.hitbox = self.rect.inflate(50, 50)  # Smaller hitbox, focusing on the body

    @staticmethod
    def load_animation(sheet, scale, num_frames):
        frames = []
        frame_width = sheet.get_width() // num_frames
        frame_height = sheet.get_height()
        for i in range(num_frames):
            frame = sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            frames.append(pygame.transform.scale(frame, (frame_width * scale, frame_height * scale)))
        return frames

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.animations)
            self.image = self.animations[self.current_frame]

    def move(self):
        self.rect.x += self.speed * self.direction
        self.hitbox.topleft = self.rect.topleft

        # Check collision with the player
        if self.rect.colliderect(player.rect):
            current_time = pygame.time.get_ticks()
            if current_time - player.last_hit_time > player.hit_cooldown:  # Check if cooldown has passed
                player.health -= 10
                player.last_hit_time = current_time  # Reset the cooldown timer

        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.direction *= -1
            self.flip = not self.flip

    def draw(self):
        self.animate()
        pygame.draw.rect(screen, GREEN, self.hitbox, 2)  # Visualize the hitbox
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect.topleft)






class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, player_score):
        super().__init__()
        self.speed = 2
        self.health = 100 + player_score // 10  # Boss health scales with player score
        self.strength = 10 + player_score // 10  # Boss strength scales with player score
        self.direction = 1
        self.flip = False

        
        self.image = pygame.image.load("images/tempplayer.png")  # Placeholder boss sprite
        self.image = pygame.transform.scale(self.image, (100 * scale, 150 * scale))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hitbox = self.rect.inflate(10, 10)

    def move(self):
        self.rect.x += self.speed * self.direction
        self.hitbox.topleft = self.rect.topleft
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.direction *= -1
            self.flip = not self.flip

    def attack(self, player):
        # Simple attack that decreases player health
        if self.rect.colliderect(player.rect):
            player.health -= self.strength

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect.topleft)
        pygame.draw.rect(screen, RED, self.hitbox, 2) 

def load_frames(sprite_sheet, frame_width, frame_height):
    frames = []
    sheet_width, sheet_height = sprite_sheet.get_size()
    for y in range(0, sheet_height, frame_height):
        for x in range(0, sheet_width, frame_width):
            frame = sprite_sheet.subsurface(pygame.Rect(x, y, frame_width, frame_height))
            frames.append(frame)
    return frames




class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed):
        super().__init__()
        self.speed = speed
        self.direction = 1
        self.flip = False
        self.jump = False
        self.width = 80
        self.height = 100
        self.vel_y = 0
        self.health = 200
        self.idle_animation = self.load_idle_animation(idle_sprite_sheet, scale)
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.animation_speed = 100
        self.last_hit_time = 0  # Tracks the last time the player was hit
        self.hit_cooldown = 2000  # 2 seconds cooldown in milliseconds

        self.image = self.idle_animation[self.current_frame]
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)

    @staticmethod
    def load_idle_animation(sheet, scale):
        frames = []
        frame_width = sheet.get_width() // 15
        frame_height = sheet.get_height()
        for i in range(15):
            frame = sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            frames.append(pygame.transform.scale(frame, (frame_width * scale, frame_height * scale)))
        return frames
    def take_dmg(self, damage):
        if self.health <= 0:
                self.is_dead = True

    def animate_idle(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.idle_animation)
            self.image = self.idle_animation[self.current_frame]
    

    def move(self, moving_left, moving_right):
        dx = 0
        dy = 0
        if player.health > 0:


            if moving_left:
                dx = -self.speed
                self.flip = True
                self.direction = -1
            if moving_right:
                dx = self.speed
                self.flip = False
                self.direction = 1

            if self.jump:
                self.vel_y = -15
                self.jump = False

        self.vel_y += GRAVITY
        dy += self.vel_y
        dy = min(dy, 10)

        for platform in platform_group:
            if platform.rect.colliderect(self.rect.move(0, dy)):
                if self.vel_y > 0:
                    self.rect.bottom = platform.rect.top
                    dy = 0
                    self.vel_y = 0

        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rect.right

        if self.rect.bottom + dy > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            dy = 0
            self.vel_y = 0

        self.rect.x += dx
        self.rect.y += dy

    def attack(self):
        global player_score 
        
        attack_rect = pygame.Rect(self.rect.centerx, self.rect.y, self.rect.width, self.rect.height)

        # Check for collisions with all enemies in the enemy group
        collided_enemies = pygame.sprite.spritecollide(self, enemy_group, False, collided=lambda player, enemy: attack_rect.colliderect(enemy.hitbox))

        for enemy in collided_enemies:
            print(f"Hit enemy at {enemy.hitbox}!")
            enemy.kill()  # Remove the enemy from the group
            player_score += 10
            return player_score
            

           

    # Draw the attack area for debugging purposes
        pygame.draw.rect(screen, GREEN, attack_rect, 2)
        

        pygame.draw.rect(screen, GREEN, attack_rect, 2)  

    def draw(self):
        self.animate_idle()
        screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 50, self.rect.y - 45))
        
        pygame.draw.rect(screen, RED, self.rect, 2)


# Create groups
platform_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
enemy_group2 = pygame.sprite.Group()

# Create game objects
for _ in range(5):
    platform = Platform(random.randint(0, SCREEN_WIDTH - 200), random.randint(50, SCREEN_HEIGHT - 50), random.randint(100, 200))
    platform_group.add(platform)

setPlatform = Platform(300, 300, 300)
platform_group.add(setPlatform)

player = Player(200, 400, scale=3, speed=3)



enemy1 = Enemy2(500, 400, 50, 35, speed=1, scale=2, sprite_sheet= bat_flight)
enemy2 = Enemy2(600, 400, 50, 35, speed=1, scale=2, sprite_sheet= bat_flight)
enemy3 = Enemy2(300, 400, 50, 35, speed=1, scale=2, sprite_sheet= bat_flight)

enemy6 = Enemy(400, 500, 120, 150, speed=2, scale=3, sprite_sheet= golem_walk)
enemy_group.add(enemy6)


# Main game loop


clock = pygame.time.Clock()
run = True
moving_left = False
moving_right = False
attack = False

#door
door = Door(SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100, 50, 100)  # Placing the door at the bottom-right
door_group = pygame.sprite.Group()
door_group.add(door)

boss_door = Bossdoor(SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100, 50, 100)  # Placing the door at the bottom-right
boss_door_group = pygame.sprite.Group()
boss_door_group.add(boss_door)











player_run = pygame.image.load("images/player_run.png")

stage = 1
while run:
    clock.tick(FPS)
    screen.blit(bg,(0, 0))
    


    

    platform_group.draw(screen)
    player.draw()
    player.move(moving_left, moving_right)

    

    draw_text("Player Score: " + str(player_score), font, TEXT_COL, 750, 35)
    door_group.draw(screen)
    
    
    
        
    for enemy in enemy_group:
        enemy.move()
        enemy.draw()
    if player.health <= 0:
            deathfade.fade()
            
        


    if attack:
        player.attack()

    pygame.draw.rect(screen, RED, (35, 35, 200, 15))
    pygame.draw.rect(screen, GREEN, (35, 35, player.health, 15))




#next level door
    if pygame.sprite.collide_rect(player, door):  # Check if the player collides with the current door
        stage += 1
        player.rect.x = 50  
        player.rect.y = 200 

        enemy_group.empty()  # Empty out the enemy group for the new stage

        enemy1 = Enemy2(500, 400, 60, 60, speed=2, scale=2, sprite_sheet=bat_flight)
        enemy2.move()
        enemy2.draw()
        enemy_group.add(enemy1, enemy2)
        pygame.display.update()

        print("Next level!")

    if stage == 2:
        door_group.remove(door)  # Remove the door from the group
        door.kill()  # Remove the door sprite from all groups and stop it from drawing/interacting
        bg = pygame.image.load("images/bg_2.png")  # Load the new background for stage 2
        
        # Add boss door after the stage transition
        boss_door = Bossdoor(500, 200, 200, 200)  # Assuming BossDoor is the class for the boss door
        door_group.add(boss_door)  # Add the boss door to the door group
        
        
    if pygame.sprite.collide_rect(player, boss_door):
        stage += 1
        
        
    if stage == 3 :
        door_group.remove(boss_door)  # Remove the door from the group
        boss_door.kill()
        bg = pygame.image.load("images/bg_3.png")
        bg = pygame.transform.scale(bg,(1000, 650))
        # Inside the main game loop, add these changes:

        # Boss Door
        if pygame.sprite.collide_rect(player, boss_door):  # Check if player collides with the boss door
            # Spawn the boss
              # Only spawn the boss once
                boss = Boss(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, scale=2, player_score=player_score)
                boss_group = pygame.sprite.Group()
                boss_group.add(boss)
                print("Boss Fight Started!")

        # Boss Fight
       
        boss_group.update()  # Update the boss
        boss_group.draw(screen)  # Draw the boss
        boss.move()  # Move the boss
        boss.attack(player)  # Boss attacks the player if close
        if player.health <= 0:
            print("Game Over!")
            # Handle game over logic here, like transitioning to death screen

# Draw player health and score as usual
            draw_text("Player Score: " + str(player_score), font, TEXT_COL, 750, 35)

        
            enemy2.move()
            enemy2.draw()
        
       
        
            pygame.display.update()
            print("Boss door triggered!")
        
        
        

            

            
    

    
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_f:
                attack = True
            if event.key == pygame.K_SPACE:
                player.jump = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_f:
                attack = False

pygame.quit()  