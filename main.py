import pygame, random
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

#COLOURS
BLACK = (0,0,0)
MINECOUNTS = [('Not a colour.'),(0,0,255),(0,128,0),(255,0,0),(0,0,128),(128,0,0),(0,128,128),(0,0,0),(128,128,128),(255,255,255)] #NOTE: Numbers are in right position (1,2,3,4,5,6,7,8,9), No offset. 9 is there because why not.
BGCOLOUR = [(192,192,192),(128,128,128),(160,160,160)]

#FONTS
font = pygame.font.Font("mine-sweeper.TTF",20)
numberfont = pygame.font.Font("mine-sweeper.TTF",int((squaresize-(2*(squaresize/10)))-(squaresize/5)))

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
                if i>0 and i<columns-1 and j>0 and j<rows-1:
                    for k in range(-1,2):
                        if grid[i-1][j+k] == 0:
                            plrgrid[i-1][j+k] = 1; pto = True
                    if grid[i][j-1] == 0:
                        plrgrid[i][j-1] = 1; pto = True
                    if grid[i][j+1] == 0:
                        plrgrid[i][j+1] = 1; pto = True
                    for k in range(-1,2):
                        if grid[i+1][j+k] == 0:
                            plrgrid[i+1][j+k] = 1; pto = True
                prvij.append([i,j])
    return pto
#MAIN LOOP
for i in range(0,mines):
    placemines()
gridnumberlogic()
while carryOn:
    mouse = pygame.mouse.get_pos()
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            carryOn = False
        elif i.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                for i in range(0,columns):
                    for j in range(0,rows):
                        if (coordgrid[i][j][0] <= mouse[0] < coordgrid[i][j][0]+squaresize) and (coordgrid[i][j][1] <= mouse[1] < coordgrid[i][j][1]+squaresize):
                            if plrgrid[i][j] != 1:
                                plrgrid[i][j] = 1
            elif pygame.mouse.get_pressed()[2]:
                for i in range(0,columns):
                    for j in range(0,rows):
                        if (coordgrid[i][j][0] <= mouse[0] < coordgrid[i][j][0]+squaresize) and (coordgrid[i][j][1] <= mouse[1] < coordgrid[i][j][1]+squaresize):
                            if plrgrid[i][j] != 1 and plrgrid[i][j] != 2:
                                plrgrid[i][j] = 2
                            elif plrgrid[i][j] == 2:
                                plrgrid[i][j] = 0
                            print(plrgrid)

    display.fill((64,64,64))

    pto = True
    while pto:
        pto = zerochecks()
    prvij = []

    if columndivision < rowdivison:
        drawGrid(columndivision)
    else:
        drawGrid(rowdivison)
        
    pygame.draw.rect(display,(128,128,128),[0,0,1000,100])
    text = font.render('Minesweeper!',1,MINECOUNTS[random.randint(1,7)])
    display.blit(text,(380,10))

    pygame.display.flip()
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