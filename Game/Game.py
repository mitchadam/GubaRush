import pygame, random, threading

from EventFlags import EventFlags

pygame.init()

arduino = False

GREEN = (20, 255, 140)
GREY = (210, 210, 210)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
BLACK = (0, 0, 0)

secondPlay = False

FALLSPEED = 8

OBJECTPROB = 10

SCREENWIDTH = 1200
SCREENHEIGHT = 800

clock = pygame.time.Clock()


size = (SCREENWIDTH, SCREENHEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("GUBA RUSH")

random.seed(None)

# Prints the score
font = pygame.font.Font("Sprites/PatrickHand-Regular.ttf", 30)
fontTitle = pygame.font.Font("Sprites/PatrickHand-Regular.ttf", 100)
fontScore = pygame.font.Font("Sprites/PatrickHand-Regular.ttf", 50)

fullGoomba = pygame.image.load("Sprites/fullbody.png").convert_alpha()
AngelGoomba = pygame.image.load("Sprites/dead.png").convert_alpha()


fullGoomba = pygame.transform.scale(fullGoomba,(300,300))
run1Goomba = pygame.image.load("Sprites/backRun.png").convert_alpha()
run2Goomba = pygame.image.load("Sprites/backRun2.png").convert_alpha()
jumpGoomba = pygame.image.load("Sprites/jump.png").convert_alpha()
duckGoomba = pygame.image.load("Sprites/duck2.png").convert_alpha()
obstacleLow = pygame.image.load("Sprites/obstacle_low.png").convert_alpha()
obstacleHigh = pygame.image.load("Sprites/obstacle_high.png").convert_alpha()
obstacleLowShadow = pygame.image.load("Sprites/obstacle_low_shadow.png").convert_alpha()
obstacleHighShadow = pygame.image.load("Sprites/obstacle_high_shadow.png").convert_alpha()

heart = pygame.image.load("Sprites/heart.png").convert_alpha()

background = pygame.image.load("Sprites/background.png").convert()
deathBackground = pygame.image.load("Sprites/dead_background.png").convert()

jumpSound = pygame.mixer.Sound('Sprites/jumpSound.wav')
slideSound = pygame.mixer.Sound('Sprites/slideSound2.wav')

pygame.mixer.music.load('Sprites/Background.wav')
pygame.mixer.music.play(-1)

class Angel(pygame.sprite.Sprite):

    # Constructor. Pass in the color of the block,
    # and its x and y positiongit
    def __init__(self):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y

        self.image = AngelGoomba
        self.rect = self.image.get_rect()
        self.rect.x = SCREENWIDTH/2 - 150
        self.rect.y = SCREENHEIGHT
        self.image = pygame.transform.scale(self.image, (300, 400))

    def update(self):
        if self.rect.y >= 220:
            self.rect.y -= 4


class Player(pygame.sprite.Sprite):

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self):

        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)


        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.\
        self.image = run1Goomba
        self.rect = self.image.get_rect()
        self.height = 200
        self.width = 150
        self.lane = 1
        self.lanePos = [(SCREENWIDTH / 6)-75, (SCREENWIDTH / 2)-75, (5*(SCREENWIDTH / 6))-75]
        self.state = 0 #0 - run, 1 -air, -1 - ground
        self.counter = 0
        self.costumes = [run1Goomba, run2Goomba]
        self.costumeState = 0
        self.costumeCount = 0
        self.actionTime = 400/FALLSPEED
        self.speed = 0
        self.image = pygame.transform.scale(self.image, (self.width, self.height))


        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.rect.x = self.lanePos[self.lane]
        self.rect.y = SCREENHEIGHT - 160


    def ChangeLane(self,direction):

        if(direction == 'right'):
            if(self.lane != 2):
                self.lane += 1
                self.speed = 1

        elif(direction == 'left'):
            if (self.lane != 0):
                self.lane -=1
                self.speed = -1


        self.rect.x = self.lanePos[self.lane]

    def Jump(self):
        jumpSound.play()
        self.rect.y -=0.5
        self.state = 1

    def Duck(self):
        slideSound.play()
        self.state = -1

    def CheckCollide(self,x,w,y,h,label):

        if(abs((self.rect.x -x)) < 50 and self.state != -1*label):
            if(y+h-40 >= self.rect.y and y+h-40 <= self.rect.y+self.height) or (y+100 >= self.rect.y and y+100 <= self.rect.y + self.height):
                return True

        return False

    def update(self):
        if(self.state != 0):
            self.counter+=1
            if(self.counter >= self.actionTime):
                self.state = 0
                self.counter =0
            if(self.state == 1):
                # This means he is jumping

                if (self.rect.y < SCREENHEIGHT - 160):
                    self.image = jumpGoomba
                    self.rect.y -= 30 -1.8*self.counter
                else:
                    self.costumeCount += 1
                    if self.costumeCount % 5 == 0:
                        if self.costumeState == 0:
                            self.costumeState = 1
                        elif self.costumeState == 1:
                            self.costumeState = 0
                        self.image = self.costumes[self.costumeState]
                    self.rect.y = SCREENHEIGHT - 160


            elif (self.state == -1):
                # This means he is ducking
                if self.counter >= self.actionTime - 10:
                    self.costumeCount += 1
                    if self.costumeCount % 5 == 0:
                        if self.costumeState == 0:
                            self.costumeState = 1
                        elif self.costumeState == 1:
                            self.costumeState = 0
                        self.image = self.costumes[self.costumeState]
                    self.rect.y = SCREENHEIGHT - 160
                else:
                    self.image = duckGoomba
        else:
            # This means he is running
            self.costumeCount +=1
            if self.costumeCount % 5 == 0:
                if self.costumeState == 0:
                    self.costumeState = 1
                elif self.costumeState == 1:
                    self.costumeState =0
                self.image = self.costumes[self.costumeState]
            self.rect.y = SCREENHEIGHT - 160


