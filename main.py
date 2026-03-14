import pygame
from GUI import TimelineUI
turn=1

pygame.init()
#Creates screen and clock
screen = pygame.display.set_mode((1024,1024))
clock = pygame.time.Clock()

ui = TimelineUI()

running = True

# Main storage for board info

boards = {
    (0, 1): [(0,1,0),1,[]],
    (1, 1): [
        (0,1,0),
        1,
        [
            [1, [10,10], [100,100], [3, 3], "UB", "Uboat"],
            [2, [4,4], [120,120], [3, 5], "M", "Merchant"],
            [3, [4,4], [150,150], [3, 7], "DD", "Destroyer"],
            [4, [4,4], [600,600], [3, 9], "CV", "Carrier"],
            [5, [4,4], [1000,1000], [3, 11], "BB", "Battleship"],
            [6, [4,4], [100,100], [3, 13], "A", "Aircraft"],
        ]
    ],
    (2, 1): [(1,1,0),1,[]],
    (1, 2): [(2,1,1),1,[]],
}

while running:

    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False

    for key,value in boards.items():
        ui.create_square(key[0],key[1])
        if value[0][2]==0:
            ui.create_line(key,(value[0][0],value[0][1]),(200,200,200))
        if value[0][2]==1:
            ui.create_line(key,(value[0][0],value[0][1]),(200,50,50))

    state = ui.update(screen,events)
    square_loc=state["square"]
    screen_stat=state["screen"]
    # Subscreen Program every tick
    if screen_stat=="sub":
        value=boards[square_loc]
        for sprites in value[2]:
            ui.create_sprite(sprites[0], sprites[3][0], sprites[3][1], sprites[5])
        ui.create_display(332,20,"Turn: "+str(square_loc[0]),120, 40)
        ui.create_display(452,20,"Timeline: "+str(square_loc[1]),120, 40)
        ui.create_display(572,20,"Current Turn: "+str(turn),120, 40)
    else: # Mainscreen Program every tick
        ui.create_display(392,20,"Turn: "+str(turn),120, 40)
        ui.create_button(512,20,"Next Turn")


    if "hi!" in state["buttons"]:
        print("Button clicked!")
    if "awesome!!1!!" in state["buttons"]:
        print("Button clicked!")


    sprite_clicked=state["sprite_clicked"]
    if sprite_clicked!=None:
        value=(boards[square_loc])[2]
        for id in value:
            if id[0]==sprite_clicked:
                if id[4]=="UB":
                    ui.create_display(20,964,"Typle: Uboat",200, 40)
                else:
                    ui.create_display(20,964,"Type: "+id[5],200, 40)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

#ui.create_circle(512,512,100) DELETE LATER, ONLY FOR EXAMPLE