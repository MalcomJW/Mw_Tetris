#tetris

#imports
import pygame
import random
import sys

pygame.init()
# constants
WIDTH, HEIGHT = 300, 500
FPS = 35

#each block is 20 pix
CELL = 20

ROWS = (HEIGHT - 120) // CELL
COLS = WIDTH // CELL


# Game settings  screen, cloc, title, difficulty
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)

#responsible for fps
clock = pygame.time.Clock()

pygame.display.set_caption("bam")

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BG_COLOR = (31, 25, 76)
GRID = (31, 25, 132)
WIN = (50, 230, 50)
LOSE = (252, 91, 122)


# load / store images
ASSETS = {
    1: pygame.image.load("Assets/1.png"),
    2: pygame.image.load("Assets/2.png"),
    3: pygame.image.load("Assets/3.png"),
    4: pygame.image.load("Assets/4.png")
}

#fonts larger for score and smaller

font = pygame.font.SysFont("verdana", 50)
font2 = pygame.font.SysFont("verdana", 15)





# shape class
class Shape:
    #version is a Dict that has nested lists which contain the 'orientation' of our shapes
    VERSION = {
        'I': [[1, 5, 9, 13], [4, 5, 6, 7]],
        'Z': [[4, 5, 9, 10], [2, 6, 5, 9]],
        'S': [[6, 7, 9, 10], [1, 5, 6, 10]],
        'L': [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        'J': [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        'T': [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        'O': [[1, 2, 5, 6]]

    }

    #is  list of strings that reps different tet shapes
    SHAPES = ['I', 'Z', 'S', 'L', 'J', 'T', 'O']


    #constructor
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.choice(self.SHAPES) #this will act as a key for our version Dict
        self.shape = self.VERSION[self.type] #we'll now get one of our nested lists
        self.color = random.randint(1, 4) #selecting a random int from 1-4
        self.orientation = 0 #starting position of shape in its list.


    #image  - image selection or version of shape
    def image(self):
        #Shape below reps the main parent list
        return self.shape[self.orientation]


    #rotation of shapes
    def rotate(self):
        self.orientation =  (self.orientation + 1) % len(self.shape)








# gameclass
class Tetris:


    # constructor
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.score = 0
        self.level = 1
        self.grid = [[0 for j in range(cols)] for i in range(rows)]
        self.next = None
        self.end = False
        self.new_shape()

    #make grid
    def make_grid(self):
        #we'll draw a line for each row
        for i in range(self.rows+1):
            pygame.draw.line(SCREEN, GRID, (0,CELL*i), (WIDTH, CELL*i)) #for each row we need to draw the line on the screen with a color, we then need our start and end pos
        for j in range(self.cols+1):
            pygame.draw.line(SCREEN, GRID, (CELL* j, 0), (CELL*j, HEIGHT-120))



    #make shape
    def new_shape(self):
        #if there's nothing there, then we create a shape at the middle
        if not self.next:
            self.next = Shape(5,0)
        self.figure = self.next # every tetris shape is known as figure in our code. Has access to everything under our INIT(self, x y) constructor
        self.next = Shape(5,0)


    #Collision is our BOOLEAN
    def collision(self):
        #checking to see if our shape has touched another block
        for i in range(4):
            for j in range(4):
                #checking to see if the number is in our lists
                if (i*4 + j) in self.figure.image():
                    block_row = i + self.figure.y
                    block_col = j + self.figure.x
                    if (block_row >= self.rows or block_col >= self.cols or block_col < 0 or self.grid[block_row] [block_col] > 0): #if our self.grid is greater than 0 then it's one of our pics
                        return True
        return False

    #remove row once completed with shapes

    def remove_row(self):
        rerun = False

        for y in range(self.rows-1, 0, -1):
            completed = True
            for x in range(0, self.cols):
                if self.grid[y][x] ==  0:
                    completed = False

            if completed:
                del self.grid[y]
                self.grid.insert(0, [0 for i in range(self.cols)])
                self.score += 1
                if self.score % 10 == 0:
                    self.level += 1
                rerun = True

            if rerun:
                self.remove_row()

    #freeze once hitting the bottom
    def freeze(self):
        for i in range(4):
            for j in range(4):
                if (i*4+j) in self.figure.image(): #if our number is in our figure figure orient list
                    self.grid[i+self.figure.y][j+self.figure.x] = self.figure.color #turning 0 into a number(occupied)

        # we then create a new shape, but if it stacks to high it ends the game
        self.remove_row()
        self.new_shape()
        if self.collision():
            self.end = True



    #move down
    def move_down(self):
        self.figure.y += 1#the 1 isn't a pixel it is rep a block
        #if a collision occurs then we'll stop our block
        if self.collision():
            self.figure.y -= 1
            self.freeze()

    #move left

    def left(self):
        #moving to the left by 1 lock
        self.figure.x -= 1
        if self.collision():
            self.figure.x += 1 # if collision then we can't move further



    #move right
    def right(self):
        self.figure.x += 1
        if self.collision():
            self.figure.x -= 1


    # free falll (letting the shape fall faster)

    def freefall(self):
        while not self.collision():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    #rotate

    def rotate(self):
        orientation = self.figure.orientation #capturing shapes initial state
        self.figure.rotate()
        if self.collision(): #if we have a collision then we can't switch it. It'll just = the original orientation
            self.figure.orientation = orientation

    def end_game(self):
        popup = pygame.Rect(50, 140, WIDTH-100, HEIGHT - 350)
        pygame.draw.rect(SCREEN, BLACK, popup)
        pygame.draw.rect(SCREEN, LOSE, popup, 2)

        game_over =font2.render("Game over", True, WHITE)
        option1 = font2.render("press r to restart", True, LOSE)
        option2 = font2.render("press q to quit", True, LOSE)

        SCREEN.blit(game_over, (popup.centerx-game_over.get_width()//2, popup.y +20))
        SCREEN.blit(option1, (popup.centerx-option1.get_width()//2, popup.y +80))
        SCREEN.blit(option2, (popup.centerx-option2.get_width()//2, popup.y + 120))



# main game loop With the while true I can more easily switch my game on/off

def main():
    tetris = Tetris(ROWS, COLS)
    counter = 0
    move = True
    space_pressed = False

    run = True
    while run:
        SCREEN.fill(BG_COLOR)

#events can cover clicks, scores, and other noteworthy changes during the operation
        #we grab PyGame's Event Dict
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()
            #EVENT loop

            keys = pygame.key.get_pressed()
            if not tetris.end:
                if keys[pygame.K_LEFT]:
                    tetris.left()
                elif keys[pygame.K_RIGHT]:
                    tetris.right()
                elif keys[pygame.K_DOWN]:
                    tetris.move_down()
                elif keys[pygame.K_UP]:
                    tetris.rotate()
                elif keys[pygame.K_SPACE]:
                    space_pressed = True
            if keys[pygame.K_r]:
                tetris.__init__(ROWS, COLS)
            if keys[pygame.K_ESCAPE] or keys[pygame.K_q]:
                run = False


        # block descends at a constant rate
        counter += 1
        if counter >= 10000:
            counter = 0


        if move:
            if counter % (FPS // (tetris.level*2)) == 0:
                if not tetris.end:
                    if space_pressed:
                        tetris.freefall()
                        space_pressed = False
                    else:
                        tetris.move_down()


        tetris.make_grid()

        #keep fallen shapes
        for x in range(ROWS):
            for y in range(COLS):
                if tetris.grid[x][y] > 0: #if current location is greater than 0 then its a num in 1-4
                    value = tetris.grid[x][y]
                    image = ASSETS[value]
                    SCREEN.blit(image, (y*CELL, x*CELL))
                    pygame.draw.rect(SCREEN, WHITE, (y*CELL, x*CELL, CELL, CELL), 1)

        #show the shape on the game screen
        if tetris.figure:
            for i in range(4):
                for j in range(4):
                    #this checks to see if we have an integer in our figure(VERSION lists)
                    if (i*4 +j) in tetris.figure.image():
                        #creating a shape by going through our ASSETS and we'll grab a pic from it. color is a int from 1-4
                        shape = ASSETS[tetris.figure.color]
                        #xy locations to where the pic will go.
                        x = CELL * (tetris.figure.x + j)
                        y = CELL * (tetris.figure.y + i)
                        #getting the image to be placed on screen at our x& y
                        SCREEN.blit(shape, (x,y))
                        pygame.draw.rect(SCREEN, WHITE, (x,y, CELL, CELL), 1)

        #control panel
        if tetris.next:
            for i in range(4):
                for j in range(4):
                    if (i *4 +j) in tetris.next.image():
                        image = ASSETS[tetris.next.color]
                        x = CELL * (tetris.next.x +j -4)
                        y = HEIGHT -100 + CELL * (tetris.next.y +i)
                        SCREEN.blit(image,(x, y))

        if tetris.end:
            tetris.end_game()



        #score
        score_text = font.render(f"{tetris.score}", True, WHITE)
        level_text = font2.render(f"level: {tetris.level}", True, WHITE)
        SCREEN.blit(score_text,(250-score_text.get_width()//2, HEIGHT-110))
        SCREEN.blit(level_text,(250-level_text.get_width()//2, HEIGHT-30))



        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()