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
        self.sizeoffile = "N/A"


    ###################################################   DRAW FV   ###################################################


    def draw(self):
        self.surface = pygame.Surface((480,280))
        self.surface.blit(self.fvimg, (0,0))

        self.draw_files()
        self.draw_save_data()

    def draw_files(self):
        lenselffiles = len(self.files)
        if lenselffiles>10:
            lenselffiles = 10
        
        for i in range(lenselffiles):
            txt = self.font.render(self.files[i],False,(0,0,0),(255,0,0) if self.selectedfile == self.files[i] else (255,255,255))
            self.surface.blit(txt, (8, 50+23*i))
    
    def draw_save_data(self):
        
        # BLOCKS
        self.surface.blit(self.font.render("Nbr of", False,(0,0,0),(255,255,255)), (388,49))
        self.surface.blit(self.font.render("blocks:", False,(0,0,0),(255,255,255)), (388,66))
        self.surface.blit(self.font.render(self.nbblocks, False,(0,0,0),(255,255,255)), (388,83))

        # LAYERS
        self.surface.blit(self.font.render("Nbr of", False,(0,0,0),(255,255,255)), (388,110))
        self.surface.blit(self.font.render("layers:", False,(0,0,0),(255,255,255)), (388,127))
        self.surface.blit(self.font.render(self.nblayers, False,(0,0,0),(255,255,255)), (388,144))

        # Camera pos
        self.surface.blit(self.font.render("Base pos", False,(0,0,0),(255,255,255)), (388,171))
        self.surface.blit(self.font.render("of cam:", False,(0,0,0),(255,255,255)), (388,188))
        self.surface.blit(self.font.render(self.initpos, False,(0,0,0),(255,255,255)), (388,205))

        # File size
        self.surface.blit(self.font.render("Size:", False,(0,0,0),(255,255,255)), (388,232))
        self.surface.blit(self.font.render(self.sizeoffile, False,(0,0,0),(255,255,255)), (388,249))


    ###################################################   OTHERS   ###################################################


    def choosefile(self):
        if 3 <= self.mousepos[0] <= 382 and 46 <= self.mousepos[1] <= 277 and self.mouseaction[0]:
            y = (self.mousepos[1]-46)//23
            self.selectedfile = self.files[int(y)]
            with open(f"Saves/{self.selectedfile}", 'r') as f:
                try:
                    self.selectedfiledata = json.load(f)
                except:
                    self.selectedfiledata = {}
            
            self.nblayers = self.nbroflayers
            self.nbblocks = self.nbrofblcks
            self.initpos = self.campos
            self.sizeoffile = self.filesize

        if self.mouseaction[1]:
            self.selectedfile = None
            self.selectedfiledata = None
            self.nblayers = "N/A"
            self.nbblocks = "N/A"
            self.initpos = "N/A"
            self.sizeoffile = "N/A"


    ###################################################   SAVESDATA   ###################################################

    @property
    def nbrofblcks(self):
        if self.selectedfiledata == None:
            return "N/A"
        ln = 0
        try:
            for lyer in self.selectedfiledata["map"]:
                ln += len(self.selectedfiledata["map"][lyer])
            return str(ln)
        except:
            return "ERR"
    
    @property
    def nbroflayers(self):
        if self.selectedfiledata == None:
            return "N/A"
        try:
            return str(len(self.selectedfiledata["all_layers"]))
        except:
            return "ERR"
        
    @property
    def campos(self):
        if self.selectedfiledata == None:
            return "N/A"
        try:
            return str(int(self.selectedfiledata["camera_pos"][0])) + ", " + str(int(self.selectedfiledata["camera_pos"][1]))
        except:
            return "ERR"
        
    @property
    def filesize(self):
        if self.selectedfile == None:
            return "N/A"
        try:
            size = int(os.stat(f"Saves/{self.selectedfile}").st_size)
        except:
            return "ERR"
        for x in ['B', 'KB', 'MB']:
            if size < 1024:
                return str(int(size))+" "+x
            size /= 1024


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