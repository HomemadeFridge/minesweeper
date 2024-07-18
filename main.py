import pygame, random
from data import *
pygame.init()

#PYGAME WINDOW SETUP
rows = int(input('How many columns?\n>')); rowdivison = 1000//rows ###THESE ARE ACTUALLY COLUMNS BUT THE REPLACE DIDN'T WORK SO THEY'RE ROWS NOW
columns = int(input('How many rows?\n>')); columndivision = 500//columns ###THESE ARE ACTUALLY ROWS BUT THE REPLACE DIDN'T WORK SO THEY'RE COLUMNS NOW
maxboardsize = rows*columns; mines = 0; squaresize = min(rowdivison,columndivision)
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
mncount = 0
prvij = []
gcarryOn = True
timed = 100
flags = 0
gameWon = False; gameLost = False

#COLOURS
BLACK = (0,0,0)
MINECOUNTS = [('Not a colour.'),(0,0,255),(0,128,0),(255,0,0),(0,0,128),(128,0,0),(0,128,128),(0,0,0),(128,128,128),(255,255,255)] #NOTE: Numbers are in right position (1,2,3,4,5,6,7,8,9), No offset. 9 is there because why not.
BGCOLOUR = [(192,192,192),(128,128,128),(160,160,160)]
SEG7COLOURS = [(0,0,0),(64,0,0),(255,0,0)]

#FONTS
font = pygame.font.Font("mine-sweeper.TTF",20)
numberfont = pygame.font.Font("mine-sweeper.TTF",int((squaresize-(2*(squaresize/10)))-(squaresize/5)))
mineyfont = pygame.font.Font("mine-sweeper.TTF",75)

#GRID
grid = [[0 for i in range(0,rows)] for i in range(0,columns)]
plrgrid = [[0 for i in range(0,rows)] for i in range(0,columns)]
coordgrid = []; temp = []
for i in range(0, columns):
    for j in range(0,rows):
        temp.append([(j*squaresize)+(500-((rows/2)*squaresize)),(i*squaresize)+100])
    coordgrid.append(temp)
    temp = []

#FUNCTIONS

def drawGrid(pixels):
    global display, rows, columns, plrgrid, grid, MINECOUNTS, squaresize
    BGCOLOUR = [(192,192,192),(128,128,128),(160,160,160)]
    for i in range(0,columns):
        for j in range(0,rows):
            if plrgrid[i][j] == 1:
                pygame.draw.rect(display,BGCOLOUR[2],[(j*pixels)+(500-((rows/2)*pixels)),(i*pixels)+100,pixels,pixels])
                pygame.draw.rect(display,BGCOLOUR[1],[(j*pixels)+(500-((rows/2)*pixels)),(i*pixels)+100,pixels,pixels],1)
            else:
                pygame.draw.rect(display,BGCOLOUR[0],[(j*pixels)+(500-((rows/2)*pixels)),(i*pixels)+100,pixels,pixels])
                pygame.draw.rect(display,BGCOLOUR[1],[(j*pixels)+(500-((rows/2)*pixels)),(i*pixels)+100,pixels,pixels],3)
            if plrgrid[i][j] == 1 and grid[i][j] != 0:
                text = numberfont.render(str(grid[i][j]), 1, MINECOUNTS[grid[i][j]])
                if grid[i][j] == 1:
                    display.blit(text, ((j*pixels)+(500-((rows/2)*pixels))+((3)*int(squaresize/10)),(i*pixels)+100+int(squaresize/10)))
                else:
                    display.blit(text, ((j*pixels)+(500-((rows/2)*pixels))+int(squaresize/5),(i*pixels)+100+int(squaresize/10)))
            elif plrgrid[i][j] == 2:
                text = numberfont.render('F', 1, MINECOUNTS[5])
                display.blit(text, ((j*pixels)+(500-((rows/2)*pixels))+int(squaresize/5),(i*pixels)+100+int(squaresize/10)))
            elif plrgrid[i][j] == 3:
                text = numberfont.render('U', 1, MINECOUNTS[6])
                display.blit(text, ((j*pixels)+(500-((rows/2)*pixels))+int(squaresize/5),(i*pixels)+100+int(squaresize/10)))

def placemines():
    global grid, rows, columns
    lowpos = random.randint(0,rows-1)
    bigpos = random.randint(0,columns-1)
    if grid[bigpos][lowpos] == 9:
        placemines()
    else:
        grid[bigpos][lowpos] = 9

def smallerchecks(i,j,ival,jval,rng1,rng2):
    global grid, mncount
    if grid[i][j+jval] == 9:
        mncount += 1
    for k in range(rng1,rng2):
        if grid[i+ival][j+k] == 9:
            mncount += 1