class OnGround(pygame.sprite.Sprite):

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self):

        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)


        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.label = -1 #0 - run, 1 -air, -1 - ground
        self.width = 150
        self.newWidth = 200
        self.height = 150
        self.image = pygame.Surface([self.width, self.height])
        self.lanePos = [(SCREENWIDTH / 6)-self.newWidth/2, (SCREENWIDTH / 2)-self.newWidth/2, (5 * (SCREENWIDTH / 6))-self.newWidth/2]

        self.rect = self.image.get_rect()
        self.image = obstacleLow
        self.image = pygame.transform.scale(self.image, (self.newWidth, 150))




        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect.y = -200

    def update(self):
        self.rect.y += FALLSPEED
        if (self.rect.y >= SCREENHEIGHT+20):
            self.kill()


class OnGroundShadow(pygame.sprite.Sprite):

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self):

        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)


        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.label = -1 #0 - run, 1 -air, -1 - ground
        self.width = 150
        self.height = 150
        self.image = pygame.Surface([self.width, self.height])
        self.lanePos = [(SCREENWIDTH / 6)-self.width/2, (SCREENWIDTH / 2)-self.width/2, (5 * (SCREENWIDTH / 6))-self.width/2]

        self.rect = self.image.get_rect()
        self.image = obstacleLowShadow
        self.image = pygame.transform.scale(self.image, (190, 60))




        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect.y = -200 + self.height

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
        self.width = 150
        self.newWidth = 200
        self.height = 150
        self.image = pygame.Surface([self.width, self.height])

        self.lanePos = [(SCREENWIDTH / 6)-self.newWidth/2-15, (SCREENWIDTH / 2)-self.newWidth/2-15, (5 * (SCREENWIDTH / 6))-self.newWidth/2-15]
        self.rect = self.image.get_rect()
        self.rect.y = -200
        self.image = obstacleHigh
        self.image = pygame.transform.scale(self.image, (self.newWidth, 150))



        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y

    def update(self):
        self.rect.y += FALLSPEED
        if (self.rect.y >= SCREENHEIGHT+20):
            self.kill()

