import pygame, random
pygame.init()

#PYGAME WINDOW SETUP
rows = int(input('How many columns?\n>')); rowdivison = 1000//rows ###THESE ARE ACTUALLY COLUMNS BUT THE REPLACE DIDN'T WORK SO THEY'RE ROWS NOW
columns = int(input('How many rows?\n>')); columndivision = 500//columns ###THESE ARE ACTUALLY ROWS BUT THE REPLACE DIDN'T WORK SO THEY'RE COLUMNS NOW
maxboardsize = rows*columns; mines = 0
def minput(mines,maxboardsize):
    mines = int(input('How many mines?\n>'))
    if mines >= maxboardsize:
        print('TOO MANY MINES.\n\n')
        mines = minput(mines,maxboardsize)
    return mines
mines = minput(mines,maxboardsize)

display = pygame.display.set_mode((1000,600))
pygame.display.set_icon(pygame.image.load('resources/gameicon.png'))
pygame.display.set_caption('Minesweeper')
framerate = pygame.time.Clock()

#VARIABLES
carryOn = True

#COLOURS
BLACK = (0,0,0)
MINECOUNTS = [('Not a colour.'),(0,0,255),(0,128,0),(255,0,0),(0,0,128),(128,0,0),(0,128,128),(0,0,0),(128,128,128),(255,255,255)] #NOTE: Numbers are in right position (1,2,3,4,5,6,7,8,9), No offset. 9 is there because why not.
BGCOLOUR = [(192,192,192),(128,128,128)]

#FONTS
font = pygame.font.Font("mine-sweeper.TTF",20)

#GRID
grid = [[0 for i in range(0,rows)] for i in range(0,columns)]

#FUNCTIONS

def drawGrid(pixels):
    global display, rows, columns
    BGCOLOUR = [(192,192,192),(128,128,128)]
    for i in range(0,columns):
        for j in range(0,rows):
            pygame.draw.rect(display,BGCOLOUR[0],[(j*pixels)+(500-((rows/2)*pixels)),(i*pixels)+100,pixels,pixels])
            pygame.draw.rect(display,BGCOLOUR[1],[(j*pixels)+(500-((rows/2)*pixels)),(i*pixels)+100,pixels,pixels],2)

def placemines():
    global grid, rows, columns
    lowpos = random.randint(0,rows-1)
    bigpos = random.randint(0,columns-1)
    if grid[bigpos][lowpos] == 9:
        placemines()
    else:
        grid[bigpos][lowpos] = 9

def gridnumberlogic():
    global grid, rows, columns
    for i in range(0,columns):
        for j in range(0,rows):
            if grid[i][j] != 9:
                mncount = 0
                if i>0 and i<columns-1 and j>0 and j<rows-1:
                    for k in range(-1,2):
                        if grid[i-1][j+k] == 9:
                            mncount += 1
                    if grid[i][j-1] == 9:
                        mncount += 1
                    if grid[i][j+1] == 9:
                        mncount += 1
                    for k in range(-1,2):
                        if grid[i+1][j+k] == 9:
                            mncount += 1
                grid[i][j] = mncount

#MAIN LOOP
for i in range(0,mines):
    placemines()
gridnumberlogic()
print(grid)
while carryOn:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            carryOn = False
    display.fill((64,64,64))

    if columndivision < rowdivison:
        drawGrid(columndivision)
    else:
        drawGrid(rowdivison)
        
    pygame.draw.rect(display,(128,128,128),[0,0,1000,100])
    text = font.render('Minesweeper!',1,MINECOUNTS[random.randint(1,7)])
    display.blit(text,(380,10))

    pygame.display.flip()
    framerate.tick(10)

pygame.quit()
