import pygame,os, json
pygame.init()

def scale_mouse_pos(screen_size):
    mousepos = list(pygame.mouse.get_pos())
    ratio_x = (screen_size[0] - 1) / 480
    ratio_y = (screen_size[1] - 1) / 280
    return mousepos[0] / ratio_x, mousepos[1] / ratio_y

class FileViewer():

    def __init__(self,file):

        self.mousepos = [-1,-1]
        self.mouseaction = [False, False]
        self.clicked = False

        self.file = file
        self.files = os.listdir(file)
        self.initfstfile = self.files[0] 

        self.font = pygame.font.Font("PixelFont.ttf", 15)
        self.fvimg = pygame.image.load("fileviewer.png")

        self.selectedfile = None
        self.selectedfiledata = None
        self.nblayers = "N/A"
        self.nbblocks = "N/A"
        self.initpos = "N/A"


    ###################################################   DRAW FV   ###################################################


    def draw(self):
        self.surface = pygame.Surface((480,280))
        self.surface.blit(self.fvimg, (0,0))

        self.draw_files()

    def draw_files(self):
        lenselffiles = len(self.files)
        if lenselffiles>10:
            lenselffiles = 10
        
        for i in range(lenselffiles):
            txt = self.font.render(self.files[i],False,(0,0,0),(255,0,0) if self.selectedfile == self.files[i] else (255,255,255))
            self.surface.blit(txt, (8, 50+23*i))


    ###################################################   OTHERS   ###################################################


    def choosefile(self):
        if 3 <= self.mousepos[0] <= 382 and 46 <= self.mousepos[1] <= 277 and self.mouseaction[0]:
            y = (self.mousepos[1]-46)//23
            self.selectedfile = self.files[int(y)]
            with open(f"Saves/{self.selectedfile}.json", 'r') as f:
                self.selectedfiledata = json.load(f)
            
            self.nblayers = self.nbroflayers
            self.nbblocks = self.nbrofblcks
            self.initpos = self.campos

        if self.mouseaction[1]:
            self.selectedfile = None
            self.selectedfiledata = None
            self.nblayers = "N/A"
            self.nbblocks = "N/A"
            self.initpos = "N/A"


    ###################################################   SAVESDATA   ###################################################

    @property
    def nbrofblcks(self):
        if self.selectedfiledata == None:
            return "N/A"
        ln = 0
        for lyer in self.selectedfiledata["map"]:
            ln += len(self.selectedfiledata["map"][lyer])
        return str(ln)
    
    @property
    def nbroflayers(self):
        if self.selectedfiledata == None:
            return "N/A"
        return str(len(self.selectedfiledata["all_layers"]))
    
    @property
    def campos(self):
        if self.selectedfiledata == None:
            return "N/A"
        return str(self.selectedfiledata["camera_pos"][0]) + ", " + str(self.selectedfiledata["camera_pos"][1])


    ###################################################   HANDLERS   ###################################################


    def files_handler(self,wheel):
        if wheel>0:
            self.files = [self.files[-1]] + self.files[0:-1]
        if wheel<0:
            self.files = self.files[1:] + [self.files[0]]

    def mouse_handler(self, screen_size):
        self.mouseaction = pygame.mouse.get_pressed()
        self.mousepos = scale_mouse_pos(screen_size)

    def click_handler(self):
        if self.mouseaction[0]:
            self.clicked = True
        else:
            self.clicked = False


    ###################################################   UPDATE   ###################################################


    def update(self, window_size, keys):
        self.draw()

        self.choosefile()

        self.files_handler(keys["wheel"])
        self.mouse_handler(window_size)
        self.click_handler()

fv = FileViewer("Saves/")