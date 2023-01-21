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
        self.all_pages = []
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
                self.all_pages.append(str(page))

            rect = self.tiles[tile].get_rect()
            rect.topleft = (8 + 17 * x, 44 + 15 * y)
            self.blocks_interactables[str(page)][str(8 + 17 * x)+";"+str(44 + 15 * y)] = [tile, self.tiles[tile], rect]
            
            if x == 2:
                x = 0
                y += 1
            else:
                x += 1
            if y == 12:
                y = 0
                page += 1
                self.all_pages.append(str(page))
            
            


    def draw_editor(self):
        self.levelmap.fill((0,0,0))
        self.draw_map(self.levelmap, tuple(self.camerapos))
        self.editormap.blit(self.levelmap, (60, 0))

        for pos in self.blocks_interactables[self.current_page]:
            pygame.draw.rect(self.editormap, (255,255,255), self.blocks_interactables[self.current_page][pos][2])
            self.editormap.blit(self.blocks_interactables[self.current_page][pos][1], self.blocks_interactables[self.current_page][pos][2])
    
    def block_collide(self, mousepos):
        current_blocks = [self.blocks_interactables[self.current_page][2] for coord in self.blocks_interactables[self.current_page] ]
        mouserect = pygame.Rect(mousepos[0], mousepos[1], 1,1)
        print(pygame.Rect.collidelistall(mousepos, current_blocks))

    def change_page(self, screen_size):  # put after display scaling
        mousepos = pygame.mouse.get_pos()
        mouseaction = pygame.mouse.get_pressed()

        right_arrow_rect = pygame.Rect(38, 22, 17, 17).inflate(screen_size[0]/320, screen_size[1]/240)
        left_arrow_rect = pygame.Rect(5, 22, 17, 17).inflate(screen_size[0]/320, screen_size[1]/240)


        print(mouseaction[0], left_arrow_rect.collidepoint(mousepos), right_arrow_rect.collidepoint(mousepos), mousepos)

        if mouseaction[0] and right_arrow_rect.collidepoint(mousepos):
            self.all_pages = self.all_pages[1:] + [self.all_pages[0]]
            self.current_page = self.all_pages[0]

        if mouseaction[0] and left_arrow_rect.collidepoint(mousepos):
            self.all_pages = [self.all_pages[-1]] + self.all_pages[:-1]
            self.current_page = self.all_pages[0]

    def movecamera(self, mov):
        if mov["left"]:
            self.camerapos[0]+=1
        if mov["right"]:
            self.camerapos[0]-=1
        if mov["down"]:
            self.camerapos[1]-=1
        if mov["up"]:
            self.camerapos[1]+=1