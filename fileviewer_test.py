import pygame
from fileviewer import FileViewer
from pygame.locals import *

def main():

    #Music
    pygame.mixer.pre_init(44100, -16, 2, 4096)
    pygame.init()

    x_screen_size = pygame.display.Info().current_w
    y_screen_size = pygame.display.Info().current_h

    screen = pygame.display.set_mode((x_screen_size, y_screen_size))
    #screen = pygame.display.set_mode((x_screen_size, y_screen_size))
    pygame.display.set_caption('The game')

    display = pygame.Surface((480, 220))

    fv = FileViewer("Saves/")

    clock = pygame.time.Clock()
    keys = {"left":False,"right":False,"jump":False,"up":False,"down":False,"wheel":0}


    while True:
        display.fill((0, 0, 0))
        keys["wheel"] = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == KEYDOWN:
                if event.key in [K_LEFT, K_q]:
                    keys["left"] = True
                if event.key in [K_RIGHT, K_d]:
                    keys["right"] = True
                if event.key in [K_SPACE, K_z, K_UP]:
                    keys["jump"] = True
                if event.key in [K_UP, K_z]:
                    keys["up"] = True
                if event.key in [K_DOWN, K_s]:
                    keys["down"] = True
            if event.type == KEYUP:
                if event.key in [K_LEFT, K_q]:
                    keys["left"] = False
                if event.key in [K_RIGHT, K_d]:
                    keys["right"] = False
                if event.key in [K_SPACE, K_w, K_UP]:
                    keys["jump"] = False
                if event.key in [K_UP, K_z]:
                    keys["up"] = False
                if event.key in [K_DOWN, K_s]:
                    keys["down"] = False
            if event.type == MOUSEWHEEL:
                keys["wheel"]=event.y
    
        fv.update(pygame.display.get_window_size(),keys)

        screen.blit(pygame.transform.scale(fv.surface, pygame.display.get_window_size()), (0,0))
        pygame.display.update()
        clock.tick(70)

main()
