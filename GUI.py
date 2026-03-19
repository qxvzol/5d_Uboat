import pygame
import math

class TimelineUI:

    def __init__(self, width=1024, height=1024):

        self.WIDTH = width
        self.HEIGHT = height

        pygame.font.init()
        self.font = pygame.font.SysFont(None, 24)
        #Icon cache
        names=[["Uboat.png",35,10],
                ["Submerged.png",35,10],
                ["Merchant.png",40,14],
                ["Destroyer.png",35,12],
                ["Carrier.png",60,16],
                ["Battleship.png",60,16],
                ["Aircraft.png",25,20],
                ["Smoke_intense.png",60,80],
                ["Smoke_weak.png",40,50],
                ["Explosion.png",15,15],
                ["Smoke_damage.png",25,40]
        ]
        self.image_cache = {}
        for name in names:
            img = pygame.image.load("Images/" + name[0]).convert_alpha()
            img = pygame.transform.scale(img, (name[1],name[2]))
            self.image_cache[name[0]] = img

        # state
        self.current_screen = "main"
        self.current_square = None

        # data
        self.points = {}
        self.displays = []
        self.buttons = []
        self.sprites = {}
        self.sp_info=[]
        self.circles = []
        self.images = []
        self.end_squares = {}
        self.clicked_sprite= None

        self.help_background = pygame.Surface((width, height))
        self.help_background.fill((40,40,40))

        self.subscreen_background = pygame.image.load(
            "Images/subscreen_bg.png"
        ).convert()

        self.subscreen_background = pygame.transform.scale(
            self.subscreen_background,
            (width, height)
        )

    # -------------------------------------------------
    # OBJECT CLASSES
    # -------------------------------------------------

    class Sprite:
        def __init__(self, x, y, image):
            self.image = image
            self.rect = self.image.get_rect(center=(x,y))

    class Display:
        def __init__(self, x, y, text, width, height, color):
            self.rect = pygame.Rect(x,y,width,height)
            self.text = text
            self.color = color

    class Button:
        def __init__(self, x, y, text, width, height):
            self.rect = pygame.Rect(x,y,width,height)
            self.text = text
            self.clicked = False

    class Circle:
        def __init__(self, x, y, radius, color, alpha):
            self.x = x
            self.y = y
            self.radius = radius
            self.color = color
            self.alpha = alpha

    # -------------------------------------------------
    # CREATION FUNCTIONS
    # -------------------------------------------------

    def create_timeline(self,time,timeline):
        x=(time*2)+128
        y=(timeline*32)+32
        self.points[((time,timeline),(time,timeline))]=[(x,y),(x,y)]

    def update_timeline(self, location):
        x=(location[0]*2)+128
        y=(location[1]*32)+32
        for key,points in self.points.items():
            if key[0][1]==location[1]:
                self.points[(key[0],location)]=[points[0],(x,y)]
                del self.points[key]
                break

    def create_sprite(self, id, x, y, icon):
        self.sp_info.append([id,icon,x,y])
        icon=str(icon+".png")
        image = self.image_cache[icon]
        sp = self.Sprite(x,y, image)
        self.sprites[id]=sp
        return sp

    def create_display(self, x, y, text, width, height, color):
        d = self.Display(x,y,text, width, height, color)
        self.displays.append(d)
        return d

    def create_button(self, x, y, text, width, height):
        b = self.Button(x,y,text, width, height)
        self.buttons.append(b)
        return b
    
    def check_range(self,sp1,sp2,range):
        x=abs(((sp1[2])-(sp2[2]))**2)
        y=abs(((sp1[3])-(sp2[3]))**2)
        r=x+y
        r=math.sqrt(r)
        if r>range:
            in_range=False
        else:
            in_range=True
        return in_range
    
    def create_circle(self, x, y, radius, color=(200,50,50), alpha=100):
        c = self.Circle(x, y, radius, color, alpha)
        self.circles.append(c)
    
    def draw_image(self, icon, x, y):
        icon=str(icon+".png")
        image = self.image_cache[icon]
        rect = image.get_rect(center=(x, y))
        self.images.append((image, rect))

    def update_square(self,location):
        self.current_square=(location)


    # -------------------------------------------------
    # MAIN UPDATE FUNCTION
    # -------------------------------------------------

    def update(self, screen, events):

        clicked_buttons = []
        mouse = pygame.mouse.get_pos()
        new_click = False

        for event in events:

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.current_screen == "main":
                    mx, my = mouse
                    for key,point in self.points.items():
                        if (abs(point[0][1]-my)<8) and (mx>point[0][0]) and (mx<point[1][0]+2):
                            board=int(mx/2)-64
                            self.current_square = (board,key[0][1])
                            self.current_screen = "sub"
                    for key,end_square in self.end_squares.items():
                        if pygame.Rect(end_square).collidepoint(mouse):
                            self.current_square = (key[1])
                            self.current_screen = "sub"

                elif self.current_screen in ["sub","help"]:
                    if pygame.Rect(10,10,100,40).collidepoint(mouse):
                        self.current_screen = "main"
                        self.current_square = None
                        self.clicked_sprite = None
                    else:
                        for key, sp in self.sprites.items():
                            if sp.rect.collidepoint(mouse):
                                self.clicked_sprite = key
                                new_click = True
                                break
                            new_click = False

                for b in self.buttons:
                    if b.rect.collidepoint(mouse):
                        clicked_buttons.append(b.text)
                        if b.text == "Help":
                            self.current_screen = "help"
                        break
                if not new_click and len(clicked_buttons)==0:
                    self.clicked_sprite = None

        # ---------------------------
        # DRAW
        # ---------------------------

        screen.fill((30,30,30))
        self.end_squares={}
        if self.current_screen == "main":
            for key,points in self.points.items():
                pygame.draw.line(screen,(200,200,200),points[0],points[1],4)
                end_square = pygame.Rect(points[1][0]+1,points[1][1]-3,9,9)
                pygame.draw.rect(screen, (100, 200, 255), end_square)
                self.end_squares[key]=end_square
                self.create_display(key[0][0]+5,key[0][1]*32+22,"Timeline: "+str(key[0][1]),100,20, (180,180,180))
        elif self.current_screen == "sub":

            screen.blit(self.subscreen_background,(0,0))

            back_button = pygame.Rect(10,10,100,40)

            pygame.draw.rect(screen,(200,80,80),back_button)

            txt = self.font.render("Back",True,(255,255,255))
            screen.blit(txt,(35,20))

            sprite_visible=[]
            in_range=False
            for sp1 in self.sp_info:
                if sp1[1]=="Uboat":
                    sprite_visible.append(sp1[0])
                    for sp2 in self.sp_info:
                        if sp2[1]!="Uboat":
                            in_range=self.check_range(sp1,sp2,200)
                            if in_range:
                                sprite_visible.append(sp2[0])

            for key,sp in self.sprites.items():
                if key in sprite_visible:
                    screen.blit(sp.image,sp.rect)

            for image, rect in self.images:
                screen.blit(image, rect)

        elif self.current_screen == "help":

            screen.blit(self.help_background,(0,0))

            back_button = pygame.Rect(10,10,100,40)

            pygame.draw.rect(screen,(200,80,80),back_button)

            txt = self.font.render("Back",True,(255,255,255))
            screen.blit(txt,(35,20))

        for d in self.displays:

            pygame.draw.rect(screen,d.color,d.rect)
            pygame.draw.rect(screen,(0,0,0),d.rect,2)

            txt = self.font.render(d.text,True,(0,0,0))
            screen.blit(txt,txt.get_rect(center=d.rect.center))

        for b in self.buttons:

            pygame.draw.rect(screen,(200,80,80),b.rect)
            pygame.draw.rect(screen,(0,0,0),b.rect,2)

            txt = self.font.render(b.text,True,(255,255,255))
            screen.blit(txt,txt.get_rect(center=b.rect.center))

        for c in self.circles:
            temp_surface = pygame.Surface((c.radius*2, c.radius*2), pygame.SRCALPHA)
            pygame.draw.circle(temp_surface,(*c.color, c.alpha),(c.radius, c.radius),c.radius)
            screen.blit(temp_surface, (c.x - c.radius, c.y - c.radius))

        # Clears lists of drawn items
        self.displays=[]
        self.buttons=[]
        self.sprites={}
        self.sp_info=[]
        self.circles = []
        self.images = []


        return {
            "screen": self.current_screen,
            "square": self.current_square,
            "buttons": clicked_buttons,
            "sprite_clicked": self.clicked_sprite
        }