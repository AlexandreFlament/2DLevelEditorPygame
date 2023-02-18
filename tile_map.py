import pygame, json, os

def blit_alpha(target, source, location, opacity):
        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)        
        target.blit(temp, location)

class TileMap():

    def __init__(self, tile_size, tiles_file):

        self.tile_size = tile_size
        self.nbr_x_tiles = 380/self.tile_size
        self.nbr_y_tiles = 240/self.tile_size
        self.tiles_file = tiles_file

        self.tiles = {".".join(f.split(".")[:-1]):pygame.image.load(self.tiles_file+f) for f in os.listdir(self.tiles_file)}

        self.tile_map = {}
        self.all_layers = {}
        self.collidables = []
        self.current_layer = None

        self.loaded_map = None

    def load_map(self, path):
        with open(path, 'r') as f:
            json_data = json.load(f)
        
        self.tile_map = json_data['map']
        self.all_layers = json_data['all_layers']

        self.loaded_map = path

    def save_map(self, path):
        with open(path, "w") as f:
            json.dump({"map":self.tile_map, "all_layers":self.all_layers}, f)
    
    def draw_map(self, display, playerpos):
        self.collidables = []

        for layer in sorted(self.all_layers):
            #print(f"            LAYER {layer}")
            for tile in self.tile_map[layer].values():

                if self.all_layers[layer]["layerspeed"] < 1:
                    addedlayerspeedx = + (tile["pos"][0] / 2 * self.tile_size)
                    addedlayerspeedy = + (tile["pos"][1] / 2 * self.tile_size)
                elif self.all_layers[layer]["layerspeed"] == 1:
                    addedlayerspeedx = 0
                    addedlayerspeedy = 0
                else:
                    addedlayerspeedx = - (tile["pos"][0] / 2 * self.tile_size)
                    addedlayerspeedy = - (tile["pos"][1] / 2 * self.tile_size)

                x = (tile["pos"][0] - playerpos[0]) * self.tile_size * self.all_layers[layer]["layerspeed"] + addedlayerspeedx
                y = (tile["pos"][1] - playerpos[1]) * self.tile_size * self.all_layers[layer]["layerspeed"] + addedlayerspeedy

                if -10 <= x <= 390 and -10 <= y <= 250:

                    if self.current_layer == None or int(layer) == int(self.current_layer):
                        display.blit(self.tiles[tile["type"]], (x, y))
                    else:
                        if self.opacity:
                            blit_alpha(display, self.tiles[tile["type"]], (x,y), 100)
                        else:
                            display.blit(self.tiles[tile["type"]], (x, y))
                
                    if tile["layer"] == 0:
                        rect = self.tiles[tile["type"]].get_rect()
                        rect.topleft = (x, y)
                        self.collidables.append(rect)
                    #print("Layer: ",layer," | Current pos: ",[x/10,y/10], " | Tile pos: ", tile["pos"], "| Type: ", tile["type"])
            #print("-------------------------------")
        #print('===============================')
                
    
    def collides(self, rect):
        collisionindex = pygame.Rect.collidelist(rect, self.collidables)
        if collisionindex == -1:
            return False
        return True
    
    def add_tile(self, type, pos, layer=None):
        if layer == None:
            layer = self.current_layer
        
        self.tile_map[str(layer)][str(pos[0])+";"+str(pos[1])] = {"type": type, "pos": list(pos), "layer": layer}

        if str(layer) not in self.all_layers:
            self.add_layer(layer)

        return True

    def add_layer(self, layer, layerspeed):
        if str(layer) in self.all_layers:
            return False
        
        self.all_layers[str(layer)] = {"layerspeed":layerspeed}
        self.tile_map[str(layer)] = {}

        return True
    
    def remove_tile(self, pos, layer=None):
        if layer == None:
            layer = self.current_layer
        if str(pos[0])+";"+str(pos[1]) not in self.tile_map[str(layer)]:
            return False
        
        del self.tile_map[str(layer)][str(pos[0])+";"+str(pos[1])]

        return True

    def remove_layer(self, layer):
        if layer not in self.all_layers:
            return False

        self.all_layers.remove(layer)
        del self.tile_map[str(layer)]

        return True

