import pygame
import numpy as np

pygame.init()

FPS = 3 # frames per second setting

fpsClock = pygame.time.Clock()


width, height = 1000, 1000

screen = pygame.display.set_mode((height, width))

bg = 25, 25, 25

screen.fill(bg)

nxC, nyC = 25, 25

dimCW = width / nxC
dimCH = height / nyC

gameState = np.zeros((nxC, nyC))

gameState[5, 3] = 1
gameState[5, 4] = 1
gameState[5, 5] = 1

gameState[6, 5] = 1
gameState[20, 5] = 1
gameState[20, 4] = 1

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
            newGameState[celX, celY] = mouseClick[2]

    screen.fill(bg)

    for y in range(0, nxC):
        for x in range(0, nyC):

            if not pauseExect:
                n_neigh = gameState[(x-1) % nxC, (y-1) % nyC] + \
                        gameState[ x    % nxC, (y-1) % nyC] + \
                        gameState[(x+1) % nxC, (y-1) % nyC] + \
                        gameState[(x-1) % nxC,  y    % nyC] + \
                        gameState[ x    % nxC,  y    % nyC] + \
                        gameState[(x+1) % nxC,  y    % nyC] + \
                        gameState[(x-1) % nxC, (y+1) % nyC] + \
                        gameState[ x    % nxC, (y+1) % nyC] + \
                        gameState[(x+1) % nxC, (y+1) % nyC]

                if gameState[x, y] == 0 and n_neigh == 3:
                    newGameState[x, y] = 1

                elif gameState[x, y] == 1 and (n_neigh<2 or n_neigh>3):
                    newGameState[x, y] = 0
                
            poly = [( x    * dimCW,  y    * dimCH),
                    ((x+1) * dimCW,  y    * dimCH),
                    ((x+1) * dimCH, (y+1) * dimCH),
                    ( x    * dimCH, (y+1) * dimCH)]

            if newGameState[x ,y] == 0:
                pygame.draw.polygon(screen, (128,128,128), poly, 1)
            else:
                pygame.draw.polygon(screen, (255,255,255), poly, 0)
    
    gameState = np.copy(newGameState)

    pygame.display.flip()
    fpsClock.tick(FPS)

pygame.quit()