def edgechecks(i,j,ival,jval):
    global grid, mncount, rows, columns
    if i == 0 or i == columns-1:
        if grid[i][j-1] == 9:
            mncount += 1
        if grid[i][j+1] == 9:
            mncount += 1
        for k in range(-1,2):
            if grid[i+ival][j+k] == 9:
                mncount += 1
    else:
        if grid[i-1][j] == 9:
            mncount += 1
        if grid[i+1][j] == 9:
            mncount += 1
        for k in range(-1,2):
            if grid[i+k][j+jval] == 9:
                mncount += 1

def gridnumberlogic():
    global grid, rows, columns, mncount
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
                elif i == 0 and j == 0:
                    smallerchecks(i,j,1,1,0,2)
                elif i == 0 and j == rows-1:
                    smallerchecks(i,j,1,-1,-1,1)
                elif i == columns-1 and j == 0:
                    smallerchecks(i,j,-1,1,0,2)
                elif i == columns-1 and j == rows-1:
                    smallerchecks(i,j,-1,-1,-1,1)
                elif i == 0:
                    edgechecks(i,j,1,0)
                elif i == columns-1:
                    edgechecks(i,j,-1,0)
                elif j == 0:
                    edgechecks(i,j,0,1)
                elif j == rows-1:
                    edgechecks(i,j,0,-1)
                grid[i][j] = mncount

def zerochecks():
    global grid, rows, columns, plrgrid, prvij
    pto = False
    for i in range(0,columns):
        for j in range(0,rows):
            if plrgrid[i][j] == 1 and [i,j] not in prvij:
                if i > 0 and j > 0 and grid[i-1][j-1] == 0:
                    plrgrid[i-1][j-1] = 1; pto = True
                if i > 0 and grid[i-1][j] == 0:
                    plrgrid[i-1][j] = 1; pto = True
                if i > 0 and j < rows-1 and grid[i-1][j+1] == 0:
                    plrgrid[i-1][j+1] = 1; pto = True
                if j > 0 and grid[i][j-1] == 0:
                    plrgrid[i][j-1] = 1; pto = True
                if j < rows-1 and grid[i][j+1] == 0:
                    plrgrid[i][j+1] = 1; pto = True
                if i < columns-1 and j > 0 and grid[i+1][j-1] == 0:
                    plrgrid[i+1][j-1] = 1; pto = True
                if i < columns-1 and grid[i+1][j] == 0:
                    plrgrid[i+1][j] = 1; pto = True
                if i < columns-1 and j < rows-1 and grid[i+1][j+1] == 0:
                    plrgrid[i+1][j+1] = 1; pto = True
                prvij.append([i,j])
    return pto

def zeroboundchecks():
    global grid, rows, columns, plrgrid, prvij
    pto = False
    for i in range(0,columns):
        for j in range(0,rows):
            if plrgrid[i][j] == 1 and [i,j] not in prvij and grid[i][j] == 0:
                if i > 0 and j > 0 and grid[i-1][j-1] != 0:
                    plrgrid[i-1][j-1] = 1; pto = True
                if i > 0 and grid[i-1][j] != 0:
                    plrgrid[i-1][j] = 1; pto = True
                if i > 0 and j < rows-1 and grid[i-1][j+1] != 0:
                    plrgrid[i-1][j+1] = 1; pto = True
                if j > 0 and grid[i][j-1] != 0:
                    plrgrid[i][j-1] = 1; pto = True
                if j < rows-1 and grid[i][j+1] != 0:
                    plrgrid[i][j+1] = 1; pto = True
                if i < columns-1 and j > 0 and grid[i+1][j-1] != 0:
                    plrgrid[i+1][j-1] = 1; pto = True
                if i < columns-1 and grid[i+1][j] != 0:
                    plrgrid[i+1][j] = 1; pto = True
                if i < columns-1 and j < rows-1 and grid[i+1][j+1] != 0:
                    plrgrid[i+1][j+1] = 1; pto = True
                prvij.append([i,j])
    return pto

def draw7segments(display, colour, offset, i):
    global SEG7COLOURS
    for j, on in enumerate(binaries[i]):
        if on:
            pygame.draw.rect(display, SEG7COLOURS[2], pygame.Rect(positions[j]).move(offset, 0))
        else:
            pygame.draw.rect(display, SEG7COLOURS[1], pygame.Rect(positions[j]).move(offset, 0))

#MAIN LOOP
for i in range(0,mines):
    placemines()
