import pygame, json
from tile_map import TileMap
from pygame.locals import *

def main():

    with open("config.json", "r") as f:
        config = json.load(f)

    #Music
    pygame.mixer.pre_init(44100, -16, 2, 4096)
    pygame.init()

    x_screen_size = pygame.display.Info().current_w
    y_screen_size = pygame.display.Info().current_h

    screen = pygame.display.set_mode((x_screen_size, y_screen_size))
    #screen = pygame.display.set_mode((x_screen_size, y_screen_size))
    pygame.display.set_caption('The game')

    display = pygame.Surface((380, 220))

    Map = TileMap(10, "Tiles/")
    Map.load_map("map_0.json")

    mouse_tile = pygame.image.load("Tiles/dirt_box_full.png")

    clock = pygame.time.Clock()

    playerpos = [0,0]
    keys = {"left":False,"right":False,"jump":False,"up":False,"down":False}


    while True:
        display.fill((0, 0, 0))
        
        Map.draw_map(display, playerpos)

        rect = mouse_tile.get_rect()
        #rect.topleft = tuple((pygame.mouse.get_pos()[0]/(x_screen_size/320), pygame.mouse.get_pos()[1]/(y_screen_size/240)))
        #print(Map.collides(rect, display), (pygame.mouse.get_pos()[0]/(x_screen_size/320), pygame.mouse.get_pos()[1]/(y_screen_size/240)))

        #display.blit(mouse_tile, (pygame.mouse.get_pos()[0]/(x_screen_size/320), pygame.mouse.get_pos()[1]/(y_screen_size/240)))
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
        
        if keys["left"]:
            playerpos[0]+=1
        if keys["right"]:
            playerpos[0]-=1
        if keys["down"]:
            playerpos[1]-=1
        if keys["up"]:
            playerpos[1]+=1
            
        screen.blit(pygame.transform.scale(display, pygame.display.get_window_size()), (0,0))
        pygame.display.update()
        clock.tick(70)

main()
