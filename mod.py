import pygame
import numpy as np
import logging

pygame.init()

FPS = 1 # frames per second setting

fpsClock = pygame.time.Clock()


width, height = 1000, 1000

screen = pygame.display.set_mode((height, width))

bg = 25, 25, 25
red = 200, 0, 0
green = 0, 200, 0
blue = 0, 0, 200

screen.fill(bg)

nxC, nyC = 25, 25

dimCW = width / nxC
dimCH = height / nyC

gameState = np.zeros((nxC, nyC, 3))

gameState[5, 3, 2] = 1
gameState[5, 4, 2] = 1
gameState[5, 5, 2] = 1

gameState[6, 5, 1] = 1
gameState[20, 5, 1] = 1
gameState[20, 4, 1] = 1

running = True
pauseExect = False

# executing loop
while running:

    newGameState = np.copy(gameState)

    for event in pygame.event.get():  
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            pauseExect = not pauseExect
        
        mouseClick = pygame.mouse.get_pressed()

        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
            if mouseClick[0] == 1:
                newGameState[celX, celY, 0] = not newGameState[celX, celY, 0]
            elif mouseClick[1] == 1:
                newGameState[celX, celY, 1] = not newGameState[celX, celY, 1]
            elif mouseClick[2] == 1:
                newGameState[celX, celY, 2] = not newGameState[celX, celY, 2]

    screen.fill(bg)

    for y in range(0, nxC):
        for x in range(0, nyC):
            colour = 0,0,0
            for rgb in range(0, 3):

                if not pauseExect:
                    n_neigh = gameState[(x-1) % nxC, (y-1) % nyC, rgb] + \
                              gameState[ x    % nxC, (y-1) % nyC, rgb] + \
                              gameState[(x+1) % nxC, (y-1) % nyC, rgb] + \
                              gameState[(x-1) % nxC,  y    % nyC, rgb] + \
                              gameState[ x    % nxC,  y    % nyC, rgb] + \
                              gameState[(x+1) % nxC,  y    % nyC, rgb] + \
                              gameState[(x-1) % nxC, (y+1) % nyC, rgb] + \
                              gameState[ x    % nxC, (y+1) % nyC, rgb] + \
                              gameState[(x+1) % nxC, (y+1) % nyC, rgb]

                    if rgb == 0:
                        n_neigh = n_neigh + gameState[x % nxC, y % nyC, rgb + 1]
                    elif rgb == 1:
                        n_neigh = n_neigh + gameState[x % nxC, y % nyC, rgb - 1] + \
                                  gameState[x % nxC, y % nyC, rgb + 1]
                    elif rgb == 2:
                        n_neigh = n_neigh + gameState[x % nxC, y % nyC, rgb - 1]

                    if gameState[x, y, rgb] == 0 and n_neigh == 3:
                        newGameState[x, y, rgb] = 1

                    elif gameState[x, y, rgb] == 1 and (n_neigh<2 or n_neigh>3):
                        newGameState[x, y, rgb] = 0
                    
                poly = [( x    * dimCW,  y    * dimCH),
                        ((x+1) * dimCW,  y    * dimCH),
                        ((x+1) * dimCH, (y+1) * dimCH),
                        ( x    * dimCH, (y+1) * dimCH)]

                if newGameState[x ,y, rgb] == 0:
                    pygame.draw.polygon(screen, (128,128,128), poly, 1)
                else:
                    if rgb == 0:
                        colour = np.array([colour,red]).sum(axis=0)
                    elif rgb == 1:
                        colour = np.array([colour,green]).sum(axis=0)
                    elif rgb == 2:
                        colour = np.array([colour,blue]).sum(axis=0)
                    pygame.draw.polygon(screen, colour, poly, 0)
    
    gameState = np.copy(newGameState)

    pygame.display.flip()
    fpsClock.tick(FPS)

pygame.quit()