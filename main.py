import pygame, random
pygame.init()

#PYGAME WINDOW SETUP
display = pygame.display.set_mode((1000,600))
pygame.display.set_icon(pygame.image.load('resources/gameicon.png'))

#VARIABLES
carryOn = True

#COLOURS
BLACK = (0,0,0)
MINECOUNTS = [('Not a colour.'),(0,0,255),(0,128,0),(255,0,0),(0,0,128),(128,0,0),(0,128,128),(0,0,0),(128,128,128),(255,255,255)] #NOTE: Numbers are in right position (1,2,3,4,5,6,7,8,9), No offset. 9 is there because why not.
BGCOLOUR = [(192,192,192),(128,128,128)]

#FONTS
font = pygame.font.Font("mine-sweeper.TTF",20)

#GRID
grid = [[0 for i in range(0,9)] for i in range(0,9)]
print(grid)

#FUNCTIONS



#MAIN LOOP
while carryOn:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            carryOn = False
    display.fill(BLACK)