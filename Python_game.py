WIDTH=1024
HEIGHT=1024

import pygame
pygame.init()
font = pygame.font.SysFont(None, 24)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
subscreen_background = pygame.image.load("Images/subscreen_bg.png").convert()
subscreen_background = pygame.transform.scale(subscreen_background,(WIDTH,HEIGHT))
# -----------------------------
# BASIC SETUP
# -----------------------------
pygame.display.set_caption("Simple Screen System")

clock = pygame.time.Clock()

# App state
current_screen = "main"
current_square = None

# Data storage
squares = []     # squares on main screen
lines = []       # lines on main screen
displays = []    # displays on all screens
buttons = []     # buttons on subscreens
sprites = {}     # sprites for each square (dictionary)

# -----------------------------
# OBJECT CLASSES
# -----------------------------
class Square:
    def __init__(self, x, y, text, turn, timeline, size=80):
        self.rect = pygame.Rect(x, y, size, size)
        self.text = text
        self.turn = turn
        self.timeline = timeline


class Sprite:
    def __init__(self, image_path, x, y):
        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 255, 255))

        #self.image = pygame.image.load(image_path).convert_alpha()
        #self.rect = self.image.get_rect(topleft=(x, y))
        self.rect=self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Display:
    def __init__(self, x, y, text, width=120, height=40):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

    def draw(self, surface):
        pygame.draw.rect(surface, (180,180,180), self.rect)
        pygame.draw.rect(surface, (0,0,0), self.rect, 2)

        text_surface = font.render(self.text, True, (0,0,0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)


class Button:
    def __init__(self, x, y, text, width=120, height=40):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

    def draw(self, surface):
        pygame.draw.rect(surface, (200,80,80), self.rect)
        pygame.draw.rect(surface, (0,0,0), self.rect, 2)

        text_surface = font.render(self.text, True, (255,255,255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------

def create_square(x, y, text, turn=1, timeline=1):
    """
    Create a square on the main screen with text on top
    """
    sq = Square(x, y, text, turn, timeline)
    squares.append(sq)
    sprites[sq] = []


def draw_line(sq1,sq2):
    """Store a line to be drawn on the main screen"""
    x1, y1 = sq1.rect.center
    x2, y2 = sq2.rect.center
    lines.append((x1, y1, x2, y2))


def draw_curve(sq1,sq2):
    """Store a curved, dotted line to be drawn on the main screen"""
    x1, y1 = sq1.rect.center
    x2, y2 = sq2.rect.center
    xm=(x1+x2)/2
    ym=((y1+y2)/2)-60
    lines.append((x1,y1,xm,ym))
    lines.append((xm,ym,x2,y2))


def create_sprite(square, sprite_type, x, y):
    """Create a sprite in a square's subscreen"""
    sp = Sprite(sprite_type, x, y)
    #sp = Sprite(image_path, x, y) FOR IMAGES LATER
    sprites[square].append(sp)


def create_display(x, y, text):
    d = Display(x, y, text)
    displays.append(d)
    return d


def create_button(x, y, text):
    b = Button(x, y, text)
    buttons.append(b)

    mouse = pygame.mouse.get_pos()
    pressed = pygame.mouse.get_pressed()[0]

    return b.rect.collidepoint(mouse) and pressed


# -----------------------------
# TEST OBJECTS (example)
# -----------------------------
create_square(100, 200,"Timeline 1, Turn 1")
create_square(300, 250,"Timeline 1, Turn 1")

draw_line(squares[0],squares[1])
draw_curve(squares[0],squares[1])

create_sprite(squares[0],"glob",100,100)
create_sprite(squares[0],"glob",300,100)
create_sprite(squares[1],"glob",150,200)

# -----------------------------
# MAIN LOOP
# -----------------------------
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()

            if current_screen == "main":
                # check if a square was clicked
                for sq in squares:
                    if sq.rect.collidepoint(mouse):
                        current_square = sq
                        current_screen = "sub"

            elif current_screen == "sub":
                #Checks if returning to main
                if pygame.Rect(10, 10, 100, 40).collidepoint(mouse):
                    current_screen = "main"
                    current_square = None

            mouse = pygame.mouse.get_pos()
            for b in buttons:
                if b.is_clicked(mouse):
                    print("Button pressed:", b.text)

    screen.fill((30, 30, 30))
    # -----------------------------
    # TOGGLEABLE BUTTONS/DISPLAYS
    # -----------------------------
    buttons.clear()
    displays.clear()

    create_button(500,500,"hi!")
    create_display(600,600,"This is a display!")

    # -----------------------------
    # MAIN SCREEN
    # -----------------------------
    if current_screen == "main":

        # draw lines
        for line in lines:
            pygame.draw.line(screen, (200, 200, 200), line[:2], line[2:], 2)

        # draw squares
        for sq in squares:
            pygame.draw.rect(screen, (100, 200, 255), sq.rect)
            text_surface = font.render(sq.text, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=sq.rect.center)
            screen.blit(text_surface, text_rect)

        

    # -----------------------------
    # SUBSCREEN
    # -----------------------------
    elif current_screen == "sub":

        # draw subscreen background
        screen.blit(subscreen_background, (0, 0))

        # back button
        back_button = pygame.Rect(10, 10, 100, 40)
        pygame.draw.rect(screen, (200, 80, 80), back_button)
        text = font.render("Back", True, (255, 255, 255))
        screen.blit(text, (35, 20))

        # draw sprites for this square
        for sp in sprites[current_square]:
            # simple color by type
            color = (0, 255, 0)
            """
            if sp.type == "enemy":
                color = (255, 0, 0)
            elif sp.type == "item":
                color = (255, 255, 0)
            """
            screen.blit(sp.image, sp.rect)

            pygame.draw.rect(screen, color, sp.rect)
    clock.tick(60)
    for d in displays:
        d.draw(screen)

    for b in buttons:
        b.draw(screen)

    print(sprites)
    pygame.display.flip()
pygame.quit()