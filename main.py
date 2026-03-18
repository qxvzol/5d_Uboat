import pygame
from GUI import TimelineUI
import copy

pygame.init()
#Creates screen and clock
screen = pygame.display.set_mode((1024,1024))
clock = pygame.time.Clock()

ui = TimelineUI()

running = True
snapshot_time = 0.0
SNAPSHOT_INTERVAL = 1

# Main storage for board info

class Board:
    __slots__ = ("alert","units")

    def __init__(self, alert, units):
        self.alert = alert
        self.units = units

    def clone(self):
        return Board(
            self.alert,
            [u.clone() for u in self.units]
        )

class Unit:
    __slots__ = ("ID", "HP", "speed", "coord", "type", "name", "visible", "suspicion", "status")

    def __init__(self, ID, HP, speed, coord, type, name, visible, suspicion, status):
        self.ID = ID
        self.HP = HP
        self.speed = speed
        self.coord = coord
        self.type = type
        self.name = name
        self.visible = visible
        self.suspicion = suspicion
        self.status = status

    def clone(self):
        return Unit(
            self.ID,
            self.HP.copy(),
            self.speed.copy(),
            self.coord.copy(),
            self.type,
            self.name,
            self.visible,
            self.suspicion,
            self.status
        )

progression=False
latest_board=[(1,1),(1,2)]
boards = {
    (0, 1): Board(1,[]),
    (1, 1): Board(
        1,
        [
            Unit(1, [100,100], [0,20], [500, 350], "Uboat", "U-69", True, 0, ""),
            Unit(2, [40,120], [8,12], [500, 500], "Merchant", "SS Empire Bell", True, 0, "convoy"),
            Unit(3, [150,150], [8,35], [500, 600], "Destroyer", "HMS Cockchafer", True, 0, "hunting"),
            Unit(4, [0,600], [8,30], [400, 500], "Carrier", "HMS Ark Royal", True, 0, "fleeing"),
            Unit(5, [1000,1000], [8,30], [600, 500], "Battleship", "HMS Warspite", True, 0, "fleeing"),
            Unit(6, [100,100], [120,120], [600, 600], "Aircraft", "", True, 0, "patrolling"),
        ]
    ),
    (0, 2): Board(1,[]),
    (1, 2): Board(1,[]),
}

ui.create_timeline(0,1)
ui.update_timeline((1,1))
ui.create_timeline(0,2)
ui.update_timeline((1,2))


while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    state = ui.update(screen,events)
    square_loc=state["square"]
    screen_stat=state["screen"]
    sprite_clicked=state["sprite_clicked"]

    # Subscreen Program every tick
    if screen_stat=="sub":
        test=boards[(1, 1)]
        value=boards[square_loc]
        #Time progression of subscreen board
        progression=False
        if square_loc in latest_board:
            progression=True
        if progression:
            snapshot_time+=(1/60)
            if snapshot_time > SNAPSHOT_INTERVAL:
                snapshot_time = 0
                latest_board.remove(square_loc)
                new_loc = (square_loc[0]+1, square_loc[1])
                boards[new_loc] = copy.deepcopy(value)
                square_loc = new_loc
                ui.update_square(square_loc)
                ui.update_timeline(square_loc)
                latest_board.append(square_loc)
        for sprites in value.units:
            if sprites.visible:
                ui.create_sprite(sprites.ID, sprites.coord[0], sprites.coord[1], sprites.type)
                if 0<((sprites.HP[0])/(sprites.HP[1]))<0.5:
                    x=sprites.coord[0]-8
                    y=sprites.coord[1]-16
                    ui.draw_image("Smoke_damage",x,y)
            if sprites.HP[0]<=0:
                if progression:
                    sprites.HP[0]-=1
                if -360<sprites.HP[0]<=0:
                    sprites.type="Smoke_intense"
                elif -720<sprites.HP[0]<=-360:
                    sprites.type="Smoke_weak"
                else:
                    value.units.remove(sprites)


        ui.create_display(392,20,"Time: "+str(square_loc[0]),120, 40)
        ui.create_display(512,20,"Timeline: "+str(square_loc[1]),120, 40)
    else: # Mainscreen Program every tick
        ui.create_button(10,960,"Help",180,40)
    if sprite_clicked!=None:
        value=(boards[square_loc]).units
        for unit in value:
            if unit.ID==sprite_clicked:
                if unit.type=="Uboat":
                    ui.create_display(20,964,"Type: Uboat",180, 20)
                    ui.create_display(20,984,"Name: "+str(unit.name),180, 20)
                    ui.create_display(200,964,"Speed: "+str(unit.speed[0])+"/"+str(unit.speed[1]),180, 20)
                    ui.create_display(200,984,str(unit.coord),180, 20)
                    ui.create_circle(unit.coord[0],unit.coord[1],200)
                elif unit.type in ["Battleship","Carrier","Merchant","Destroyer"]:
                    ui.create_display(20,964,"Type: "+str(unit.type),180, 20)
                    ui.create_display(20,984,"Name: "+str(unit.name),180, 20)
                    ui.create_display(200,964,"Speed: "+str(unit.speed[0])+"/"+str(unit.speed[1]),180, 20)
                    ui.create_display(200,984,str(unit.coord),180, 20)
                    ui.create_display(380,964,"Status: "+str(unit.status),180, 20)
                    ui.create_button(380,984,"Target Ship",180, 20)
                    ui.create_button(560,964,"Fire Torpedo",180, 40)
                else:
                    ui.create_display(20,964,"Type: Aircraft",180, 20)
                    ui.create_display(20,984,"Status: "+str(unit.status),180, 20)
                    ui.create_display(200,964,"Speed: "+str(unit.speed[0])+"/"+str(unit.speed[1]),180, 20)
                    ui.create_display(200,984,str(unit.coord),180, 20)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

#ui.create_circle(512,512,100) DELETE LATER, ONLY FOR EXAMPLE