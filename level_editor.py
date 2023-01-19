import pygame
from tile_map import TileMap


class Editor(TileMap):
    def __init__(self, tile_size, tiles_file):
        super().__init__(tile_size, tiles_file)

        self.levelmap = pygame.Surface((380, 220))
        self.editormap = pygame.Surface((480, 280))

        self.selectedblock = None
        self.current_layer = 0
        self.camerapos = [0,0]
    
    def draw_editor(self):
        self.draw_map(self.levelmap, tuple(self.camerapos))
        pygame.draw.rect(self.editormap, (255,255,255), self.editormap.get_rect())
        self.editormap.blit(self.levelmap, (60, 0))
    
    def movecamera(self, mov):
        if mov["left"]:
            self.camerapos[0]+=1
        if mov["right"]:
            self.camerapos[0]-=1
        if mov["down"]:
            self.camerapos[1]-=1
        if mov["up"]:
            self.camerapos[1]+=1