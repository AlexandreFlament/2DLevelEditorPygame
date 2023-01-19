import pygame
from tile_map import TileMap


class Editor(TileMap):
    def __init__(self, tile_size, tiles_file):
        super().__init__(tile_size, tiles_file)

        self.levelmap = pygame.Surface((380, 220))
        self.editormap = pygame.image.load("editor.png")

        self.selectedblock = None
        self.current_layer = 0
        self.current_page = "0"
        self.camerapos = [0,0]

        self.add_layer_rect = pygame.Rect(145, 231, 13, 12)
        self.remove_layer_rect = pygame.Rect(145, 245, 13, 12)
        self.move_to_layer_rect = pygame.Rect(145, 259, 13, 12)
        self.set_layer_speed_rect = pygame.Rect(254, 231, 13, 12)
        
        self.blocks_interactables = {}

        x=0
        y=0
        page=0
        for tile in self.tiles:

            if str(page) not in self.blocks_interactables:
                self.blocks_interactables[str(page)] = {}

            rect = self.tiles[tile].get_rect()
            rect.topleft = (8 + 17 * x, 44 + 15 * y)
            self.blocks_interactables[str(page)][str(8 + 17 * x)+";"+str(44 + 15 * y)] = [tile, self.tiles[tile], rect]
            if x != 2:
                x += 1
            else:
                x = 0
                y +=1


    def draw_editor(self):
        self.levelmap.fill((0,0,0))
        self.draw_map(self.levelmap, tuple(self.camerapos))
        self.editormap.blit(self.levelmap, (60, 0))

        for pos in self.blocks_interactables[self.current_page]:
            pygame.draw.rect(self.editormap, (255,0,255), self.blocks_interactables[self.current_page][pos][2])
            self.editormap.blit(self.blocks_interactables[self.current_page][pos][1], self.blocks_interactables[self.current_page][pos][2].topleft)
    
    def movecamera(self, mov):
        if mov["left"]:
            self.camerapos[0]+=1
        if mov["right"]:
            self.camerapos[0]-=1
        if mov["down"]:
            self.camerapos[1]-=1
        if mov["up"]:
            self.camerapos[1]+=1