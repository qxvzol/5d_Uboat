import pygame
import math

class TimelineUI:

    def __init__(self, width=1024, height=1024):

        self.WIDTH = width
        self.HEIGHT = height

        pygame.font.init()
        self.font = pygame.font.SysFont(None, 24)
        #Icon cache
        names=[["Uboat.png",50,10], ["Submerged.png",50,10], ["Merchant.png",60,20], ["Destroyer.png",50,15], ["Carrier.png",100,30],
        ["Battleship.png",100,30], ["Aircraft.png",40,30], ["Smoke_intense.png",75,100], ["Smoke_weak.png",50,60], ["Explosion.png",20,20], ["Smoke_damage.png",30,50]
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
        self.squares = {}
        self.lines = []
        self.displays = []
        self.buttons = []
        self.sprites = {}
        self.sp_info=[]
        self.circles = []
        self.images = []
        self.sprite_clicked= None

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

    class Square:
        def __init__(self, x, y, text, turn, timeline, size=80):
            self.rect = pygame.Rect(x, y, size, size)
            self.text = text
            self.turn = turn
            self.timeline = timeline

    class Sprite:
        def __init__(self, x, y, image):
            self.image = image
            self.rect = self.image.get_rect(topleft=(x,y))

    class Display:
        def __init__(self, x, y, text, width, height):
            self.rect = pygame.Rect(x,y,width,height)
            self.text = text

    class Button:
        def __init__(self, x, y, text, width=120, height=40):
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

    def create_square(self, turn, timeline):
        text=str(("Turn "+str(turn)+", Line "+str(timeline)))
        x=turn*100
        y=timeline*100-40
        sq = self.Square(x,y,text,turn,timeline)
        self.squares[(turn,timeline)]=sq
        return sq

    def create_line(self, k1, k2, color):
        sq1 = self.squares[k1]
        sq2 = self.squares[k2]

        x1, y1 = sq1.rect.center
        x2, y2 = sq2.rect.center

        self.lines.append([(x1, y1), (x2, y2),color])

    def create_sprite(self, id, x, y, icon):
        x=(x*32)-48
        y=(y*32)-32
        self.sp_info.append([id,icon,x,y])
        icon=str(icon+".png")
        image = self.image_cache[icon]
        sp = self.Sprite(x,y, image)
        self.sprites[id]=sp
        return sp

    def create_display(self, x, y, text, width, height):
        d = self.Display(x,y,text, width, height)
        self.displays.append(d)
        return d

    def create_button(self, x, y, text):
        b = self.Button(x,y,text)
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

        return c
    
    def draw_image(self, icon, x, y):
        icon=str(icon+".png")
        image = self.image_cache[icon]
        rect = image.get_rect(topleft=(x, y))
        self.images.append((image, rect))

    # -------------------------------------------------
    # MAIN UPDATE FUNCTION
    # -------------------------------------------------

    def update(self, screen, events):

        clicked_buttons = []
        mouse = pygame.mouse.get_pos()

        for event in events:

            if event.type == pygame.MOUSEBUTTONDOWN:

                if self.current_screen == "main":
                    for key, sq in self.squares.items():
                        if sq.rect.collidepoint(mouse):
                            self.current_square = key
                            self.current_screen = "sub"

                elif self.current_screen == "sub":

                    if pygame.Rect(10,10,100,40).collidepoint(mouse):
                        self.current_screen = "main"
                        self.current_square = None
                    else:
                        for key, sp in self.sprites.items():
                            if sp.rect.collidepoint(mouse):
                                self.clicked_sprite = key
                                break
                            self.clicked_sprite = None
                        

                for b in self.buttons:
                    if b.rect.collidepoint(mouse):
                        clicked_buttons.append(b.text)

        # ---------------------------
        # DRAW
        # ---------------------------

        screen.fill((30,30,30))

        if self.current_screen == "main":
            self.clicked_sprite = None
            for line in self.lines:
                pygame.draw.line(screen,line[2],line[0],line[1],2)

            for sq in self.squares.values():

                pygame.draw.rect(screen,(100,200,255),sq.rect)

                txt = self.font.render(sq.text,True,(0,0,0))
                rect = txt.get_rect(center=sq.rect.center)

                screen.blit(txt,rect)

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

        for d in self.displays:

            pygame.draw.rect(screen,(180,180,180),d.rect)
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

            pygame.draw.circle(
                temp_surface,
                (*c.color, c.alpha),
                (c.radius, c.radius),
                c.radius
            )

            screen.blit(temp_surface, (c.x - c.radius, c.y - c.radius))

        # Clears lists of drawn items
        self.displays=[]
        self.buttons=[]
        self.sprites={}
        self.squares={}
        self.lines=[]
        self.sp_info=[]
        self.circles = []
        self.images = []

        return {
            "screen": self.current_screen,
            "square": self.current_square,
            "buttons": clicked_buttons,
            "sprite_clicked": self.clicked_sprite
        }