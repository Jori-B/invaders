# Based on https://www.youtube.com/watch?v=Q-__8Xw9KTM&ab_channel=UnityCoin
import pygame
import os
import time
import random
import utility

# initialize font usage
pygame.font.init()
pygame.init()

# How big is our window going to be, dimensions depend on the screen preventing windows to be too big
infoObject = pygame.display.Info()
WIDTH, HEIGHT = infoObject.current_w-20, infoObject.current_h-40
# WIDTH, HEIGHT = 1366, 768
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multiplication Invaders")

# Load images
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

# Player player
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

# Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# Background
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background_black.png")), (WIDTH, HEIGHT))

# Answer Box
ANSWER_BOX= pygame.image.load(os.path.join("assets", "Answer_button.png"))

class Laser:
    def __init__(self, x, y, img):
        # TODO: These coordinates need to be placed in the center of the space ship
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, velocity):
        self.y += velocity

    def off_screen(self, height):
        # Return a false value when the y position is higher than the height of screen (starts at top with 0)
        return not(self.y < height and self.y >= 0)

    def collision(self, obj):
        # Is an object colliding with the object that called the function
        return collide(self, obj)

# Abstract class (no usage only inheriting from it). Namely, enemy and player player are both similar
class Ship:
    # Half a second since FPS is 60
    COOLDOWN = 30

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.health = health
        # Cool down is so that the user can't just spam the laser
        self.cool_down_counter = 0

    def draw(self, window):
        # Draw something red on the window, where it's going to be and how wide , 0 means filling in
        # pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, 50, 50), 0)
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    # Is used for player and the enemy, however in player it checks wheter it hit an enemy
    def move_lasers(self, velocity, obj):
        # When you move the lasers check if cooldown is finished
        self.cooldown()
        for laser in self.lasers:
            laser.move(velocity)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                # Every time player is hit 10 hitpoints are removed
                obj.health -= 10
                # After a hit the laser needs to be removed again
                self.lasers.remove(laser)


    # Handles counting the cooldown, before a laser can be shot again
    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        # Only shoot laser if the cooldown counter is 0
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 10, self.y - 20, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


# Inherits from player (so all the things from player are also in player)
class Player(Ship):
    def __init__(self, x, y, health=100):
        # Use ship's initialization method
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        # Mask for pixel perfect collision instead of square collision box
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    # Checks whether laser hit an enemy
    def move_lasers(self, velocity, objs, window):
        # When you move the lasers check if cooldown is finished
        self.cooldown()
        # For each laser that the player has
        for laser in self.lasers:
            laser.move(velocity)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                # For each enemy in the objects list if it collides with the laser remove it
                for obj in objs:
                    if laser.collision(obj):
                        # TODO: Add multplication showing and check if answr is correct or wrong
                        main_font = pygame.font.SysFont("notosansmonocjkkr", 30)
                        answer=""
                        answer_label = main_font.render(f"Answer: {answer}", 1, (255, 255, 255))
                        string=""
                        #pygame.draw.rect(WINDOW,(0,0,255),(WIDTH/2 - answer_label.get_width()/2, HEIGHT/2 - answer_label.get_height()/2,answer_label.get_width()+50,answer_label.get_height()))
                        window.blit(ANSWER_BOX, (WIDTH/2 - ANSWER_BOX.get_width()/2, HEIGHT/2 - ANSWER_BOX.get_height()/2,ANSWER_BOX.get_width()+50,ANSWER_BOX.get_height()))        
                        window.blit(answer_label, (WIDTH/2 - ANSWER_BOX.get_width()/2 +30, HEIGHT/2 - answer_label.get_height()/2))
                        pygame.display.update()
                        
                        while True:
                            event = pygame.event.poll()
                            keys = pygame.key.get_pressed()
                            
                            if event.type == pygame.KEYDOWN:
                                key = pygame.key.name(event.key)  # Returns string id of pressed key.
                                
                                if len(key) == 1:  # This covers all letters and numbers not on numpad.
                                    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                                        #if  # Include any other shift characters here.
                                        #else:
                                        string += key.upper()
                                    else:
                                        string += key
                                #elif  # Include any other characters here.
                                elif key == "backspace":
                                    string = string[:len(string) - 1]
                                elif event.key == pygame.K_RETURN:  # Finished typing.
                                    break

                                text = main_font.render(string, 1, (255, 255, 255))
                                window.blit(text, (WIDTH/2 -answer_label.get_width()/2 +40, HEIGHT/2 - answer_label.get_height()/2))
                                pygame.display.update()

                        objs.remove(obj)
                        # Make sure that the laser you want to remove actually exists in the list
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        # Red rectangle
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() + 20,
                         self.ship_img.get_width(), 10))
        # Green rectangle
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() + 20,
                         self.ship_img.get_width() * (self.health/self.max_health), 10))


