import pygame, random
pygame.init()

#PYGAME WINDOW SETUP
display = pygame.display.set_mode((1000,600))
pygame.display.set_icon(pygame.image.load('resources/gameicon.png'))
framerate = pygame.time.Clock()

#VARIABLES
carryOn = True
rows = int(input('How many rows?\n>')); rowdivison = 1000//rows
columns = int(input('How many columns?\n>')); columndivision = 500//columns

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
    global display, rows, columns, BGCOLOUR
    for i in range(0,columns):
        for j in range(0,rows):
            pygame.draw.rect(display,(128,128,128),[(j*pixels)+(500-((rows/2)*pixels)),(i*pixels)+100,pixels,pixels])
            pygame.draw.rect(display,(192,192,192),[(j*pixels)+(500-((rows/2)*pixels)),(i*pixels)+100,pixels,pixels],2)

#MAIN LOOP
while carryOn:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            carryOn = False
    display.fill((192,192,192))

    if columndivision < rowdivison:
        drawGrid(columndivision)
    else:
        drawGrid(rowdivison)
        
    pygame.draw.rect(display,(128,128,128),[0,0,1000,100])

    pygame.display.flip()
    framerate.tick(60)