class InAirShadow(pygame.sprite.Sprite):

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self):

        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)


        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.label = 1  # 0 - run, 1 -air, -1 - ground
        self.width = 150
        self.height = 150
        self.image = pygame.Surface([self.width, self.height])

        self.lanePos = [(SCREENWIDTH / 6)-self.width/2, (SCREENWIDTH / 2)-self.width/2, (5 * (SCREENWIDTH / 6))-self.width/2]
        self.rect = self.image.get_rect()
        self.rect.y = -200 + self.height
        self.image = obstacleHighShadow
        self.image = pygame.transform.scale(self.image, (200, 100))


        self.counter =0

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y

    def update(self):
        self.rect.y += FALLSPEED
        if (self.rect.y >= SCREENHEIGHT+20):
            self.kill()

        self.counter +=1


class BackDrop(pygame.sprite.Sprite):

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self,):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = background

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y += FALLSPEED

        if self.rect.y >= SCREENHEIGHT:
            self.rect.y = -SCREENHEIGHT

def StartScreen():
    start = True
    while start:

        backdropList.update()
        backdropList.draw(screen)

        buff = font.render("Welcome To", True, WHITE)
        w,h =font.size("welcome to")
        screen.blit(buff, [SCREENWIDTH/2 - w/2, 60])

        buff = fontTitle.render("GUBA RUSH", True, WHITE)
        w, h = fontTitle.size("GUBA RUSH")
        screen.blit(buff, [SCREENWIDTH/2 - w/2, 90])

        buff = font.render("Press Enter To Play", True, WHITE)
        w, h = font.size("Press Enter To Play")
        screen.blit(buff, [SCREENWIDTH / 2 - w / 2, 300])

        screen.blit(fullGoomba,(SCREENWIDTH/2-130, SCREENHEIGHT/2))



        pygame.display.flip()

        for event in pygame.event.get():
            # Close window if click x-button
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    start = False
                    break


def CalibrateScreen():
    counter = 0
    while counter <1:
        counter +=1
        backdropList.update()
        backdropList.draw(screen)

        buff = font.render("Calibrating Hardware...", True, WHITE)
        w, h = font.size("Calibrating Hardware...")
        screen.blit(buff, [SCREENWIDTH / 2 - w / 2, 60])

        pygame.display.flip()

        for event in pygame.event.get():
            # Close window if click x-button
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    start = False
                    break

    if not arduino:
        #pygame.time.delay(5000)
        pass
    else:
        eventFlags.calibrate()



def GameOverScreen(score):
    start = True

    angelGoomba = Angel()
    angelList = pygame.sprite.Group()

    angelList.add(angelGoomba)

    global secondPlay
    secondPlay = True

    leaders = []
    with open ("LeaderBoard", "r") as fid:
        try:
            for line in fid:
                a,b = line.split()
                leaders.append((a + " ", int(b)))
                print('reaing in')
        except:
            pass

    numbersUsers = len(leaders)+1
    with open ("LeaderBoard", "a") as fid:
        strbuff1 = "GUBA_" + str(numbersUsers) + ": "
        strbuff = strbuff1 + str(score) + "\n"
        fid.write(strbuff)
        leaders.append((strbuff1, score))

    leaders = sorted(leaders, key = lambda t: t[1], reverse = True)
    while start:

        screen.blit(deathBackground,(0, 0))


        angelList.update()
        angelList.draw(screen)

        buff = fontTitle.render("GAME OVER", True, WHITE)
        w, h = fontTitle.size("GAME OVER")
        screen.blit(buff, [SCREENWIDTH / 2 - w / 2, 20])

        buff = font.render("Press Enter To Play Again", True, WHITE)
        w, h = font.size("Press Enter To Play Again")
        screen.blit(buff, [SCREENWIDTH / 2 - w / 2, 150])

        ScoreStr = "GUBA_" + str(numbersUsers) + " " +"Score:" + str(score)
        buff = font.render(ScoreStr, True, WHITE)
        w, h = font.size("GUBA_" + str(numbersUsers) + "Score: 10")
        screen.blit(buff, [SCREENWIDTH / 2 - w / 2, 210])

        ScoreStr = "< LEADERBOARD > "
        buff = font.render(ScoreStr, True, WHITE)
        w, h = font.size("< LEADERBOARD > ")                  
        screen.blit(buff, [SCREENWIDTH / 4 - w , 150])

        pygame.draw.lines(screen, WHITE, True, ((SCREENWIDTH / 4 - w, 185), (SCREENWIDTH / 4-5, 185)), 4)

        for i in range(len(leaders)):
            if i <= 7:
                ScoreStr = str(leaders[i][0])
                buff = font.render(ScoreStr, True, WHITE)
                w, h = font.size(ScoreStr)
                screen.blit(buff, [SCREENWIDTH / 4 - w -60, 190+i*40])

                ScoreStr = str(leaders[i][1])
                buff = font.render(ScoreStr, True, WHITE)
                w, h = font.size(ScoreStr)
                screen.blit(buff, [SCREENWIDTH / 4 - w -40, 190+i*40])

        pygame.display.flip()

        for event in pygame.event.get():
            # Close window if click x-button
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    RunGame()
                    break

