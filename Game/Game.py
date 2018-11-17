import pygame, random
# Let's import the Car Class

pygame.init()

GREEN = (20, 255, 140)
GREY = (210, 210, 210)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
BLACK = (0, 0, 0)

FALLSPEED = 10

OBJECTPROB = 3

SCREENWIDTH = 1200
SCREENHEIGHT = 800

clock = pygame.time.Clock()


size = (SCREENWIDTH, SCREENHEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("GOOMBA RUSH")

random.seed(None)

# Prints the score
font = pygame.font.Font("PatrickHand-Regular.ttf", 30)



# This will be a list that will contain all the sprites we intend to use in our game.
all_sprites_list = pygame.sprite.Group()


class Player(pygame.sprite.Sprite):

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self):

       # Call the parent class (Sprite) constructor
       pygame.sprite.Sprite.__init__(self)


       # Create an image of the block, and fill it with a color.
       # This could also be an image loaded from the disk.\
       self.height = 20
       self.width =20
       self.image = pygame.Surface([self.width, self.height])
       self.image.fill(RED)
       self.lane = 1
       self.lanePos = [ SCREENWIDTH / 6, SCREENWIDTH / 2, 5*(SCREENWIDTH / 6)]
       self.collide = False
       self.state = 0 #0 - run, 1 -air, -1 - ground
       self.counter = 0


       # Fetch the rectangle object that has the dimensions of the image
       # Update the position of this object by setting the values of rect.x and rect.y
       self.rect = self.image.get_rect()
       self.rect.x = self.lanePos[self.lane]
       self.rect.y = SCREENHEIGHT - 50


    def ChangeLane(self,direction):

        if(direction == 'right'):
            if(self.lane != 2):
                self.lane +=1

        elif(direction == 'left'):
            if (self.lane != 0):
                self.lane -=1

        self.rect.x = self.lanePos[self.lane]

    def Jump(self):

        self.state = 1

    def Duck(self):

        self.state = -1

    def CheckCollide(self,x,w,y,h,label):

        if(self.rect.x == x and self.state != -1*label):
            if(y+h>= self.rect.y and y+h <= self.rect.y+self.height) or (y >= self.rect.y and y <= self.rect.y+self.height):
                return True

        return False

    def update(self):
        if(self.state != 0):
            self.counter+=1
            if(self.counter >= 40):
                self.state = 0
                self.counter =0
            if(self.state == 1):
            # This means he is jumping
                self.image.fill(PURPLE)
            elif (self.state == -1):
            #This means he is ducking
                self.image.fill(GREY)

        else:
            # This means he is running
            self.image.fill(RED)

class OnGround(pygame.sprite.Sprite):

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self):

       # Call the parent class (Sprite) constructor
       pygame.sprite.Sprite.__init__(self)


       # Create an image of the block, and fill it with a color.
       # This could also be an image loaded from the disk.
       self.label = -1 #0 - run, 1 -air, -1 - ground
       self.width = 20
       self.height = 20
       self.image = pygame.Surface([self.width, self.height])
       self.image.fill(BLACK)
       self.lanePos = [SCREENWIDTH / 6, SCREENWIDTH / 2, 5 * (SCREENWIDTH / 6)]



       # Fetch the rectangle object that has the dimensions of the image
       # Update the position of this object by setting the values of rect.x and rect.y
       self.rect = self.image.get_rect()
       self.rect.y = -50

    def update(self):
        self.rect.y += FALLSPEED
        if (self.rect.y >= SCREENHEIGHT+20):
            self.kill()




class InAir(pygame.sprite.Sprite):

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self):

       # Call the parent class (Sprite) constructor
       pygame.sprite.Sprite.__init__(self)


       # Create an image of the block, and fill it with a color.
       # This could also be an image loaded from the disk.
       self.label = 1  # 0 - run, 1 -air, -1 - ground
       self.width = 20
       self.height = 20
       self.image = pygame.Surface([self.width, self.height])
       self.image.fill(WHITE)
       self.lanePos = [SCREENWIDTH / 6, SCREENWIDTH / 2, 5 * (SCREENWIDTH / 6)]


       # Fetch the rectangle object that has the dimensions of the image
       # Update the position of this object by setting the values of rect.x and rect.y
       self.rect = self.image.get_rect()

    def update(self):
        self.rect.y += FALLSPEED
        if (self.rect.y >= SCREENHEIGHT+20):
            self.kill()

