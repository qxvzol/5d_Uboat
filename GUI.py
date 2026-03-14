import pygame

class TimelineUI:

    def __init__(self, width=1024, height=1024):

        self.WIDTH = width
        self.HEIGHT = height

        pygame.font.init()
        self.font = pygame.font.SysFont(None, 24)

        # state
        self.current_screen = "main"
        self.current_square = None

        # data
        self.squares = []
        self.lines = []
        self.displays = []
        self.buttons = []
        self.sprites = {}

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
        def __init__(self, x, y):
            self.image = pygame.Surface((40, 40))
            self.image.fill((255,255,255))
            self.rect = self.image.get_rect(topleft=(x,y))

    class Display:
        def __init__(self, x, y, text, width=120, height=40):
            self.rect = pygame.Rect(x,y,width,height)
            self.text = text

    class Button:
        def __init__(self, x, y, text, width=120, height=40):
            self.rect = pygame.Rect(x,y,width,height)
            self.text = text
            self.clicked = False

    # -------------------------------------------------
    # CREATION FUNCTIONS
    # -------------------------------------------------

    def create_square(self, x, y, text, turn=1, timeline=1):
        sq = self.Square(x,y,text,turn,timeline)
        self.squares.append(sq)
        self.sprites[sq] = []
        return sq

    def draw_line(self, sq1, sq2):
        x1,y1 = sq1.rect.center
        x2,y2 = sq2.rect.center
        self.lines.append((x1,y1,x2,y2))

    def create_sprite(self, square, x, y):
        sp = self.Sprite(x,y)
        self.sprites[square].append(sp)
        return sp

    def create_display(self, x, y, text):
        d = self.Display(x,y,text)
        self.displays.append(d)
        return d

    def create_button(self, x, y, text):
        b = self.Button(x,y,text)
        self.buttons.append(b)
        return b

    # -------------------------------------------------
    # MAIN UPDATE FUNCTION
    # -------------------------------------------------

    def update(self, screen, events):

        clicked_buttons = []

        mouse = pygame.mouse.get_pos()

        for event in events:

            if event.type == pygame.MOUSEBUTTONDOWN:

                if self.current_screen == "main":

                    for sq in self.squares:
                        if sq.rect.collidepoint(mouse):
                            self.current_square = sq
                            self.current_screen = "sub"

                elif self.current_screen == "sub":

                    if pygame.Rect(10,10,100,40).collidepoint(mouse):
                        self.current_screen = "main"
                        self.current_square = None

                for b in self.buttons:
                    if b.rect.collidepoint(mouse):
                        clicked_buttons.append(b.text)

        # ---------------------------
        # DRAW
        # ---------------------------

        screen.fill((30,30,30))

        if self.current_screen == "main":

            for line in self.lines:
                pygame.draw.line(screen,(200,200,200),line[:2],line[2:],2)

            for sq in self.squares:

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

            for sp in self.sprites[self.current_square]:
                screen.blit(sp.image,sp.rect)

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

        return {
            "screen": self.current_screen,
            "square": self.current_square,
            "buttons": clicked_buttons
        }