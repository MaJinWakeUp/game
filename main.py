import random, pygame, sys
from pygame.locals import *

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)

class Game:
    def __init__(self):
        self.FPS = 10
        self.SPEED = 5
        self.WINDOWWIDTH = 880
        self.WINDOWHEIGHT = 680
        self.CELLSIZE = 40
        self.CELLWIDTH = int(self.WINDOWWIDTH / self.CELLSIZE)
        self.CELLHEIGHT = int(self.WINDOWHEIGHT / self.CELLSIZE)
        self.BGCOLOR = BLACK
        self.UP = 'up'
        self.DOWN = 'down'
        self.LEFT = 'left'
        self.RIGHT = 'right'
        self.HEAD = 0  # syntactic sugar: index of the worm's head
        self.CURRENT_LEVEL = 1

    def run(self):
        global FPSCLOCK, DISPLAYSURF, BASICFONT

        pygame.init()
        FPSCLOCK = pygame.time.Clock()
        DISPLAYSURF = pygame.display.set_mode((self.WINDOWWIDTH, self.WINDOWHEIGHT))
        BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
        pygame.display.set_caption('HalloThanksMas')

        self.showStartScreen()


    def runLevel1(self):
        startx = random.randint(5, self.CELLWIDTH - 6)
        starty = random.randint(5, self.CELLHEIGHT - 6)
        wormCoords = [{'x': startx, 'y': starty},
                        {'x': startx - 1, 'y': starty},
                        {'x': startx - 2, 'y': starty}]
        direction = self.RIGHT
        apple = self.getRandomLocation(wormCoords)

        # show the first frame, and wait for the player input
        DISPLAYSURF.fill(self.BGCOLOR)
        self.drawGrid()
        self.drawWorm(wormCoords)
        self.drawApple(apple)
        self.drawScore(len(wormCoords) - 3)

        while True:
            self.drawPressKeyMsg()

            if self.checkForKeyPress():
                pygame.event.get() 
                break

            pygame.display.update()
            FPSCLOCK.tick(self.FPS)

        while True:
            pre_direction = direction
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.terminate()
                elif event.type == KEYDOWN:
                    if (event.key == K_LEFT or event.key == K_a) and direction != self.RIGHT:
                        direction = self.LEFT
                    elif (event.key == K_RIGHT or event.key == K_d) and direction != self.LEFT:
                        direction = self.RIGHT
                    elif (event.key == K_UP or event.key == K_w) and direction != self.DOWN:
                        direction = self.UP
                    elif (event.key == K_DOWN or event.key == K_s) and direction != self.UP:
                        direction = self.DOWN
                    elif event.key == K_ESCAPE:
                        self.terminate()

            if wormCoords[self.HEAD]['x'] == -1 or wormCoords[self.HEAD]['x'] == self.CELLWIDTH or wormCoords[self.HEAD]['y'] == -1 or wormCoords[self.HEAD]['y'] == self.CELLHEIGHT:
                return self.showGameOverScreen()
            for wormBody in wormCoords[1:]:
                if wormBody['x'] == wormCoords[self.HEAD]['x'] and wormBody['y'] == wormCoords[self.HEAD]['y']:
                    return self.showGameOverScreen()

            if wormCoords[self.HEAD]['x'] == apple['x'] and wormCoords[self.HEAD]['y'] == apple['y']:
                apple = self.getRandomLocation(wormCoords)
            else:
                del wormCoords[-1]

            if not self.examine_direction(direction, pre_direction):
                direction = pre_direction
            if direction == self.UP:
                newHead = {'x': wormCoords[self.HEAD]['x'], 'y': wormCoords[self.HEAD]['y'] - 1}
            elif direction == self.DOWN:
                newHead = {'x': wormCoords[self.HEAD]['x'], 'y': wormCoords[self.HEAD]['y'] + 1}
            elif direction == self.LEFT:
                newHead = {'x': wormCoords[self.HEAD]['x'] - 1, 'y': wormCoords[self.HEAD]['y']}
            elif direction == self.RIGHT:
                newHead = {'x': wormCoords[self.HEAD]['x'] + 1, 'y': wormCoords[self.HEAD]['y']}
            wormCoords.insert(0, newHead)
            DISPLAYSURF.fill(self.BGCOLOR)
            self.drawGrid()
            self.drawWorm(wormCoords)
            self.drawApple(apple)
            self.drawScore(len(wormCoords) - 3)
            pygame.display.update()
            FPSCLOCK.tick(self.FPS)
    
    def runLevel2(self):
        startx = random.randint(5, self.CELLWIDTH - 6)
        starty = random.randint(5, self.CELLHEIGHT - 6)
        wormCoords = [{'x': startx, 'y': starty},
                        {'x': startx - 1, 'y': starty},
                        {'x': startx - 2, 'y': starty}]
        direction = self.RIGHT
        apple = self.getRandomLocation(wormCoords)

        while True:
            pre_direction = direction
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.terminate()
                elif event.type == KEYDOWN:
                    if (event.key == K_LEFT or event.key == K_a) and direction != self.RIGHT:
                        direction = self.LEFT
                    elif (event.key == K_RIGHT or event.key == K_d) and direction != self.LEFT:
                        direction = self.RIGHT
                    elif (event.key == K_UP or event.key == K_w) and direction != self.DOWN:
                        direction = self.UP
                    elif (event.key == K_DOWN or event.key == K_s) and direction != self.UP:
                        direction = self.DOWN
                    elif event.key == K_ESCAPE:
                        self.terminate()

            if wormCoords[self.HEAD]['x'] == -1 or wormCoords[self.HEAD]['x'] == self.CELLWIDTH or wormCoords[self.HEAD]['y'] == -1 or wormCoords[self.HEAD]['y'] == self.CELLHEIGHT:
                return
            for wormBody in wormCoords[1:]:
                if wormBody['x'] == wormCoords[self.HEAD]['x'] and wormBody['y'] == wormCoords[self.HEAD]['y']:
                    return

            if wormCoords[self.HEAD]['x'] == apple['x'] and wormCoords[self.HEAD]['y'] == apple['y']:
                apple = self.getRandomLocation(wormCoords)
            else:
                del wormCoords[-1]

            if not self.examine_direction(direction, pre_direction):
                direction = pre_direction
            if direction == self.UP:
                newHead = {'x': wormCoords[self.HEAD]['x'], 'y': wormCoords[self.HEAD]['y'] - 1}
            elif direction == self.DOWN:
                newHead = {'x': wormCoords[self.HEAD]['x'], 'y': wormCoords[self.HEAD]['y'] + 1}
            elif direction == self.LEFT:
                newHead = {'x': wormCoords[self.HEAD]['x'] - 1, 'y': wormCoords[self.HEAD]['y']}
            elif direction == self.RIGHT:
                newHead = {'x': wormCoords[self.HEAD]['x'] + 1, 'y': wormCoords[self.HEAD]['y']}
            wormCoords.insert(0, newHead)
            DISPLAYSURF.fill(self.BGCOLOR)
            self.drawGrid()
            self.drawWorm(wormCoords)
            self.drawApple(apple)
            self.drawScore(len(wormCoords) - 3)
            pygame.display.update()
            FPSCLOCK.tick(self.FPS)
    
    def runLevel3(self):
        startx = random.randint(5, self.CELLWIDTH - 6)
        starty = random.randint(5, self.CELLHEIGHT - 6)
        wormCoords = [{'x': startx, 'y': starty},
                        {'x': startx - 1, 'y': starty},
                        {'x': startx - 2, 'y': starty}]
        direction = self.RIGHT
        apple = self.getRandomLocation(wormCoords)

        while True:
            pre_direction = direction
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.terminate()
                elif event.type == KEYDOWN:
                    if (event.key == K_LEFT or event.key == K_a) and direction != self.RIGHT:
                        direction = self.LEFT
                    elif (event.key == K_RIGHT or event.key == K_d) and direction != self.LEFT:
                        direction = self.RIGHT
                    elif (event.key == K_UP or event.key == K_w) and direction != self.DOWN:
                        direction = self.UP
                    elif (event.key == K_DOWN or event.key == K_s) and direction != self.UP:
                        direction = self.DOWN
                    elif event.key == K_ESCAPE:
                        self.terminate()

            if wormCoords[self.HEAD]['x'] == -1 or wormCoords[self.HEAD]['x'] == self.CELLWIDTH or wormCoords[self.HEAD]['y'] == -1 or wormCoords[self.HEAD]['y'] == self.CELLHEIGHT:
                return
            for wormBody in wormCoords[1:]:
                if wormBody['x'] == wormCoords[self.HEAD]['x'] and wormBody['y'] == wormCoords[self.HEAD]['y']:
                    return

            if wormCoords[self.HEAD]['x'] == apple['x'] and wormCoords[self.HEAD]['y'] == apple['y']:
                apple = self.getRandomLocation(wormCoords)
            else:
                del wormCoords[-1]

            if not self.examine_direction(direction, pre_direction):
                direction = pre_direction
            if direction == self.UP:
                newHead = {'x': wormCoords[self.HEAD]['x'], 'y': wormCoords[self.HEAD]['y'] - 1}
            elif direction == self.DOWN:
                newHead = {'x': wormCoords[self.HEAD]['x'], 'y': wormCoords[self.HEAD]['y'] + 1}
            elif direction == self.LEFT:
                newHead = {'x': wormCoords[self.HEAD]['x'] - 1, 'y': wormCoords[self.HEAD]['y']}
            elif direction == self.RIGHT:
                newHead = {'x': wormCoords[self.HEAD]['x'] + 1, 'y': wormCoords[self.HEAD]['y']}
            wormCoords.insert(0, newHead)
            DISPLAYSURF.fill(self.BGCOLOR)
            self.drawGrid()
            self.drawWorm(wormCoords)
            self.drawApple(apple)
            self.drawScore(len(wormCoords) - 3)
            pygame.display.update()
            FPSCLOCK.tick(self.FPS)

    def examine_direction(self, temp, direction):
        if direction == self.UP and temp == self.DOWN:
            return False
        elif direction == self.RIGHT and temp == self.LEFT:
            return False
        elif direction == self.LEFT and temp == self.RIGHT:
            return False
        elif direction == self.DOWN and temp == self.UP:
            return False
        return True

    def drawPressKeyMsg(self):
        pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
        pressKeyRect = pressKeySurf.get_rect()
        pressKeyRect.topleft = (self.WINDOWWIDTH - 200, self.WINDOWHEIGHT - 30)
        DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

    def checkForKeyPress(self):
        if len(pygame.event.get(QUIT)) > 0:
            self.terminate()

        keyUpEvents = pygame.event.get(KEYUP)
        if len(keyUpEvents) == 0:
            return None
        if keyUpEvents[0].key == K_ESCAPE:
            self.terminate()
        return keyUpEvents[0].key

    def showStartScreen(self):
        titleFont = pygame.font.Font('freesansbold.ttf', 50)
        titleSurf = titleFont.render('Welcome to HalloThanksMas!', True, DARKGREEN, DARKGRAY)
        titleRect = titleSurf.get_rect()
        titleRect.center = (self.WINDOWWIDTH / 2, self.WINDOWHEIGHT / 2 - 50)

        # Level 1: Halloween
        # Level 2: Thanksgiving
        # Level 3: Christmas
        # show theses levels in the start screen, and let the player choose one
        selectSurf = BASICFONT.render('Select a level by pressing corresponding key:', True, WHITE)
        selectRect = selectSurf.get_rect()
        selectRect.center = (self.WINDOWWIDTH / 2, self.WINDOWHEIGHT / 2)

        levels = ['1: Halloween', '2: Thanksgiving', '3: Christmas']

        DISPLAYSURF.fill(self.BGCOLOR)
        DISPLAYSURF.blit(titleSurf, titleRect)
        DISPLAYSURF.blit(selectSurf, selectRect)
        # self.drawPressKeyMsg()

        for i in range(len(levels)):
            # align the levels in the left
            levelSurf = BASICFONT.render(levels[i], True, WHITE)
            levelRect = levelSurf.get_rect()
            levelRect.topleft = (self.WINDOWWIDTH / 2 - 100, self.WINDOWHEIGHT / 2 + 20 + 30 * i)
            DISPLAYSURF.blit(levelSurf, levelRect)
        

        while True:
            key = self.checkForKeyPress()
            if key is not None:
                if key == K_1:
                    self.CURRENT_LEVEL = 1
                    self.runLevel1()
                elif key == K_2:
                    self.CURRENT_LEVEL = 2
                    self.runLevel2()
                elif key == K_3:
                    self.CURRENT_LEVEL = 3
                    self.runLevel3()
                break
            pygame.display.update()
            FPSCLOCK.tick(self.FPS)

    def terminate(self):
        pygame.quit()
        sys.exit()

    def getRandomLocation(self, worm):
        temp = {'x': random.randint(0, self.CELLWIDTH - 1), 'y': random.randint(0, self.CELLHEIGHT - 1)}
        while self.test_not_ok(temp, worm):
            temp = {'x': random.randint(0, self.CELLWIDTH - 1), 'y': random.randint(0, self.CELLHEIGHT - 1)}
        return temp

    def test_not_ok(self, temp, worm):
        for body in worm:
            if temp['x'] == body['x'] and temp['y'] == body['y']:
                return True
        return False

    def showGameOverScreen(self):
        gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
        gameSurf = gameOverFont.render('Game', True, WHITE)
        overSurf = gameOverFont.render('Over', True, WHITE)
        gameRect = gameSurf.get_rect()
        overRect = overSurf.get_rect()
        gameRect.midtop = (self.WINDOWWIDTH / 2, 10)
        overRect.midtop = (self.WINDOWWIDTH / 2, gameRect.height + 10 + 25)

        DISPLAYSURF.blit(gameSurf, gameRect)
        DISPLAYSURF.blit(overSurf, overRect)

        # show the "1: Restart" and "2: Main Menu" options
        options = ['1: Restart', '2: Main Menu']
        for i in range(len(options)):
            optionSurf = BASICFONT.render(options[i], True, WHITE)
            optionRect = optionSurf.get_rect()
            optionRect.center = (self.WINDOWWIDTH / 2, self.WINDOWHEIGHT / 2 + 50 + 30 * i)
            DISPLAYSURF.blit(optionSurf, optionRect)

        while True:
            key = self.checkForKeyPress()
            if key is not None:
                if key == K_1:
                    if self.CURRENT_LEVEL == 1:
                        self.runLevel1()
                    elif self.CURRENT_LEVEL == 2:
                        self.runLevel2()
                    elif self.CURRENT_LEVEL == 3:
                        self.runLevel3()
                elif key == K_2:
                    self.showStartScreen()
                else:
                    continue
                break
            pygame.display.update()
            FPSCLOCK.tick(self.FPS)

    def drawScore(self, score):
        scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (self.WINDOWWIDTH - 120, 10)
        DISPLAYSURF.blit(scoreSurf, scoreRect)

    def drawWorm(self, wormCoords):
        for coord in wormCoords:
            x = coord['x'] * self.CELLSIZE
            y = coord['y'] * self.CELLSIZE
            wormSegmentRect = pygame.Rect(x, y, self.CELLSIZE, self.CELLSIZE)
            pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormSegmentRect)
            wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, self.CELLSIZE - 8, self.CELLSIZE - 8)
            pygame.draw.rect(DISPLAYSURF, GREEN, wormInnerSegmentRect)

    def drawApple(self, coord):
        x = coord['x'] * self.CELLSIZE
        y = coord['y'] * self.CELLSIZE
        appleImage = pygame.image.load('images/turkey.png').convert_alpha()
        appleImage = pygame.transform.scale(appleImage, (self.CELLSIZE, self.CELLSIZE))
        appleRect = appleImage.get_rect()
        appleRect.topleft = (x, y)
        DISPLAYSURF.blit(appleImage, appleRect)

    def drawGrid(self):
        for x in range(0, self.WINDOWWIDTH, self.CELLSIZE):
            pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, self.WINDOWHEIGHT))
        for y in range(0, self.WINDOWHEIGHT, self.CELLSIZE):
            pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (self.WINDOWWIDTH, y))


if __name__ == '__main__':
    game = Game()
    game.run()