playerList = pygame.sprite.Group()
lowObstacleList = pygame.sprite.Group()
highObstacleList = pygame.sprite.Group()
all_obstacles_list = pygame.sprite.Group()
backdropList = pygame.sprite.Group()
ShadowList = pygame.sprite.Group()

player1 = Player()
backdrop1 = BackDrop()
backdrop2 = BackDrop()
backdrop2.rect.y = -SCREENHEIGHT


backdropList.add(backdrop1)
backdropList.add(backdrop2)



if arduino:
    eventFlags = EventFlags(port='/dev/tty.usbmodem14101',
                            up_threshold = 3000,
                            down_threshold = 4000,
                            gy_threshold = 2500,
                            up_down_delay=1.5,
                            left_right_delay=1)

    def doEventFlags():
        eventFlags.check()
        if eventFlags.up():
            events.append('up')
        if eventFlags.down():
            events.append('down')
        if eventFlags.left():
            events.append('left')
        if eventFlags.right():
            events.append('right')


    class myThread(threading.Thread):
        def __init__(self, threadID, name, counter):
            threading.Thread.__init__(self)
            self.threadID = threadID
            self.name = name
            self.counter = counter

        def run(self):
            print("Starting " + self.name)
            while 1:
                doEventFlags()

    arduino_thread = myThread(1, "Thread-1", 1)


playerList.add(player1)

events = []


