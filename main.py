import pygame
from GUI import TimelineUI
import copy
import math

pygame.init()
#Creates screen and clock
screen = pygame.display.set_mode((1024,1024))
clock = pygame.time.Clock()

ui = TimelineUI()

grey=(180,180,180)
red=(200,80,80)
MOVEMENT_FACTOR=0.02

warp=False

running = True
snapshot_time = 0.0
SNAPSHOT_INTERVAL = 1
timeline_count=1

def clamp(value,min,max):
    if value>max:
        value=max
    elif value<min:
        value=min
    return value

def convert_movement(speed,dest,pos):
    x=dest[0]-pos[0]
    y=dest[1]-pos[1]
    dist=((x**2)+(y**2))**0.5
    if speed>0:
        t=(dist/speed)/MOVEMENT_FACTOR
        x2=x/t
        y2=y/t
    else:
        x2=0
        y2=0
    return x2,y2

# Main storage for board info

class Board:
    __slots__ = ("alert","units")

    def __init__(self, alert, units):
        self.alert = alert
        self.units = units

class Unit:
    __slots__ = ("ID", "HP", "speed", "dest", "coord", "type", "name", "unit_spec")

    def __init__(self, ID, HP, speed, dest, coord, type, name, unit_spec):
        self.ID = ID
        self.HP = HP
        self.speed = speed
        self.dest = dest
        self.coord = coord
        self.type = type
        self.name = name
        self.unit_spec = unit_spec

class Uboat:
    __slots__ = ("warp", )

    def __init__(self, warp, ):
        self.warp = warp

class Enemy:
    __slots__ = ("visible", "suspicion", "status", "acc")

    def __init__(self, visible, suspicion, status, acc):
        self.visible = visible
        self.suspicion = suspicion
        self.status = status
        self.acc = acc


progression=False
latest_board=[(1,1)]
boards = {
    (0, 1): Board(1,[]),
    (1, 1): Board(
        1,
        [
            Unit(1, [100,100], [20,20], [0,0], [500, 350], "Uboat", "U-69", Uboat(0)),
            Unit(2, [40,120], [8,12], [0,0], [500, 500], "Merchant", "SS Empire Bell", Enemy(True,0,"patrol",0)),
            Unit(3, [150,150], [8,35], [0,0], [500, 600], "Destroyer", "HMS Cockchafer", Enemy(True,0,"patrol",0)),
            Unit(4, [0,600], [8,25], [0,0], [400, 500], "Carrier", "HMS Ark Royal", Enemy(True,0,"patrol",0)),
            Unit(5, [1000,1000], [25,25], [800,800], [500, 500], "Battleship", "HMS Warspite", Enemy(True,0,"patrol",0)),
            Unit(6, [100,100], [120,120], [0,0], [600, 600], "Aircraft", None, Enemy(True,0,"patrol",0)),
        ]
    ),
}

ui.create_timeline(0,1)
ui.update_timeline((1,1))