def StartScreen():
    start = True
    while start:

        screen.fill(BLACK)
        pygame.display.flip()

        for event in pygame.event.get():
            # Close window if click x-button
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    start = False
                    break

def GameOverScreen():
    start = True
    while start:

        screen.fill(BLACK)
        pygame.display.flip()

        for event in pygame.event.get():
            # Close window if click x-button
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    start = False
                    break


# add later for better code
def TrackScore():
    pass

def NewObs():
    pass


all_sprites_list = pygame.sprite.Group()
all_obstacles_list =pygame.sprite.Group()

player1 = Player()
# box1 = OnGround((BLACK), 20, 20)

# Inital start in center

all_sprites_list.add(player1)
# all_sprites_list.add(box1)


# Allowing the user to close the window...
carryOn = True

previousObs = -1

score = 0
scoreCounter = 0

StartScreen()
while carryOn:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            carryOn = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player1.ChangeLane('left')
            elif event.key == pygame.K_RIGHT:
                player1.ChangeLane('right')
            elif event.key == pygame.K_UP:
                player1.Jump()
            elif event.key == pygame.K_DOWN:
                player1.Duck()

    # Handles addition of obstacles
    rand = random.randint(0,100)


    if (rand< OBJECTPROB and previousObs != 0):
        previousObs = 0
        if (rand % 2 ==0):
            obstacle = OnGround()
            obstacle.rect.x = obstacle.lanePos[0]
            all_sprites_list.add(obstacle)
            all_obstacles_list.add(obstacle)
        else:
            obstacle = InAir()
            obstacle.rect.x = obstacle.lanePos[0]
            all_sprites_list.add(obstacle)
            all_obstacles_list.add(obstacle)

    elif(rand < 2*OBJECTPROB and previousObs != 1):
        previousObs = 1
        if (rand % 2 ==0):
            obstacle = OnGround()
            obstacle.rect.x = obstacle.lanePos[1]
            all_sprites_list.add(obstacle)
            all_obstacles_list.add(obstacle)
        else:
            obstacle = InAir()
            obstacle.rect.x = obstacle.lanePos[1]
            all_sprites_list.add(obstacle)
            all_obstacles_list.add(obstacle)
    elif(rand <3*OBJECTPROB and previousObs != 2):
        previousObs = 2
        if (rand % 2 ==0):
            obstacle = OnGround()
            obstacle.rect.x = obstacle.lanePos[2]
            all_sprites_list.add(obstacle)
            all_obstacles_list.add(obstacle)
        else:
            obstacle = InAir()
            obstacle.rect.x = obstacle.lanePos[2]
            all_sprites_list.add(obstacle)
            all_obstacles_list.add(obstacle)


    # Checks Collisions
    for obs in all_obstacles_list:
        hit = player1.CheckCollide(obs.rect.x, obs.width, obs.rect.y, obs.height,obs.label)
        if hit:
            carryOn = False


    # Game Logic
    all_sprites_list.update()

    # Drawing on Screen
    screen.fill(GREEN)
    pygame.draw.line(screen,BLACK,[SCREENWIDTH/3,0],[SCREENWIDTH/3,SCREENHEIGHT],5)
    pygame.draw.line(screen,BLACK,[2*SCREENWIDTH/3,0],[2*SCREENWIDTH/3,SCREENHEIGHT],5)


    scoreCounter += 1
    if (scoreCounter % 30 == 0):
        score += 1
    score_tracker = "Score: " + str(score)
    score_board = font.render(str(score_tracker), True, BLACK)
    screen.blit(score_board, [SCREENWIDTH - 120, 20])


    # Now let's draw all the sprites in one go. (For now we only have 1 sprite!)
    all_sprites_list.draw(screen)

    # Refresh Screen
    pygame.display.flip()

    # Number of frames per secong e.g. 60
    clock.tick(30)

GameOverScreen()