# Allowing the user to close the window...
def RunGame():
    carryOn = True

    previousObs = -1

    score = 0
    scoreCounter = 0

    livesCounter =3

    lane0 = True
    lane0Counter =0
    lane1 = True
    lane1Counter =0
    lane2 = True
    lane2Counter =0
    laneResetValue = 600/FALLSPEED

    StartScreen()
    if not secondPlay:
        CalibrateScreen()

    if arduino and not secondPlay:
        arduino_thread.start()

    while carryOn:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                carryOn = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT :
                    player1.ChangeLane('left')
                elif event.key == pygame.K_RIGHT:
                    player1.ChangeLane('right')
                elif event.key == pygame.K_UP:
                    player1.Jump()
                elif event.key == pygame.K_DOWN:
                    player1.Duck()

        if arduino:
            global events
            for event in events:
                if event == 'left':
                    player1.ChangeLane('left')
                elif event == 'right':
                    player1.ChangeLane('right')
                elif event == 'up':
                    player1.Jump()
                elif event == 'down':
                    player1.Duck()
            events = []


        # Handles addition of obstacles
        rand = random.randint(0,1000)
        shadowshift = 15
        shadowshift2 = 3



        if (rand< OBJECTPROB and  lane0):
            lane0 = False
            if (rand % 2 == 0):
                obstacle = OnGround()
                obstacleShadow = OnGroundShadow()

                obstacle.rect.x = obstacle.lanePos[0]
                obstacleShadow.rect.x = obstacleShadow.lanePos[0] + shadowshift

                lowObstacleList.add(obstacle)
                ShadowList.add(obstacleShadow)

                all_obstacles_list.add(obstacle)
            else:
                obstacle = InAir()
                obstacleShadow = InAirShadow()

                obstacle.rect.x = obstacle.lanePos[0]
                obstacleShadow.rect.x = obstacleShadow.lanePos[0] + shadowshift2

                highObstacleList.add(obstacle)
                ShadowList.add(obstacleShadow)

                all_obstacles_list.add(obstacle)


        elif(rand < 2*OBJECTPROB and lane1):
            lane1 = False
            if (rand % 2 == 0):
                obstacle = OnGround()
                obstacleShadow = OnGroundShadow()

                obstacle.rect.x = obstacle.lanePos[1]
                obstacleShadow.rect.x = obstacleShadow.lanePos[1] + shadowshift

                lowObstacleList.add(obstacle)
                ShadowList.add(obstacleShadow)

                all_obstacles_list.add(obstacle)
            else:
                obstacle = InAir()
                obstacleShadow = InAirShadow()

                obstacle.rect.x = obstacle.lanePos[1]
                obstacleShadow.rect.x = obstacleShadow.lanePos[1] + shadowshift2

                highObstacleList.add(obstacle)
                ShadowList.add(obstacleShadow)

                all_obstacles_list.add(obstacle)

        elif(rand <3*OBJECTPROB and lane2):
            lane2 = False
            if (rand % 2 ==0):
                obstacle = OnGround()
                obstacleShadow = OnGroundShadow()

                obstacle.rect.x = obstacle.lanePos[2]
                obstacleShadow.rect.x = obstacleShadow.lanePos[2] + shadowshift

                lowObstacleList.add(obstacle)
                ShadowList.add(obstacleShadow)

                all_obstacles_list.add(obstacle)
            else:
                obstacle = InAir()
                obstacleShadow = InAirShadow()

                obstacle.rect.x = obstacle.lanePos[2]
                obstacleShadow.rect.x = obstacleShadow.lanePos[2] + shadowshift2

                highObstacleList.add(obstacle)
                ShadowList.add(obstacleShadow)

                all_obstacles_list.add(obstacle)


        # this makes sure obstacles dont overlap
        if (not lane0):
            lane0Counter +=1
            if lane0Counter >= laneResetValue:
                lane0Counter = 0
                lane0 = True

        if (not lane1):
            lane1Counter +=1
            if lane1Counter >= laneResetValue:
                lane1Counter = 0
                lane1 = True

        if (not lane2):
            lane2Counter +=1
            if lane2Counter >= laneResetValue:
                lane2Counter = 0
                lane2 = True

        # Checks Collisions
        for obs in all_obstacles_list:
            hit = player1.CheckCollide(obs.rect.x, obs.width, obs.rect.y, obs.height, obs.label)
            if hit:
                all_obstacles_list.remove(obs)
                hit = False
                livesCounter -= 1
                #print('COLLIDE')
                if livesCounter <=0:
                    # pass # Game Over
                    carryOn = False
                    break


        # Game Logic
        playerList.update()
        lowObstacleList.update()
        highObstacleList.update()
        backdropList.update()
        ShadowList.update()

        # Drawing on Screen
        screen.fill(BLACK)
        pygame.draw.line(screen,BLACK,[SCREENWIDTH/3,0],[SCREENWIDTH/3,SCREENHEIGHT],5)
        pygame.draw.line(screen,BLACK,[2*SCREENWIDTH/3,0],[2*SCREENWIDTH/3,SCREENHEIGHT],5)


        # Now let's draw all the sprites in one go. (For now we only have 1 sprite!)
        backdropList.draw(screen)
        ShadowList.draw(screen)
        lowObstacleList.draw(screen)
        playerList.draw(screen)
        highObstacleList.draw(screen)

        scoreCounter += 1
        if (scoreCounter % 30 == 0):
            score += 1
        score_tracker = "Score: " + str(score)
        w, h = fontScore.size("Score: 100")
        score_board = fontScore.render(str(score_tracker), True, BLACK)
        screen.blit(score_board, [SCREENWIDTH - w - 10, 20])

        # score_tracker = "Action: "
        # w, h = fontScore.size("Action: ")
        # score_board = fontScore.render(str(score_tracker), True, BLACK)
        # screen.blit(score_board, [SCREENWIDTH-w - 200, 20])

        # if eventFlags.ignore and eventFlags.ignore_gy:
        #     indicateColour = RED
        # else:
        #     indicateColour = GREEN
        # pygame.draw.circle(screen,indicateColour,(SCREENWIDTH-w - 55,60),10)
        
        for i in range(0,livesCounter):
            screen.blit(heart,(40 + 100*i, 20))

        # Refresh Screen
        pygame.display.flip()

        # Number of frames per secong e.g. 60
        clock.tick(400)


    GameOverScreen(score)
RunGame()