class Enemy(Ship):
    # Pass a color to the color map to get the corresponding img
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER)
    }
    # Enemies also have a color attribute
    def __init__(self, x, y, color, health=100):
        # Use ship's initialization method
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    # Move the ship downward when this is called
    def move(self, velocity):
        self.y += velocity

    def shoot(self):
        # Only shoot laser if the cooldown counter is 0
        if self.cool_down_counter == 0:
            # Offset the laser x position a little so it comes from the center of the enemy ship
            laser = Laser(self.x + 15, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

def collide(obj1, obj2):
    # distance top left hand corner ojbect 2 - 1
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    # pygame function overlap determines if two imgs' masks are overlapping
    # it returns and (x,y) collision point if they are overlapping, else none
    # Convert the floating point pixels values we get from the sharp images to integers
    return obj1.mask.overlap(obj2.mask, (int(offset_x), int(offset_y))) != None

def main():
    # Dictates if while loop is going to run
    run = True
    # Amount of frames per second (checking if character is moving once every second)
    FPS = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("notosansmonocjkkr", 30)
    lost_font = pygame.font.SysFont("notosansmonocjkkr", 60)
    # If you want to know which fonts are available
    # print(pygame.font.get_fonts())

    enemies = []
    # Every level a new wave will be created of 5 enemies
    wave_length = 5
    enemy_velocity = 1

    # How fast the player can move every time you press the key a max of 5 pixels to move
    player_velocity = 5
    laser_velocity = 4

    # Define a player space ship at location
    player = Player(WIDTH / 2, HEIGHT)
    # Center the ship on screen
    player.x -= (player.get_width() / 2)
    player.y -= (player.get_height() + 50)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_window():
        # Draw the background img at coordinate: 0,0 (which is the top left)
        WINDOW.blit(BACKGROUND, (0, 0))
        # Draw text (f strings embed variables)
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))
        # Top left hand corner plus a little offset
        WINDOW.blit(lives_label, (10, 10))
        # Top light hand corner (width screen minus width of label minus 10 pixels offset
        WINDOW.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        # Draw all enemies (before you initialize the player so the player goes over them)
        for enemy in enemies:
            enemy.draw(WINDOW)
        # Draw the player
        player.draw(WINDOW)

        if lost:
            lost_label = lost_font.render("You Lost!", 1, (255, 255, 255))
            WINDOW.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, HEIGHT/2 - lost_label.get_height()/2))

        # refresh the display surface
        pygame.display.update()

    # TODO: When shooting an enemy tell the player the "explosion code" needs to be entered
    while run:
        clock.tick(FPS)

        redraw_window()
        # No more lives or health then you lost
        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1
        if lost:
            # FPS * 3 = 3 sec
            if lost_count > FPS * 3:
                run = False
            else:
                continue
        # If there are no more enemies on screen then
        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                # TODO: when enemies overlap they need to be offset
                # TODO: probably -100 is too low
                # pick random positions way up the screen for enemies to spawn in to make it look like they come in at
                # different height and Random choice from color list
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        # Check for all events (keypresses, mouseclick, etc.
        for event in pygame.event.get():
            # if the 'x' on the right top is pressed the game is quit
            if event.type == pygame.QUIT:
                # YOU COULD CHANGE THIS TO quit() to press 'x' and quit the program
                run = False
        # check and get all keyboard keys that are pressed
        keys = pygame.key.get_pressed()
        # Key to move and don't let the player move off screen
        if keys[pygame.K_LEFT] and player.x + player_velocity > 0:
            # Move to the left
            player.x -= player_velocity
        # Adding 50 for width of the player's spaceship
        if keys[pygame.K_RIGHT] and player.x + player_velocity + player.get_width() < WIDTH:
            # Move to the right
            player.x += player_velocity
        if keys[pygame.K_UP] and player.y + player_velocity > 0:
            # Move up
            player.y -= player_velocity
        if keys[pygame.K_DOWN] and player.y + player_velocity + player.get_height() < HEIGHT:
            # Move down
            player.y += player_velocity
        if keys[pygame.K_SPACE]:
            player.shoot()

        # Move the enemies downwards all the time, [:] means a copy of the list (just to be sure nothing bad happens)
        for enemy in enemies[:]:
            enemy.move(enemy_velocity)
            # Check if laser hit the player
            enemy.move_lasers(laser_velocity, player)
            # Roughly every 2 sec an enemy should shoot, randomly determined
            if random.randrange(0, 2*60) == 1:
                enemy.shoot()
            # When the player collides with the enemy the enemy is removed and player's health reduces
            elif collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)

            # If the enemy moves off screen lose a life
            if enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        # Laser velocity needs to be negative since the y value is lower upwards the screen, meaning laser will go up
        player.move_lasers(-laser_velocity, enemies,WINDOW)

def main_menu():
    title_font = pygame.font.SysFont("notosansmonocjkkr", 70)

    run = True
    while run:
        WINDOW.blit(BACKGROUND, (0, 0))
        title_label = title_font.render("Press the mouse to begin...", 1, (225, 225, 255))
        WINDOW.blit(title_label, (WIDTH/2 - title_label.get_width()/2, HEIGHT/2 - title_label.get_height()/2))
        pygame.display.update()
        for event in pygame.event.get():
            # if pressing quit 'x' then stop
            if event.type == pygame.QUIT:
                run = False
            # if press any other button then begin
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()

main_menu()
