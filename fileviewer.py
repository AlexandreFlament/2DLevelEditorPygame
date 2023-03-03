import pygame,os, json, level_editor_test
from pygame.locals import *
pygame.init()

def scale_mouse_pos(screen_size):
    mousepos = list(pygame.mouse.get_pos())
    ratio_x = (screen_size[0] - 1) / 480
    ratio_y = (screen_size[1] - 1) / 280
    return mousepos[0] / ratio_x, mousepos[1] / ratio_y

class FileViewer():

    def __init__(self,file):
        self.running = True

        self.mousepos = [-1,-1]
        self.mouseaction = [False, False]
        self.clicked = False

        self.naming = False
        self.name = ""
        self.inputactive = False

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

        self.hoverables = [[pygame.image.load("Assets/FileViewer/load_hover.png"), (6,52,6,22)],
        [pygame.image.load("Assets/FileViewer/delete_hover.png"), (59,131,6,22)],
        [pygame.image.load("Assets/FileViewer/clear_hover.png"), (6,66,25,41)],
        [pygame.image.load("Assets/FileViewer/create_hover.png"), (69,144,25,41)]
        ]


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


    ###################################################   BUTTONS   ###################################################


    def deletef(self):
        if 59 <= self.mousepos[0] <= 131 and 6 <= self.mousepos[1] <= 22 and self.mouseaction[0] and self.selectedfile != None and not self.clicked:
            os.remove(f"Saves/{self.selectedfile}")
            self.files.remove(self.selectedfile)
            self.nblayers = "N/A"
            self.nbblocks = "N/A"
            self.initpos = "N/A"
            self.sizeoffile = "N/A"

    def clearf(self):
        if 6 <= self.mousepos[0] <= 66 and 25 <= self.mousepos[1] <= 41 and self.mouseaction[0] and self.selectedfile != None and not self.clicked:
            with open(f"Saves/{self.selectedfile}", 'w') as f:
                json.dump({"map": {"0": {}}, "all_layers": {"0": {"layerspeed": 1.0}}, "camera_pos": [0, 0]}, f)
            self.nblayers = "1"
            self.nbblocks = "0"
            self.initpos = "0, 0"
            self.sizeoffile = self.filesize
    
    def loadf(self):
        if self.nbblocks == "N/A" or self.nblayers == "N/A" or self.initpos == "N/A" or self.sizeoffile == "N/A" or self.nbblocks == "ERR" or self.nblayers == "ERR" or self.initpos == "ERR" or self.sizeoffile == "ERR" or self.selectedfile == None:
            return
        
        if 6 <= self.mousepos[0] <= 56 and 6 <= self.mousepos[1] <= 22 and self.mouseaction[0] and not self.clicked:
            level_editor_test.main(f"Saves/{self.selectedfile}")

    def createf(self, unicode): # 6 22 | popup
        if (69 <= self.mousepos[0] <= 144 and 25 <= self.mousepos[1] <= 41 and self.mouseaction[0] and not self.clicked) or self.naming:
            self.naming = True

            popupsurface = pygame.Surface((108,40))
            popup = pygame.image.load("Assets/FileViewer/create_popup.png")

            popupsurface.blit(popup,(0,0))
            popupsurface.blit(self.font.render(self.name,False,(0,0,0)), (5,22))
            self.surface.blit(popupsurface, (186,110))

            if unicode == '\b':
                self.name = self.name[:-1]
            elif unicode == '\r' and self.name+".json" not in self.files:
                self.naming = False
            elif type(unicode) != str:
                self.inputactive = False
            elif unicode in "azertyuiopqsdfghjklmwxcvbnAZERTYUIOPQSDFGHJKLMWXCVBN0123456789" and len(self.name) < 9 and not self.inputactive:
                self.name += unicode
                self.inputactive = True

            if self.name != "" and not self.naming:
                with open("Saves/"+self.name+".json", 'w') as f:
                    json.dump({"map": {"0": {}}, "all_layers": {"0": {"layerspeed": 1.0}}, "camera_pos": [0, 0]}, f)

                self.files = [self.name+".json"] + self.files
                self.selectedfile = self.name+".json"

                self.nblayers = "1"
                self.nbblocks = "0"
                self.initpos = "0, 0"
                self.sizeoffile = self.filesize

                self.name = ""


    ###################################################   OTHERS   ###################################################


    def choosefile(self):
        if 3 <= self.mousepos[0] <= 382 and 46 <= self.mousepos[1] <= 277 and self.mouseaction[0] and not self.clicked:
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
    
    def hover_handler(self):
        for L in self.hoverables:
            if L[1][0] <= self.mousepos[0] <= L[1][1] and L[1][2] <= self.mousepos[1] <= L[1][3]:
                self.surface.blit(L[0], (L[1][0], L[1][2]))


    ###################################################   UPDATE   ###################################################


    def update(self, window_size, keys):
        self.mouse_handler(window_size)

        self.draw()

        if not self.naming:
            self.deletef()
            self.clearf()
            self.loadf()
            self.createf(keys["unicode"])

            self.choosefile()
        else:
            self.createf(keys["unicode"])

        self.files_handler(keys["wheel"])
        self.click_handler()
        self.hover_handler()

fv = FileViewer("Saves/")