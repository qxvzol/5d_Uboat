import pygame
from GUI import TimelineUI

pygame.init()
#Creates screen and clock
screen = pygame.display.set_mode((1024,1024))
clock = pygame.time.Clock()

ui = TimelineUI()

sq1 = ui.create_square(100,200,"Timeline 1 Turn 1")
sq2 = ui.create_square(300,250,"Timeline 1 Turn 2")

ui.draw_line(sq1,sq2)

ui.create_sprite(sq1,100,100)

running = True

# Main storage for board info

boards = {
    (1, 1): [
        1,
        [
            [1, 10, 100, "uboat.png"],
            [2, 4, 80, "merchant.png"]
        ]
    ]
}

while running:

    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False

    ui.create_button(500,500,"hi!")
    ui.create_display(600,600,"Display!")
    ui.create_button(250,700,"awesome!!1!!")

    state = ui.update(screen,events)

    if "hi!" in state["buttons"]:
        print("Button clicked!")
    if "awesome!!1!!" in state["buttons"]:
        print("Button clicked!")

    pygame.display.flip()
    clock.tick(60)

pygame.quit()