gridnumberlogic()
while carryOn:
    mouse = pygame.mouse.get_pos()
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            carryOn = False
        elif i.type == pygame.MOUSEBUTTONDOWN and gcarryOn:
            if pygame.mouse.get_pressed()[0]:
                for i in range(0,columns):
                    for j in range(0,rows):
                        if (coordgrid[i][j][0] <= mouse[0] < coordgrid[i][j][0]+squaresize) and (coordgrid[i][j][1] <= mouse[1] < coordgrid[i][j][1]+squaresize):
                            if plrgrid[i][j] != 1 and plrgrid[i][j] != 2:
                                plrgrid[i][j] = 1
            elif pygame.mouse.get_pressed()[2]:
                for i in range(0,columns):
                    for j in range(0,rows):
                        if (coordgrid[i][j][0] <= mouse[0] < coordgrid[i][j][0]+squaresize) and (coordgrid[i][j][1] <= mouse[1] < coordgrid[i][j][1]+squaresize):
                            if plrgrid[i][j] != 1 and plrgrid[i][j] != 2 and (mines-flags)>0:
                                plrgrid[i][j] = 2
                                flags += 1
                            elif plrgrid[i][j] == 2:
                                plrgrid[i][j] = 0
                                flags -= 1

    display.fill((64,64,64))

    pto = True
    while pto:
        pto = zerochecks()
    prvij = []
    pto = True
    while pto:
        pto = zeroboundchecks()
    prvij = []
    
    gameWon = True
    for i in range(0,columns):
        for j in range(0,rows):
            if plrgrid[i][j] == 1 and grid[i][j] == 9 and gcarryOn:
                print('get mined.')
                gcarryOn = False
                gameLost = True
            elif plrgrid[i][j] != 1 and grid[i][j] != 9 and gcarryOn:
                gameWon = False

    if columndivision < rowdivison:
        drawGrid(columndivision)
    else:
        drawGrid(rowdivison)
        
    pygame.draw.rect(display,(128,128,128),[0,0,1000,100])
    text = font.render('Minesweeper!',1,MINECOUNTS[random.randint(1,7)])
    display.blit(text,(380,10))
    if not gameLost and gameWon:
        gcarryOn = False
        for i in range(0,columns):
            for j in range(0,rows):
                if grid[i][j] == 9 and plrgrid[i][j] == 0:
                    plrgrid[i][j] = 2
                    flags += 1
    elif gameLost:
        gcarryOn = False
        for i in range(0,columns):
            for j in range(0,rows):
                if grid[i][j] == 9 and plrgrid[i][j] == 0:
                    plrgrid[i][j] = 3
    if not gcarryOn and gameLost:
        text = font.render('Game  Over   :(',1,MINECOUNTS[5])
        display.blit(text,(380,50))
    elif not gcarryOn and gameWon and not gameLost:
        text = font.render('You           win!',1,MINECOUNTS[2])
        display.blit(text,(380,50))
    # text = mineyfont.render(str(timed//60),1,MINECOUNTS[1])
    # display.blit(text,(700,-2))
    # text = mineyfont.render(str(mines-flags),1,MINECOUNTS[1])
    # display.blit(text,(100,-2))

    pygame.draw.rect(display,SEG7COLOURS[0],[90,0,190,100])
    pygame.draw.rect(display,SEG7COLOURS[0],[720,0,190,100])

    draw7segments(display, MINECOUNTS[5], 100, (mines-flags)//100)
    draw7segments(display, MINECOUNTS[5], 160, ((mines-flags)%100)//10)
    draw7segments(display, MINECOUNTS[5], 220, (mines-flags)%10)

    draw7segments(display, MINECOUNTS[5], (1000-270), (timed//60)//100)
    draw7segments(display, MINECOUNTS[5], (1000-210), ((timed//60)%100)//10)
    draw7segments(display, MINECOUNTS[5], (1000-150), (timed//60)%10)

    pygame.display.flip()

    if gcarryOn: timed += 1
    if timed//60 >= 999: 
        gcarryOn = False
        gameLost = True
    
    ##IF YOU WANT TO REMOVE THE TIME LIMIT, USE THIS INSTEAD OF THE ABOVE:
    ##if timed//60 >= 999: timed = 0

    framerate.tick(60)
pygame.quit()

##smaller checks can also be rewritten as:
                    # if grid[i][j-1] == 9:
                    #     mncount += 1
                    # for k in range(-1,1):
                    #     if grid[i+1][j+k] == 9:
                    #         mncount += 1

##edge checks can also be:
                    # if grid[i][j-1] == 9:
                    #     mncount += 1
                    # if grid[i][j+1] == 9:
                    #     mncount += 1
                    # for k in range(-1,2):
                    #     if grid[i+1][j+k] == 9:
                    #         mncount += 1

# def zerochecks():
#     global grid, rows, columns, plrgrid, prvij
#     pto = False
#     for i in range(0,columns):
#         for j in range(0,rows):
#             if plrgrid[i][j] == 1 and [i,j] not in prvij:
#                 if i>0 and i<columns-1 and j>0 and j<rows-1:
#                     for k in range(-1,2):
#                         if grid[i-1][j+k] == 0:
#                             plrgrid[i-1][j+k] = 1; pto = True
#                     if grid[i][j-1] == 0:
#                         plrgrid[i][j-1] = 1; pto = True
#                     if grid[i][j+1] == 0:
#                         plrgrid[i][j+1] = 1; pto = True
#                     for k in range(-1,2):
#                         if grid[i+1][j+k] == 0:
#                             plrgrid[i+1][j+k] = 1; pto = True
#                 prvij.append([i,j])
#     return pto