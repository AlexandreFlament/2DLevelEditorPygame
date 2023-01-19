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
        self.nbr_x_tiles = 320/self.tile_size
        self.nbr_y_tiles = 240/self.tile_size
        self.tiles_file = tiles_file

        self.tiles = {".".join(f.split(".")[:-1]):pygame.image.load(self.tiles_file+f) for f in os.listdir(self.tiles_file)}

        self.tile_map = {}
        self.all_layers = {}
        self.collidables = []
        self.current_layer = None

    def load_map(self, path):
        with open(path, 'r') as f:
            json_data = json.load(f)
        
        self.tile_map = json_data['map']
        self.all_layers = json_data['all_layers']

    def save_map(self, path):
        with open(path, "w") as f:
            json.dump({"map":self.tile_map, "all_layers":self.all_layers}, f)
    
    def draw_map(self, display, playerpos):
        self.collidables = []

        for layer in sorted(self.all_layers):
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

                if 0 <= x <= 320 and 0 <= y <= 240:

                    if self.current_layer == None or layer == self.current_layer:
                        display.blit(self.tiles[tile["type"]], (x, y))
                    else:
                        blit_alpha(display, self.tiles[tile["type"]], (x,y), 128)
                
                    if tile["layer"] == 0:
                        rect = self.tiles[tile["type"]].get_rect()
                        rect.topleft = (x, y)
                        self.collidables.append(rect)
                
    
    def collides(self, rect):
        collisionindex = pygame.Rect.collidelist(rect, self.collidables)
        if collisionindex == -1:
            return False
        return True
    
    def add_tile(self, type, pos, layer=None):
        if layer == None:
            layer = self.current_layer
        if type not in self.tiles:
            return False
        self.tile_map[str(layer)][str(pos[0])+";"+str(pos[1])] = {"type": type, "pos": list(pos), "layer": layer}
        if layer not in self.all_layers:
            self.all_layers.append(layer)
    
    def add_layer(self, layer):
        if layer in self.all_layers:
            return False
        
        self.all_layers.append(int(layer))
        self.tile_map[str(layer)] = {}
    
    def remove_tile(self, pos, layer=None):
        if layer == None:
            layer = self.current_layer
        if str(pos[0])+";"+str(pos[1]) not in self.tile_map[str(layer)]:
            return False
        
        del self.tile_map[str(layer)][str(pos[0])+";"+str(pos[1])]

    def remove_layer(self, layer):
        if layer not in self.all_layers:
            return False

        self.all_layers.remove(layer)
        del self.tile_map[str(layer)]

