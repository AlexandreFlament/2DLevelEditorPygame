import pygame
from tile_map import TileMap


def scale_mouse_pos(screen_size):
    mousepos = list(pygame.mouse.get_pos())
    ratio_x = (screen_size[0] - 1) / 480
    ratio_y = (screen_size[1] - 1) / 280
    return mousepos[0] / ratio_x, mousepos[1] / ratio_y


class Editor(TileMap):
    def __init__(self, tile_size, tiles_file, image_file):
        super().__init__(tile_size, tiles_file, image_file)

        self.levelmap = pygame.Surface((380, 220))

        self.selectedblock = None
        self.current_layer = 0
        self.current_page = "0"
        self.current_category = "Images"
        self.categoryimg = pygame.image.load(f"Assets/{self.current_category}.png")
        self.all_blocks_pages = []
        self.all_images_pages = []
        self.camerapos = [0,0]
        self.opacity = True
        self.clicked = False
        self.hoverables = [[pygame.image.load("Assets/opacity_hover.png"), (221,295,226,241)],
        [pygame.image.load("Assets/remove_hover.png"), (141,180,241,253)],
        [pygame.image.load("Assets/clear_hover.png"), (184,210,241,253)],
        [pygame.image.load("Assets/uncheck_hover.png"), (121,132,251,262)],
        [pygame.image.load("Assets/check_hover.png"), (199,210,258,269)]
        ]

        self.options = {
            "addlayer": {
                "layer":["0","1","2","3","4","5","-5","-4","-3","-2","-1"], 
                "speed":["1.0", "1.5","0.5"]
                },
            "currentlayer":{
                "speed":["1.0", "1.5","0.5"]
                }
        }

        self.add_layer_rect = pygame.Rect(145, 231, 13, 12)
        self.remove_layer_rect = pygame.Rect(145, 245, 13, 12)
        self.move_to_layer_rect = pygame.Rect(145, 259, 13, 12)
        self.set_layer_speed_rect = pygame.Rect(254, 231, 13, 12)
        
        ### INIT BLOCKS
        self.blocks_interactables = {}
        self.selected_block = None

        x,y,page=0,0,0
        for tile in self.tiles:
            if str(page) not in self.blocks_interactables:
                self.blocks_interactables[str(page)] = {}
                self.all_blocks_pages.append(str(page))

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
                self.all_blocks_pages.append(str(page))

        ### INIT IMAGES
        self.images_interactables = {}
        self.selected_image = None

        x,y,page=0,0,0
        for image in self.mini:

            if str(page) not in self.images_interactables:
                self.images_interactables[str(page)] = {}
                self.all_images_pages.append(str(page))

            if 0 <= y <= 5:
                rect = self.mini[image].get_rect()
                rect.topleft = (8 + 17 * x, 44 + 15 * y)
            elif 6 <= y <= 7:
                rect = self.mini[image].get_rect()
                rect.topleft = (8 + 17 * x, 44 + 15 * y-1)
            elif 8 <= y <= 9:
                rect = self.mini[image].get_rect()
                rect.topleft = (8 + 17 * x, 44 + 15 * y-2)
            elif 10 <= y <= 11:
                rect = self.mini[image].get_rect()
                rect.topleft = (8 + 17 * x, 44 + 15 * y-3)

            self.images_interactables[str(page)][str(x)+";"+str(y)] = [image, self.mini[image], rect]
            
            if x == 2:
                x = 0
                y += 1
            else:
                x += 1
            if y == 12:
                y = 0
                page += 1
                self.all_images_pages.append(str(page))


    ###################################################   DRAW ED   ###################################################


    def draw_editor(self):
        self.editormap = pygame.image.load("editor.png")

        self.levelmap.fill((0,0,0))
        self.draw_map(self.levelmap, tuple(self.camerapos))
        self.editormap.blit(self.levelmap, (60, 0))
        self.editormap.blit(self.categoryimg, (14,4))

        if self.current_category == "Tiles":
            self.mouse_block_interaction()
            for pos in self.blocks_interactables[self.current_page]:
                pygame.draw.rect(self.editormap, (255,255,255), self.blocks_interactables[self.current_page][pos][2])
                self.editormap.blit(self.blocks_interactables[self.current_page][pos][1], self.blocks_interactables[self.current_page][pos][2])
        if self.current_category == "Images":
            self.mouse_image_interaction()
            for pos in self.images_interactables[self.current_page]:
                pygame.draw.rect(self.editormap, (255,255,255), self.images_interactables[self.current_page][pos][2])
                self.editormap.blit(self.images_interactables[self.current_page][pos][1], self.images_interactables[self.current_page][pos][2])

        self.draw_layers()


    ###################################################   BLOCKS   ###################################################


    def change_block_page(self):
        left_arrow_rect = pygame.Rect(5, 22, 17, 17)
        right_arrow_rect = pygame.Rect(38, 22, 17, 17)

        if self.mouseaction[0] and right_arrow_rect.collidepoint(self.mousepos) and not self.clicked:
            self.all_blocks_pages = self.all_blocks_pages[1:] + [self.all_blocks_pages[0]]
            self.current_page = self.all_blocks_pages[0]

        if self.mouseaction[0] and left_arrow_rect.collidepoint(self.mousepos) and not self.clicked:
            self.all_blocks_pages = [self.all_blocks_pages[-1]] + self.all_blocks_pages[:-1]
            self.current_page = self.all_blocks_pages[0]

    def select_block(self):
        if self.mouseaction[0] and (6 <= self.mousepos[0] <= 54 and 41 <= self.mousepos[1] <= 218): 
            selected_block = None
            selected_block_type = None
            for pos in self.blocks_interactables[self.current_page]:
                if self.blocks_interactables[self.current_page][pos][2].collidepoint(self.mousepos):
                    selected_block = self.blocks_interactables[self.current_page][pos][1]
                    selected_block_type = self.blocks_interactables[self.current_page][pos][0]
            self.selected_block = selected_block         
            self.selected_block_type = selected_block_type
    
    def mouse_block_interaction(self):
        layerspeed = self.all_layers[str(self.current_layer)]["layerspeed"]
        x = (self.mousepos[0]-60)
        y = (self.mousepos[1])
        x = (x - x % self.tile_size) / self.tile_size + self.camerapos[0] * self.all_layers[str(self.current_layer)]["layerspeed"]
        y = (y - y % self.tile_size) / self.tile_size + self.camerapos[1] * self.all_layers[str(self.current_layer)]["layerspeed"]

        if 60 <= self.mousepos[0] <= 440 and 0 <= self.mousepos[1] <= 220:
            if self.selected_block != None:
                self.editormap.blit(self.selected_block, (self.mousepos[0] - self.mousepos[0]%10 , self.mousepos[1] - self.mousepos[1]%10))
                
                if self.mouseaction[0] and not self.clicked:
                    if self.add_tile(self.selected_block_type, (x,y), self.current_layer):
                        print(f"Place | Block type: {self.selected_block_type} | Layer: {self.current_layer} | Layer speed: {layerspeed} | x: {x} y: {y} | Camera pos: {self.camerapos}")

                if self.mouseaction[1]:
                    self.selected_block = None
                    self.selected_block_type = None

            if self.mouseaction[2]:
                if self.remove_tile((x,y), self.current_layer):
                    print(f"Remove | Layer: {self.current_layer} | x: {x} y: {y} | Camera pos: {self.camerapos}")


    ###################################################   IMAGES   ###################################################


    def change_image_page(self):
        left_arrow_rect = pygame.Rect(5, 22, 17, 17)
        right_arrow_rect = pygame.Rect(38, 22, 17, 17)

        if self.mouseaction[0] and right_arrow_rect.collidepoint(self.mousepos) and not self.clicked:
            self.all_images_pages = self.all_images_pages[1:] + [self.all_images_pages[0]]
            self.current_page = self.all_images_pages[0]

        if self.mouseaction[0] and left_arrow_rect.collidepoint(self.mousepos) and not self.clicked:
            self.all_images_pages = [self.all_images_pages[-1]] + self.all_images_pages[:-1]
            self.current_page = self.all_images_pages[0]
    
    def select_image(self):
        if self.mouseaction[0] and (6 <= self.mousepos[0] <= 54 and 41 <= self.mousepos[1] <= 218): 
            selected_image = None
            selected_image_type = None
            for pos in self.images_interactables[self.current_page]:
                if self.images_interactables[self.current_page][pos][2].collidepoint(self.mousepos):
                    selected_image_type = self.images_interactables[self.current_page][pos][0]
                    selected_image = self.images[selected_image_type]
            self.selected_image = selected_image
            self.selected_image_type = selected_image_type
    
    def mouse_image_interaction(self):
        layerspeed = self.all_layers[str(self.current_layer)]["layerspeed"]
        x = (self.mousepos[0]-60)
        y = (self.mousepos[1])
        x = (x - x % self.tile_size) / self.tile_size + self.camerapos[0] * self.all_layers[str(self.current_layer)]["layerspeed"]
        y = (y - y % self.tile_size) / self.tile_size + self.camerapos[1] * self.all_layers[str(self.current_layer)]["layerspeed"]

        if 60 <= self.mousepos[0] <= 440 and 0 <= self.mousepos[1] <= 220:
            if self.selected_image != None:
                self.editormap.blit(self.selected_image, (self.mousepos[0] - self.mousepos[0]%10 , self.mousepos[1] - self.mousepos[1]%10))

                if self.mouseaction[0] and not self.clicked:
                    if self.add_tile(self.selected_image_type, (x,y), self.current_layer):
                        print(f"Place | Image type: {self.selected_image_type} | Layer: {self.current_layer} | Layer speed: {layerspeed} | x: {x} y: {y} | Camera pos: {self.camerapos}")

                if self.mouseaction[1]:
                    self.selected_image = None
                    self.selected_image_type = None

            if self.mouseaction[2]:
                if self.remove_tile((x,y), self.current_layer):
                    print(f"Remove | Layer: {self.current_layer} | x: {x} y: {y} | Camera pos: {self.camerapos}")


    ###################################################   LAYERS   ###################################################


    def draw_layers(self):
        c = 0
        for layer in sorted(self.all_layers):             

            self.editormap.blit(pygame.image.load("Assets\Layer.png"), (445, 22 + 12*c))
            
            if int(layer) < 0:
                self.editormap.blit(pygame.image.load(f"Assets\{str(layer)[0]}.png"), (467, 27 + 12*c))
                self.editormap.blit(pygame.image.load(f"Assets\{str(layer)[1]}.png"), (470, 22 + 12*c))
            else:
                self.editormap.blit(pygame.image.load(f"Assets\{str(layer)}.png"), (470, 22 + 12*c))
            c+=1

            if str(layer) == str(self.current_layer):
                line = pygame.rect.Rect(443, 22+12*c-1-12,1,12)
                pygame.draw.rect(self.editormap, (255,215,0), line)
    
    def select_layer(self):
        if self.mouseaction[0] == 1:
            for layerpos in range(len(self.all_layers)):
                if 443 <= self.mousepos[0] <= 479 and 22 + 12*layerpos <= self.mousepos[1] <= 21 + 12*layerpos + 11:
                    self.current_layer = sorted(list(self.all_layers.keys()))[layerpos]
    
    def addlayer(self, wheel):
        if 97 <= self.mousepos[0] <= 114 and 243 <= self.mousepos[1] <= 255:
            if wheel < 0 and self.options["addlayer"]["layer"][0] != "-5":
                self.options["addlayer"]["layer"] = [self.options["addlayer"]["layer"][-1]] + self.options["addlayer"]["layer"][:-1]
            if wheel > 0 and self.options["addlayer"]["layer"][0] != "5":
                self.options["addlayer"]["layer"] = self.options["addlayer"]["layer"][1:] + [self.options["addlayer"]["layer"][0]]
        if 97 <= self.mousepos[0] <= 114 and 258 <= self.mousepos[1] <= 270:
            if wheel < 0 and self.options["addlayer"]["speed"][0] != "0.5":
                self.options["addlayer"]["speed"] = [self.options["addlayer"]["speed"][-1]] + self.options["addlayer"]["speed"][:-1]
            if wheel > 0 and self.options["addlayer"]["speed"][0] != "1.5":
                self.options["addlayer"]["speed"] = self.options["addlayer"]["speed"][1:] + [self.options["addlayer"]["speed"][0]]
        
        if self.options["addlayer"]["layer"][0] not in self.all_layers: 
            self.editormap.blit(pygame.image.load("Assets/check.png"), (121,251))
            self.hoverables[3] = [pygame.image.load("Assets/check_hover.png"), (121,132,251,262)]

            if self.mouseaction[0] and 121 <= self.mousepos[0] <= 132 and 251 <= self.mousepos[1] <= 262:
                self.add_layer(self.options["addlayer"]["layer"][0], float(self.options["addlayer"]["speed"][0]))
                self.hoverables[3] = [pygame.image.load("Assets/uncheck_hover.png"), (121,132,251,262)]
        
        nb = self.options["addlayer"]["layer"][0]
        if nb[0] == "-":
            self.editormap.blit(pygame.image.load("Assets/-.png"), (103,248))
            self.editormap.blit(pygame.image.load(f"Assets/{nb[1]}.png"), (107,245))
        else:
            self.editormap.blit(pygame.image.load(f"Assets/{nb[0]}.png"), (107,245))

        nb = self.options["addlayer"]["speed"][0]
        self.editormap.blit(pygame.image.load(f"Assets/{nb[0]}.png"), (99,260))
        self.editormap.blit(pygame.image.load(f"Assets/{nb[2]}.png"), (107,260))

    def currentlayer(self, wheel):
        if self.mouseaction[0]:
            if 141 <= self.mousepos[0] <= 180 and 241 <= self.mousepos[1] <= 253 and not self.clicked and self.current_layer != 0:
                del self.tile_map[str(self.current_layer)]
                del self.all_layers[str(self.current_layer)]
                self.current_layer = 0
            if 184 <= self.mousepos[0] <= 210 and 241 <= self.mousepos[1] <= 253 and not self.clicked:
                self.tile_map[str(self.current_layer)] = {}
            if 199 <= self.mousepos[0] <= 210 and 258 <= self.mousepos[1] <= 269 and self.current_layer != 0:
                self.all_layers[str(self.current_layer)]["layerspeed"] = float(self.options["currentlayer"]["speed"][0])
                self.all_layers = sorted(self.all_layers)

        if 175 <= self.mousepos[0] <= 192 and 258 <= self.mousepos[1] <= 270:
            if wheel < 0 and self.options["currentlayer"]["speed"][0] != "0.5":
                self.options["currentlayer"]["speed"] = [self.options["currentlayer"]["speed"][-1]] + self.options["currentlayer"]["speed"][:-1]
            if wheel > 0 and self.options["currentlayer"]["speed"][0] != "1.5":
                self.options["currentlayer"]["speed"] = self.options["currentlayer"]["speed"][1:] + [self.options["currentlayer"]["speed"][0]]
        
        nb = self.options["currentlayer"]["speed"][0]
        self.editormap.blit(pygame.image.load(f"Assets/{nb[0]}.png"), (177,260))
        self.editormap.blit(pygame.image.load(f"Assets/{nb[2]}.png"), (185,260))
             

    ###################################################   OTHERS   ###################################################

   
    def movecamera(self, mov):
        if mov["right"]:
            self.camerapos[0] += 1
        if mov["left"]:
            self.camerapos[0] -= 1
        if mov["up"]:
            self.camerapos[1] -= 1
        if mov["down"]:
            self.camerapos[1] += 1

    def toggle_opacity(self):
        if self.mouseaction[0] == 1 and not self.clicked:
            if 221 <= self.mousepos[0] <= 295 and 226 <= self.mousepos[1] <= 241:
                self.opacity = not self.opacity

    def category_changer(self):
        if (4 <= self.mousepos[0] <= 14 and 4 <= self.mousepos[1] <= 13) or (46 <= self.mousepos[0] <= 56 and 4 <= self.mousepos[1] <= 13):
            if self.mouseaction[0] == 1 and not self.clicked:
                if self.current_category == "Images":
                    self.current_category = "Tiles"
                    self.categoryimg = pygame.image.load("Assets/Blocks.png")
                else:
                    self.current_category = "Images"
                    self.categoryimg = pygame.image.load("Assets/Images.png")

    ###################################################   HANDLERS   ###################################################


    def mouse_handler(self, screen_size):
        self.mouseaction = pygame.mouse.get_pressed()
        self.mousepos = scale_mouse_pos(screen_size)

    def click_handler(self):
        if self.mouseaction[0]:
            self.clicked = True
        else:
            self.clicked = False
    
    def hover_handler(self):
        for L in self.hoverables:
            if L[1][0] <= self.mousepos[0] <= L[1][1] and L[1][2] <= self.mousepos[1] <= L[1][3]:
                self.editormap.blit(L[0], (L[1][0], L[1][2]))


    ###################################################   UPDATE   ###################################################


    def update(self, keys, window_size):
        self.mouse_handler(window_size)
        self.movecamera(keys)
        if self.current_category == "Tiles":
            self.change_block_page()
            self.select_block()
        if self.current_category == "Images":
            self.change_image_page()
            self.select_image()
        self.select_layer()
        self.toggle_opacity()
        self.draw_editor()
        self.addlayer(keys["Wheel"])
        self.currentlayer(keys["Wheel"])
        self.category_changer()
        self.click_handler()
        self.hover_handler()


# 60 0
# 440 220