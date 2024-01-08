import pygame
import os
import random

pygame.init()

#GLOBAL CONSTANTS:
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#LOAD IMAGES:

#DINO:
#dino run
RUNNING = [pygame.image.load(os.path.join('Assets/Dino', 'DinoRun1.png')), 
           pygame.image.load(os.path.join('Assets/Dino', 'DinoRun2.png'))]
#dino jump
JUMPING = pygame.image.load(os.path.join('Assets/Dino', 'DinoJump.png'))
#dino duck
DUCKING = [pygame.image.load(os.path.join('Assets/Dino', 'DinoDuck1.png')), 
           pygame.image.load(os.path.join('Assets/Dino', 'DinoDuck2.png'))]

#OBJECTS:
SMALL_CACTUS = [pygame.image.load(os.path.join('Assets/Cactus', 'SmallCactus1.png')), 
                pygame.image.load(os.path.join('Assets/Cactus', 'SmallCactus2.png')),
                pygame.image.load(os.path.join('Assets/Cactus', 'SmallCactus3.png'))]

LARGE_CACTUS = [pygame.image.load(os.path.join('Assets/Cactus', 'LargeCactus1.png')), 
                pygame.image.load(os.path.join('Assets/Cactus', 'LargeCactus2.png')),
                pygame.image.load(os.path.join('Assets/Cactus', 'LargeCactus3.png'))]

BIRD = [pygame.image.load(os.path.join('Assets/Bird', 'Bird1.png')),
        pygame.image.load(os.path.join('Assets/Bird', 'Bird2.png'))]

CLOUD = pygame.image.load(os.path.join('Assets/Other', 'Cloud.png'))

BG = pygame.image.load(os.path.join('Assets/Other', 'Track.png'))

#DINO CLASS
class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        #default states
        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        #animation frame
        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0] #starting frame
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, user_input):
        #check the state of the dino
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        #step index, reset every 10 steps
        if self.step_index >= 10:
            self.step_index = 0

        #check for user input
        if user_input[pygame.K_UP] and not self.dino_jump: 
            #if up key pressed, but not currently jumping, set jump state to true, and others to false
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif user_input[pygame.K_DOWN] and not self.dino_jump:
            #if down key pressed, and not currently jumping, set duck to true and others to false
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or user_input[pygame.K_DOWN]): 
            #if not jumping and down not pressed, just run
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    #duck, run and jump functions
    def duck(self):
         #current run frame
        self.image = self.duck_img[self.step_index // 5]
        #get rect and set coordinates
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        #increment step index (frame)
        self.step_index += 1

    def run(self):
        #current run frame
        self.image = self.run_img[self.step_index // 5]
        #get rect and set coordinates
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        #increment step index (frame)
        self.step_index += 1


    def jump(self):
        self.image = self.jump_img
        if self.dino_jump: #if jumping is True
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8 #decrement jump_vel to make dino come back down
        if self.jump_vel < - self.JUMP_VEL: #to stop dino from falling through the floor
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    #draw function
    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed #moves cloud from left to right
        if self.x < -self.width: #reset cloud if off screen
            self.x = SCREEN_WIDTH + random.randint(800, 1000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))

class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0,2)
        super().__init__(image, self.type)
        self.rect.y = 325

class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0,2)
        super().__init__(image, self.type)
        self.rect.y = 300

class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1

#main function
def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock() 
    #create player by declaring instance of class 'Dinosaur'
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 14
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    death_count = 0

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1
       

        text = font.render('Points: ' + str(points), True, (0,0,0))
        text_rect = text.get_rect()
        text_rect.center = (1000, 40)
        SCREEN.blit(text, text_rect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width: #makes background loop by spawning new image if current image leaves screen
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    #while 'Game Active' loop. Variable called 'run' because thats what the game is about really lol XP
    while run:
        #create possibility to quit when 'x' on window is pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
            
                run = False
        
        #fill screen with white
        SCREEN.fill((255,255,255))

        #add user input
        user_input = pygame.key.get_pressed()

        #draw and update functions
        player.draw(SCREEN)
        player.update(user_input)


        #if the list of obstacles is empty, append one of the obstacles
        if len(obstacles) == 0:
            if random.randint(0,2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0,2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0,2) == 2:
                obstacles.append(Bird(BIRD))

        #draw them
        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            #collision detection
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(200)
                death_count += 1
                menu(death_count)


        background()

        cloud.draw(SCREEN)
        cloud.update()

        score()

        #timing and display update
        clock.tick(30) #30 fps
        pygame.display.update()

def menu(death_count):
    global points
    run = True
    while run:    
        #fill screen with white
        SCREEN.fill((255,255,255))
        font = pygame.font.Font('freesansbold.ttf', 30)
        if death_count == 0:
            text = font.render('Press any Key to Start :)', True, (0,0,0))
        elif death_count > 0:
            text = font.render('Press any Key to Start :)', True, (0,0,0))
            score = font.render('Your Score: ' + str(points), True, (0,0,0))
            score_rect = score.get_rect()
            score_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, score_rect)
        text_rect = text.get_rect()
        text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, text_rect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                main()
        
    
menu(death_count = 0)
            
