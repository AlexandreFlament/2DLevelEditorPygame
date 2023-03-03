import pygame, sys
from level_editor import Editor
from pygame.locals import *

def main(maptoload):

    #Music
    pygame.mixer.pre_init(44100, -16, 2, 4096)
    pygame.init()

    x_screen_size = pygame.display.Info().current_w
    y_screen_size = pygame.display.Info().current_h

    screen = pygame.display.set_mode((x_screen_size, y_screen_size))
    pygame.display.set_caption('The game editor')

    display = pygame.Surface((480, 280))    

    clock = pygame.time.Clock()
    keys = {"left":0,"right":0,"jump":False,"up":0,"down":0,"lctrl":False}

    ed = Editor(10, "Tiles/", "Images/")
    ed.load_map(maptoload)

    while ed.running:
        display.fill((0, 0, 0))
        keys["Wheel"] = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ed.save_map(ed.loaded_map)
                ed.running = False
            if event.type == KEYDOWN:
                if event.key in [K_LEFT, K_q]:
                    keys["left"] = 0.5
                if event.key in [K_RIGHT, K_d]:
                    keys["right"] = 0.5
                if event.key in [K_SPACE, K_z, K_UP]:
                    keys["jump"] = True
                if event.key in [K_UP, K_z]:
                    keys["up"] = 0.5
                if event.key in [K_DOWN, K_s]:
                    keys["down"] = 0.5
                if event.key in [K_LCTRL]:
                    keys["lctrl"] = True
            if event.type == KEYUP:
                if event.key in [K_LEFT, K_q]:
                    keys["left"] = 0
                if event.key in [K_RIGHT, K_d]:
                    keys["right"] = 0
                if event.key in [K_SPACE, K_w, K_UP]:
                    keys["jump"] = False
                if event.key in [K_UP, K_z]:
                    keys["up"] = 0
                if event.key in [K_DOWN, K_s]:
                    keys["down"] = 0
                if event.key in [K_LCTRL]:
                    keys["lctrl"] = False
            if event.type == MOUSEWHEEL:
                keys["Wheel"]=event.y

        ed.update(keys, pygame.display.get_window_size())

        screen.blit(pygame.transform.scale(ed.editormap, pygame.display.get_window_size()), (0,0))
        pygame.display.update()
        clock.tick(60)
