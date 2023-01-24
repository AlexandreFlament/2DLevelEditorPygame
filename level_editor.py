import pygame
from tile_map import TileMap


def scale_mouse_pos(screen_size):
    mousepos = list(pygame.mouse.get_pos())
    ratio_x = (screen_size[0] - 1) / 480
    ratio_y = (screen_size[1] - 1) / 280
    return mousepos[0] / ratio_x, mousepos[1] / ratio_y


class Editor(TileMap):
    def __init__(self, tile_size, tiles_file):
        super().__init__(tile_size, tiles_file)

        self.levelmap = pygame.Surface((380, 220))
        self.editormap = pygame.image.load("editor.png")

        self.selectedblock = None
        self.current_layer = 0
        self.current_page = "0"
        self.all_pages = []
        self.camerapos = [0,0]

        self.add_layer_rect = pygame.Rect(145, 231, 13, 12)
        self.remove_layer_rect = pygame.Rect(145, 245, 13, 12)
        self.move_to_layer_rect = pygame.Rect(145, 259, 13, 12)
        self.set_layer_speed_rect = pygame.Rect(254, 231, 13, 12)
        
        self.blocks_interactables = {}
        self.selected_block = None

        x=0
        y=0
        page=0
        for tile in self.tiles:

            if str(page) not in self.blocks_interactables:
                self.blocks_interactables[str(page)] = {}
                self.all_pages.append(str(page))

            if 0 <= y <= 5:
                rect = self.tiles[tile].get_rect()
                rect.topleft = (8 + 17 * x, 44 + 15 * y)
            elif 6 <= y <= 7:
                rect = self.tiles[tile].get_rect()
                rect.topleft = (8 + 17 * x, 44 + 15 * y-1)
            elif 8 <= y <= 9:
                rect = self.tiles[tile].get_rect()
                rect.topleft = (8 + 17 * x, 44 + 15 * y-2)
            elif 10 <= y <= 11:
                rect = self.tiles[tile].get_rect()
                rect.topleft = (8 + 17 * x, 44 + 15 * y-3)

            self.blocks_interactables[str(page)][str(x)+";"+str(y)] = [tile, self.tiles[tile], rect]

            if x == 2:
                x = 0
                y += 1
            else:
                x += 1
            if y == 12:
                y = 0
                page += 1
                self.all_pages.append(str(page))

    def draw_editor(self, window_size):
        self.editormap = pygame.image.load("editor.png")

        self.levelmap.fill((0,0,0))
        self.draw_map(self.levelmap, tuple(self.camerapos))
        self.editormap.blit(self.levelmap, (60, 0))
        self.mouse_block_interaction(window_size)

        for pos in self.blocks_interactables[self.current_page]:
            pygame.draw.rect(self.editormap, (255,255,255), self.blocks_interactables[self.current_page][pos][2])
            self.editormap.blit(self.blocks_interactables[self.current_page][pos][1], self.blocks_interactables[self.current_page][pos][2])
        
        self.draw_layers()
    
    '''def block_collide(self, mousepos, screen_size):
        ratio_x = (screen_size[0] - 1) / 480
        ratio_y = (screen_size[1] - 1) / 280
        mousepos = (mousepos[0] / ratio_x, mousepos[1] / ratio_y)

        current_blocks = [self.blocks_interactables[self.current_page][pos][2] for pos in self.blocks_interactables[self.current_page]]
        mouserect = pygame.Rect(mousepos[0], mousepos[1], 1,1)'''

    def change_page(self, screen_size):
        mouseaction = pygame.mouse.get_pressed()
        mousepos = scale_mouse_pos(screen_size)

        left_arrow_rect = pygame.Rect(5, 22, 17, 17)
        right_arrow_rect = pygame.Rect(38, 22, 17, 17)

        if mouseaction[0] and right_arrow_rect.collidepoint(mousepos):
            self.all_pages = self.all_pages[1:] + [self.all_pages[0]]
            self.current_page = self.all_pages[0]

        if mouseaction[0] and left_arrow_rect.collidepoint(mousepos):
            self.all_pages = [self.all_pages[-1]] + self.all_pages[:-1]
            self.current_page = self.all_pages[0]

    def select_block(self, screen_size):
        mouseaction = pygame.mouse.get_pressed()
        mousepos = scale_mouse_pos(screen_size)

        if mouseaction[0] and (6 <= mousepos[0] <= 54 and 41 <= mousepos[1] <= 218): 
            selected_block = None
            for pos in self.blocks_interactables[self.current_page]:
                if self.blocks_interactables[self.current_page][pos][2].collidepoint(mousepos):
                    selected_block = self.blocks_interactables[self.current_page][pos][1]
            
            self.selected_block = selected_block         
    
    def mouse_block_interaction(self, screen_size):
        mousepos = scale_mouse_pos(screen_size)

        if 60 <= mousepos[0] <= 440 and 0 <= mousepos[1] <= 220:
            if self.selected_block != None:
                self.editormap.blit(self.selected_block, mousepos)

    def movecamera(self, mov):
        if mov["left"]:
            self.camerapos[0]+=1
        if mov["right"]:
            self.camerapos[0]-=1
        if mov["down"]:
            self.camerapos[1]-=1
        if mov["up"]:
            self.camerapos[1]+=1

    def draw_layers(self):
        c = 0
        for layer in sorted(self.all_layers):             

            self.editormap.blit(pygame.image.load("Assets\Layer.png"), (445, 22 + 12*c))
            
            if c%2 == 0:
                if int(layer) < 0:
                    self.editormap.blit(pygame.image.load(f"Assets\{str(layer)[0]}.png"), (467, 27 + 12*c))
                    self.editormap.blit(pygame.image.load(f"Assets\{str(layer)[1]}.png"), (470 - c, 22 + 12*c))
                else:
                    self.editormap.blit(pygame.image.load(f"Assets\{str(layer)}.png"), (472 - c, 22 + 12*c))
                c+=1
            else:
                if int(layer) < 0:
                    self.editormap.blit(pygame.image.load(f"Assets\{str(layer)[0]}.png"), (467, 27 + 12*c))
                    self.editormap.blit(pygame.image.load(f"Assets\{str(layer)[1]}.png"), (471 - c, 22 + 12*c))
                else:
                    self.editormap.blit(pygame.image.load(f"Assets\{str(layer)}.png"), (473 - c, 22 + 12*c))
                c+=1

            if str(layer) == str(self.current_layer):
                line = pygame.rect.Rect(443, 22+12*c-1-12,1,12)
                pygame.draw.rect(self.editormap, (255,215,0), line)
    
    def select_layer(self, screen_size):
        mouseaction = pygame.mouse.get_pressed()
        mousepos = scale_mouse_pos(screen_size)

        if mouseaction[0] == 1:
            for layerpos in range(len(self.all_layers)):
                if 443 <= mousepos[0] <= 479 and 22 + 12*layerpos <= mousepos[1] <= 21 + 12*layerpos + 11:
                    self.current_layer = sorted(list(self.all_layers.keys()))[layerpos]
    
    def update(self, keys, window_size):
        self.movecamera(keys)
        self.change_page(window_size)
        self.select_block(window_size)
        self.select_layer(window_size)
        self.draw_editor(window_size)

# 60 0
# 440 220