while running:

    click_events = pygame.event.get()
    for event in click_events:
        if event.type == pygame.QUIT:
            running = False

    state = ui.update(screen,click_events,warp,timeline_count)
    square_loc=state["square"]
    screen_stat=state["screen"]
    sprite_clicked=state["sprite_clicked"]
    buttons_clicked=state["buttons"]
    teleport=state["teleport"]

    if teleport!=None:
        prev_board=boards[prev_board_info[0]]
        for sprites in prev_board.units:
            if sprites.ID==prev_board_info[1]:
                new_sprites=copy.deepcopy(sprites)
                prev_board.units.remove(sprites)
                print("hi")
        if teleport not in latest_board:
            timeline_count+=1
            boards[teleport[0],timeline_count] = copy.deepcopy(boards[teleport])
            ui.create_timeline(teleport[0],timeline_count)
            latest_board.append((teleport[0],timeline_count))
            print(teleport[0],timeline_count)
        new_id=1
        for sprites in boards[teleport].units:
            print("ARGGHH")
            new_id+=1
        new_sprites.ID=new_id
            
        if teleport not in latest_board:
            boards[teleport[0],timeline_count].units.append(new_sprites)
            for units in boards[teleport[0],timeline_count].units:
                if units.type=="Uboat":
                    print(units.unit_spec.warp)
                    units.unit_spec.warp=0
        else:
            boards[teleport].units.append(new_sprites)

        teleport=None
        warp=False

    #Time progression of subscreen boards
    if screen_stat=="sub":
        value=boards[square_loc]
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



    #Mainscreen program running every tick
    if screen_stat=="main":
        ui.create_button(10,960,"Help",180,40)



    #Subscreen program running every tick
    elif screen_stat=="sub":
        for sprites in value.units:
            if sprites.type!="Uboat":
                sprites.unit_spec.suspicion=clamp(sprites.unit_spec.suspicion,0,1)
                if sprites.unit_spec.visible:
                    if sprites.unit_spec.suspicion>0:
                        color=(20*sprites.unit_spec.suspicion+180,-130*sprites.unit_spec.suspicion+180,-130*sprites.unit_spec.suspicion+180)
                        ui.create_display(sprites.coord[0]-60,sprites.coord[1]-48,"",120,20, grey)
                        ui.create_display(sprites.coord[0]-(sprites.unit_spec.suspicion*60),sprites.coord[1]-48,"",sprites.unit_spec.suspicion*120,20, color)
            show=False
            if sprites.type!="Uboat":
                if sprites.unit_spec.visible:
                    show=True
            elif sprites.type=="Uboat":
                show=True
            if show:
                ui.create_sprite(sprites.ID, sprites.coord[0], sprites.coord[1], sprites.type, sprites.dest)
                if 0<((sprites.HP[0])/(sprites.HP[1]))<0.5:
                    x=sprites.coord[0]-8
                    y=sprites.coord[1]-16
                    ui.draw_image("Smoke_damage",x,y)


        ui.create_display(392,20,"Time: "+str(square_loc[0]),120, 40, grey)
        ui.create_display(512,20,"Timeline: "+str(square_loc[1]),120, 40, grey)


    #Subscreen program running when board is progressing
        if progression:
            for sprites in value.units:
                x,y=convert_movement(sprites.speed[0],sprites.dest,sprites.coord)
                sprites.coord[0]+=x
                sprites.coord[1]+=y
                if not ((0<sprites.coord[0]<1000) and (0<sprites.coord[1]<1000)):
                    value.units.remove(sprites)

                if sprites.HP[0]<=0:
                    sprites.HP[0]-=1
                    if -360<sprites.HP[0]<=0:
                        sprites.type="Smoke_intense"
                    elif -720<sprites.HP[0]<=-360:
                        sprites.type="Smoke_weak"
                    else:
                        value.units.remove(sprites)

                if sprites.type=="Uboat":
                    if sprites.unit_spec.warp!=0:
                        sprites.unit_spec.warp+=0.01
                        if sprites.unit_spec.warp>1:
                            sprites.unit_spec.warp=0
                            print(sprites.ID)
                            warp=True
                            prev_board_info=(square_loc,sprites.ID)


                        

    #Subscreen program for sprite click
    if sprite_clicked!=None:
        value=(boards[square_loc]).units
        for unit in value:
            if unit.ID==sprite_clicked:
                if unit.type=="Uboat":
                    ui.create_display(20,964,"Type: Uboat",180, 20, grey)
                    ui.create_display(20,984,"Name: "+str(unit.name),180, 20, grey)
                    ui.create_display(200,964,"Speed: "+str(unit.speed[0])+"/"+str(unit.speed[1]),180, 20, grey)
                    ui.create_display(200,984,str(math.floor(unit.coord[0]))+","+str(math.floor(unit.coord[1])),180, 20, grey)
                    ui.create_circle(unit.coord[0],unit.coord[1],200)
                    ui.create_button(380,964,"Engage Warp",180,20)
                    ui.create_display(380,984,"Warp: "+str(round(unit.unit_spec.warp*100,2))+"%",180,20,red)
                    #UBOAT Destination set
                    if ui.movement!=None:
                        unit.dest=ui.movement
                    if "Engage Warp" in buttons_clicked:
                        if unit.unit_spec.warp==0:
                            unit.unit_spec.warp+=0.01
                    
                elif unit.type in ["Battleship","Carrier","Merchant","Destroyer"]:
                    ui.create_display(20,964,"Type: "+str(unit.type),180, 20, grey)
                    ui.create_display(20,984,"Name: "+str(unit.name),180, 20, grey)
                    ui.create_display(200,964,"Speed: "+str(unit.speed[0])+"/"+str(unit.speed[1]),180, 20, grey)
                    ui.create_display(200,984,str(math.floor(unit.coord[0]))+","+str(math.floor(unit.coord[1])),180, 20, grey)
                    ui.create_display(380,964,"Status: "+str(unit.unit_spec.status),180, 20, grey)
                    ui.create_button(380,984,"Target Ship",180, 20)
                    ui.create_button(560,964,"Fire Torpedo",180, 40)
                else:
                    ui.create_display(20,964,"Type: Aircraft",180, 20, grey)
                    ui.create_display(20,984,"Status: "+str(unit.unit_spec.status),180, 20, grey)
                    ui.create_display(200,964,"Speed: "+str(unit.speed[0])+"/"+str(unit.speed[1]),180, 20, grey)
                    ui.create_display(200,984,str(math.floor(unit.coord[0]))+","+str(math.floor(unit.coord[1])),180, 20, grey)


    #Pygame clock counter

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
