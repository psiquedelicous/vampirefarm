#import libraries
import pygame
import pygame_textinput
import math
from enum import Enum

#title
SCREEN_TITLE = 'Vampire Farm'

#screen size
SCREEN_WIDTH = 768
SCREEN_HEIGHT = 768

#clock to update frames
clock = pygame.time.Clock()

#position of units on game map
game_map = [['0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0']]


#colors (RGB)
WHITE_COLOR = (255, 255, 255)
RED_COLOR = (255, 0, 0)
BLACK_COLOR = (0, 0, 0)
GREEN_COLOR = (0, 255, 0)
GREY_COLOR = (194, 194, 194)

#fonts
pygame.font.init()
fontTitle = pygame.font.Font('fonts/8-bit pusab.ttf', 40)
fontLevels = pygame.font.Font('fonts/8-bit pusab.ttf', 25)
fontCounter = pygame.font.Font('fonts/8-bit pusab.ttf', 10)
LoseText = pygame.font.Font('fonts/8-bit pusab.ttf', 40)
WinText = pygame.font.Font('fonts/8-bit pusab.ttf', 40)

#cursor
MANUAL_CURSOR = pygame.transform.scale(pygame.image.load('images/cursor.png'), (48, 48))

#sounds and music
pygame.mixer.init()
##vampire sounds when clicked
vamp1_sound = pygame.mixer.Sound('sounds/vamp1.wav')
vamp2_sound = pygame.mixer.Sound('sounds/vamp2.wav')
vamp3_sound = pygame.mixer.Sound('sounds/vamp3.wav')
##vampire sounds during evolution
VthreeLvltwo_sound = pygame.mixer.Sound('sounds/V3lvl2.wav')
VtwoLvlOne_sound = pygame.mixer.Sound('sounds/V2lvl1.wav')
##human sounds during evolution
oneLvlTwo_sound = pygame.mixer.Sound('sounds/1lvl2.wav')
twoLvlThree_sound = pygame.mixer.Sound('sounds/2lvl3.wav')
threeLvltwo_sound = pygame.mixer.Sound('sounds/3lvl2.wav')
twoLvlOne_sound = pygame.mixer.Sound('sounds/2lvl1.wav')
farmDeath_sound = pygame.mixer.Sound('sounds/farmdeath.wav')
##game event's sounds
turn_sound = pygame.mixer.Sound('sounds/turn.wav')
death_sound = pygame.mixer.Sound('sounds/death.wav')
farm_sound = pygame.mixer.Sound('sounds/farm.wav')
##music
pygame.mixer.music.load('sounds/sleepysong.wav')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

#grid system
class PixelPoint :
    def __init__(self, x, y) :
        self.x = x
        self.y = y

    def __str__(self):
        return '(' + str(self.x) + ',' + str(self.y) + ')'

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return PixelPoint(self.x + other.x, self.y + other.y)
        else :
            raise TypeError('unsupported operand type(s) for +: "{}" and "{}"'.format(self.__class__, type(other)))

def GetTileAt(coord:PixelPoint) :
    return game_map[coord.y][coord.x]

#convert pixel to grid order
def pixToGrid(x, y):
    gridX = math.floor(x / 96)
    gridY = math.floor(y / 96)
    gridCoord = (gridX, gridY)
    return gridCoord

#convert grid order to pixel
def gridToPix(x, y):
    piX = x * 96
    piY = y * 96
    pixCoord = (piX, piY)
    return pixCoord

#snap cursor
def SnapToIncrement(value, snapTo) :
    return round(value/snapTo) * snapTo

#level
class Level(Enum):
    level1 = 1
    level2 = 2
    level3 = 3
    levelFarm = -1

#class where all the game pieces converge
class Game:

    #FPS rate
    TICK_RATE = 60

    #initializer of the game
    def __init__(self, image_path, image_path2, title, width, height, cursor, turn):
        self.title = title
        self.width = width
        self.height = height
        self.cursor = cursor
        self.turn = turn

        #create the window
        self.game_screen = pygame.display.set_mode((width, height))

        #set the title
        pygame.display.set_caption(title)

        #background
        self.image = pygame.transform.scale(pygame.image.load(image_path), (width, height))
        
        #splash screen
        self.screen_splash = pygame.transform.scale(pygame.image.load(image_path2), (width, height))

        #win screen
        self.winScreen = pygame.transform.scale(pygame.image.load('images/win.png'), (width, height))

        #game over screen
        self.gameoverScreen = pygame.transform.scale(pygame.image.load('images/gameover.png'), (width, height))
        
        #hide the standard cursor
        pygame.mouse.set_visible(False) 

    #game loop
    def run_game_loop(self):

        #game states
        is_game_over = False
        start = True
        gameLevel = False

        #other states
        selectedGridCoordinates = None
        selectedEntity = None
        movedVamp = []

        #splash screen - beginning of game
        while start == True and gameLevel == False and not is_game_over:
            #self.game_screen.blit(self.screen_splash, (0, 0))
            self.game_screen.fill(GREY_COLOR)

            #title
            textTitle = fontTitle.render('VAMPIRE FARM', True, RED_COLOR)
            self.game_screen.blit(textTitle, (self.width-650, self.height-700))

            #levels
            ##level1
            textLevels = fontLevels.render('Level 1', True, BLACK_COLOR)
            self.game_screen.blit(textLevels, (self.width-480, self.height-570))
          
            vamp1_img = pygame.transform.scale(pygame.image.load('images/1vamp.png'), (96, 96))
            self.game_screen.blit(vamp1_img, (96, self.height-600))
          
            human1_img = pygame.transform.scale(pygame.image.load('images/1human.png'), (96, 96))
            self.game_screen.blit(human1_img, (576, self.height-600))

            ##level 2
            textLevels = fontLevels.render('Level 2', True, BLACK_COLOR)
            self.game_screen.blit(textLevels, (self.width-480, self.height-440))

            vamp2_img = pygame.transform.scale(pygame.image.load('images/2vamp.png'), (96, 96))
            self.game_screen.blit(vamp2_img, (96, self.height-470))
          
            human2_img = pygame.transform.scale(pygame.image.load('images/2human.png'), (96, 96))
            self.game_screen.blit(human2_img, (576, self.height-470))

            ##level 3
            textLevels = fontLevels.render('Level 3', True, BLACK_COLOR)
            self.game_screen.blit(textLevels, (self.width-480, self.height-310))

            vamp3_img = pygame.transform.scale(pygame.image.load('images/3vamp.png'), (96, 96))
            self.game_screen.blit(vamp3_img, (96, self.height-340))
          
            human3_img = pygame.transform.scale(pygame.image.load('images/3human.png'), (96, 96))
            self.game_screen.blit(human3_img, (576, self.height-340))

            ##level farm
            textLevels = fontLevels.render('Level Farm', True, BLACK_COLOR)
            self.game_screen.blit(textLevels, (self.width-520, self.height-180))

            farmHuman_img = pygame.transform.scale(pygame.image.load('images/farmHuman.png'), (96, 96))
            self.game_screen.blit(farmHuman_img, (self.width-450, self.height-110))

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    start = False
                    gameLevel = True
            pygame.display.update()
            clock.tick(self.TICK_RATE)

        #game level
        while start == False and gameLevel == True and not is_game_over:

            self.game_screen.blit(self.image, (0, 0))
            
            #draw map
            tile_rects = []
            y = 0
            for layer in game_map:
                x = 0
                for tile in layer:
                    if isinstance(tile, Vampires):
                        self.game_screen.blit(tile.GetSprite(),(x*96,y*96))
                    elif isinstance(tile, Humans):
                        self.game_screen.blit(tile.GetSprite(),(x*96,y*96))
                    elif tile != '0':
                        tile_rects.append(pygame.Rect(x*96,y*96,96,96))
                    x += 1
                y += 1
            
            #cursor on Tile
            mouseX, mouseY = pygame.mouse.get_pos()
            x, y = pixToGrid(mouseX,mouseY)
            px,py = gridToPix(x,y)
            pygame.draw.rect(self.game_screen, WHITE_COLOR, (px, py, 96, 96), 12)
            
            #turn text
            textTurn = fontCounter.render('Turn ' + str(self.turn), True, BLACK_COLOR)
            self.game_screen.blit(textTurn, (self.width - 80, self.height - 40))
            
            #select tile
            if (selectedGridCoordinates != None) :
                px,py = gridToPix(selectedGridCoordinates[0], selectedGridCoordinates[1])
                pygame.draw.rect(self.game_screen, RED_COLOR, (px, py, 96, 96), 12)
            
            #game over event and win event
            vampHere = 0
            farmHere = 0
            humansCount = 0
            for y in range(len(game_map)):
                for x in range(len(game_map[y])):
                    if isinstance(game_map[y][x], Vampires):
                        vampHere += 1
                    if isinstance(game_map[y][x], Humans):
                        humansCount += 1
                        if game_map[y][x].level == Level.levelFarm:
                            farmHere += 1
            
            ##game over event
            if vampHere == 0 or humansCount < 4:
                pygame.mixer.music.stop()
                self.game_screen.fill(GREY_COLOR)
                LoseText = fontTitle.render('Game Over!', True, BLACK_COLOR)
                self.game_screen.blit(LoseText, (self.width-576, self.height-420))
                pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
                pygame.event.set_blocked(pygame.KEYDOWN)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        is_game_over = True
                pygame.display.update()
                clock.tick(self.TICK_RATE)

            ##win event
            elif farmHere == 4:
                self.game_screen.fill(GREY_COLOR)
                WinText = fontTitle.render('You Win!', True, BLACK_COLOR)
                self.game_screen.blit(WinText, (self.width-525, self.height-420))
                pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
                pygame.event.set_blocked(pygame.KEYDOWN)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        is_game_over = True
                pygame.display.update()
                clock.tick(self.TICK_RATE)
                
            #events getter
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_game_over = True
                
                #select
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouseX,mouseY=pygame.mouse.get_pos()
                    x, y = pixToGrid(mouseX,mouseY)
                    
                    #select to move
                    if (isinstance(game_map[y][x], Vampires)) :
                        selectedGridCoordinates=(x,y)
                        selectedEntity = game_map[y][x]
                        if game_map[y][x].level == Level.level1:                     
                            pygame.mixer.Sound.play(vamp1_sound)
                        if game_map[y][x].level == Level.level2:                     
                            pygame.mixer.Sound.play(vamp2_sound)
                        if game_map[y][x].level == Level.level3:                     
                            pygame.mixer.Sound.play(vamp3_sound)
                        continue
                    
                    #move vampire
                    if selectedEntity != None :
                        Vampires.Movement(selectedEntity, (x, y))
                        selectedGridCoordinates = selectedEntity.gridCoord
                        #append moved vampire to list
                        movedVamp.append(selectedGridCoordinates) 
                
                #deselect
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    selectedGridCoordinates = None
                    selectedEntity = None
    
                #end turn
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pygame.mixer.Sound.play(turn_sound)
                        movedVamp = []
                        Update()
                        self.turn += 1
                   
            #render vampires moved this turn
            for vamp in movedVamp:
                px, py = gridToPix(vamp[0], vamp[1])
                pygame.draw.rect(self.game_screen, BLACK_COLOR, (px, py, 96, 96), 12)
            
            #cursor effect
            x, y = pygame.mouse.get_pos()
            mX = SnapToIncrement(x,12)
            mY = SnapToIncrement(y,12)
            self.game_screen.blit(MANUAL_CURSOR, (mX,mY)) 

            pygame.display.update()
            clock.tick(self.TICK_RATE)

#map's limits 
def outOfMap(point:PixelPoint):
    x = point.x
    y = point.y

    if y < 0 or y > 7 or x < 0 or x > 7:
        return True
    else: 
        return False

#basic parameters of the units
class Units:
    def __init__(self, gridCoord, level):
        self.movedThisTurn = False
        self.gridCoord = gridCoord
        self.level = level
        game_map[gridCoord[1]][gridCoord[0]] = self
    
    #check surrounding are for units
    def UnitsAround(self):
        self.unitsAroundCount = 0
        self.unitsIDAround = {} 

        #square above
        north = PixelPoint(self.gridCoord[0]-1,self.gridCoord[1])
        if not outOfMap(north) and isinstance(GetTileAt(north), Units):
            self.unitsAroundCount += 1
            self.unitsIDAround['above'] = GetTileAt(north)
        
        #square to the left
        left = PixelPoint(self.gridCoord[0],self.gridCoord[1]-1)
        if not outOfMap(left) and isinstance(GetTileAt(left), Units):
            self.unitsAroundCount += 1
            self.unitsIDAround['left'] = GetTileAt(left)

        #square to the right
        right = PixelPoint(self.gridCoord[0],self.gridCoord[1]+1)
        if not outOfMap(right) and isinstance(GetTileAt(right), Units):
            self.unitsAroundCount += 1
            self.unitsIDAround['right'] = GetTileAt(right)
        
        #square below
        down = PixelPoint(self.gridCoord[0]+1,self.gridCoord[1])
        if not outOfMap(down) and isinstance(GetTileAt(down), Units):
            self.unitsAroundCount += 1
            self.unitsIDAround['below'] = GetTileAt(down)
        
        return self.unitsIDAround
    
    #check if there are units around
    def areUnitsAround(self):
        Units.UnitsAround(self)
        if self.unitsAroundCount == 0:
            return False
        else:
            return True
    
    #kill unit
    def Kill(self) :
        game_map[self.gridCoord[1]][self.gridCoord[0]] = '0'

#parameters of vampires
class Vampires(Units):
    def __init__(self, gridCoord, level):
        super(Vampires, self).__init__(gridCoord, level)
        self.Health()
        self.index = 0

    #vampire's animations   
    ##vampire level 1
    spriteWidth = 0
    spritev1_img = pygame.image.load('images/vamp1sprites.png')
    VampList1 = []

    for sprite in range(0, 7):
        sprite = pygame.transform.scale(spritev1_img.subsurface((spriteWidth, 0, 8, 8)), (96, 96))
        VampList1.append(sprite)
        spriteWidth += 8

    ##vampire level 2
    spriteWidth = 0
    spritev2_img = pygame.image.load('images/vamp2sprites.png')
    VampList2 = []

    for sprite in range(0, 7):
        sprite = pygame.transform.scale(spritev2_img.subsurface((spriteWidth, 0, 8, 8)), (96, 96))
        VampList2.append(sprite)
        spriteWidth += 8

    ##vampire level 3
    spriteWidth = 0
    spritev3_img = pygame.image.load('images/vamp3sprites.png')
    VampList3 = []

    for sprite in range(0, 7):
        sprite = pygame.transform.scale(spritev3_img.subsurface((spriteWidth, 0, 8, 8)), (96, 96))
        VampList3.append(sprite)
        spriteWidth += 8 
    
    #levels of health
    def Health(self):
        self.health = 0
        if self.level == Level.level1:
            self.health = 100
        if self.level == Level.level2:
            self.health = 250
        if self.level == Level.level3:
            self.health = 330

    #health to level
    def checkHealth(self):
        if self.health <= 0:
            pygame.mixer.Sound.play(death_sound)
            self.Kill()
        elif self.level == Level.level1:
            if self.health >= 200 and self.health < 300:
                self.level = Level.level2
                pygame.mixer.Sound.play(vamp2_sound)
        elif self.level == Level.level2:
            if self.health <= 199:
                self.level = Level.level1
                pygame.mixer.Sound.play(VtwoLvlOne_sound)
            elif self.health >= 300:
                self.level = Level.level3
                pygame.mixer.Sound.play(vamp3_sound)            
        elif self.level == Level.level3:
            if self.health >= 200 and self.health < 300:
                self.level = Level.level2
                pygame.mixer.Sound.play(VthreeLvltwo_sound)

    #sprite/animation to level
    def GetSprite(self):
        if self.level == Level.level1:
            self.index += 0.05
            if self.index >= len(Vampires.VampList1):
                self.index = 0
            return Vampires.VampList1[math.floor(self.index)]
            return Vampires.oneVamp_img
        elif self.level == Level.level2:
            self.index += 0.05
            if self.index >= len(Vampires.VampList2):
                self.index = 0
            return Vampires.VampList2[math.floor(self.index)]
            return Vampires.twoVamp_img
        elif self.level == Level.level3:
            self.index += 0.05
            if self.index >= len(Vampires.VampList3):
                self.index = 0
            return Vampires.VampList3[math.floor(self.index)]
    
    #power level of units around
    def PowerLevel(self):
        Units.UnitsAround(self)       
        humanLevel = 0
        lvlNum = 0
        for key, value in self.unitsIDAround.items():
            if isinstance(value, Humans):
                lvlNum = value.level.value
                humanLevel += lvlNum
        return humanLevel
        
    #move only to a square in the map and empty
    def Movement(unit, coordU):
        #only one movement/one turn
        if (unit.movedThisTurn) :
            return
            
        unitPrevx, unitPrevy = unit.gridCoord
        
        x = coordU[0]
        y = coordU[1]
                
        distX = abs(x - unitPrevx)
        distY = abs(y - unitPrevy)

        #deny movement if square is outside of map or occupied
        if distX > 1 or distY > 1 or game_map[y][x] != '0':
            return
        
        game_map[unitPrevy][unitPrevx] = '0'
        unit.gridCoord = (coordU[0],coordU[1])
        game_map[y][x] = unit
          
        unit.movedThisTurn = True

    #adjust unit level to level of humans around 
    def Interaction(self):
        humanLevel = self.PowerLevel()
        Units.areUnitsAround(self)
        if Units.areUnitsAround(self) == False:
            if self.level == Level.level1:
                self.health -= 5
            if self.level == Level.level2:
                self.health -= 10
            if self.level == Level.level3:
                self.health -= 15
        elif Units.areUnitsAround(self) == True:
            if self.level.value <= humanLevel:
                if humanLevel == 1:
                    self.health -= 7
                elif humanLevel == 2:
                    self.health -= 12
                elif humanLevel == 3:
                    self.health -= 18
                elif humanLevel >= 4:
                    self.health -= 25
            elif self.level.value > humanLevel and self.health < 400 :
                if humanLevel == -1:
                    self.health += 40
                if humanLevel == 1:
                    self.health += 35
                elif humanLevel == 2:
                    self.health += 30
        self.checkHealth()

#parameters of humans         
class Humans(Units):
    def __init__(self, gridCoord, level):
        super(Humans, self).__init__(gridCoord, level)
        self.Health()
        self.index = 0
    
    #human farm sprite
    farmHuman_img = pygame.transform.scale(pygame.image.load('images/farmHuman.png'), (96, 96))
    
    #human's animations
    ##human level 1
    spriteWidth = 0
    spriteh1_img = pygame.image.load('images/human1sprites.png')
    HumanList1 = []

    for sprite in range(0, 7):
        sprite = pygame.transform.scale(spriteh1_img.subsurface((spriteWidth, 0, 8, 8)), (96, 96))
        HumanList1.append(sprite)
        spriteWidth += 8

    ##human level 2
    spriteWidth = 0
    spriteh2_img = pygame.image.load('images/human2sprites.png')
    HumanList2 = []

    for sprite in range(0, 7):
        sprite = pygame.transform.scale(spriteh2_img.subsurface((spriteWidth, 0, 8, 8)), (96, 96))
        HumanList2.append(sprite)
        spriteWidth += 8

    ##human level 3
    spriteWidth = 0
    spriteh3_img = pygame.image.load('images/human3sprites.png')
    HumanList3 = []

    for sprite in range(0, 7):
        sprite = pygame.transform.scale(spriteh3_img.subsurface((spriteWidth, 0, 8, 8)), (96, 96))
        HumanList3.append(sprite)
        spriteWidth += 8

    #levels of health
    def Health(self):
        self.health = 0
        if self.level == Level.level1:
            self.health = 100
        elif self.level == Level.level2:
            self.health = 200
        elif self.level == Level.level3:
            self.health = 300
        elif self.level == Level.levelFarm:
            self.health = 200
            
    #health to level
    def checkHealth(self):
        if self.level == Level.level1:
            if self.health <= 0:
                pygame.mixer.Sound.play(farm_sound)
                self.level = Level.levelFarm
                self.health = 200
            elif self.health >= 200 and self.health < 300:
                pygame.mixer.Sound.play(oneLvlTwo_sound)
                self.level = Level.level2
        elif self.level == Level.level2:
            if self.health <= 199:
                pygame.mixer.Sound.play(twoLvlOne_sound)
                self.level = Level.level1
            elif self.health >= 300:
                pygame.mixer.Sound.play(twoLvlThree_sound)
                self.level = Level.level3               
        elif self.level == Level.level3:
            if self.health >= 200 and self.health < 300:
                pygame.mixer.Sound.play(threeLvltwo_sound)
                self.level = Level.level2
        elif self.level == Level.levelFarm:   
            if self.health <= 0:
                pygame.mixer.Sound.play(farmDeath_sound)
                self.Kill()
        
    #sprite/animation to level
    def GetSprite(self):
        if self.level == Level.level1:
            self.index += 0.05
            if self.index >= len(Humans.HumanList1):
                self.index = 0
            return Humans.HumanList1[math.floor(self.index)]
        elif self.level == Level.level2:
            self.index += 0.05
            if self.index >= len(Humans.HumanList2):
                self.index = 0
            return Humans.HumanList2[math.floor(self.index)]
        elif self.level == Level.level3:
            self.index += 0.05
            if self.index >= len(Humans.HumanList3):
                self.index = 0
            return Humans.HumanList3[math.floor(self.index)]
        elif self.level == Level.levelFarm:
            return Humans.farmHuman_img

    #power level of units around
    def PowerLevel(self):
        Units.UnitsAround(self)        
        vampLevel = 0
        for key, value in self.unitsIDAround.items():
            if isinstance(value, Vampires):
                lvlNum = value.level.value
                vampLevel += lvlNum
        return vampLevel
        
    #adjust unit level to level of vampires around 
    def Growth(self):
        vampLevel = self.PowerLevel()
        Units.areUnitsAround(self)
        if Units.areUnitsAround(self) == False:
            if self.level == Level.level1:
                self.health += 10
            elif self.level == Level.level2:
                self.health += 20
            elif self.level == Level.level3:
                self.health += 25
        elif Units.areUnitsAround(self) == True:
            if self.level.value >= vampLevel and self.health < 400:
                if vampLevel == 1:
                    self.health += 10
                elif vampLevel == 2:
                    self.health += 20
                elif vampLevel == 3:
                    self.health += 30
                elif vampLevel >= 4:
                    self.health += 45
            elif self.level.value >= 0 and self.level.value < vampLevel:
                if vampLevel == 1:
                    self.health -= 25
                elif vampLevel == 2:
                    self.health -= 35
                elif vampLevel == 3:
                    self.health -= 45
                elif vampLevel >= 4:
                    self.health -= 60
            elif self.level == Level.levelFarm and vampLevel > 5:
                    self.health -= 50
        self.checkHealth()

#check for changes to apply to units
def Update():
   for y in range(len(game_map)):
       for x in range(len(game_map[y])):
           if isinstance(game_map[y][x], Units) :
                unit = game_map[y][x]
                unit.movedThisTurn = False
                if isinstance(unit, Vampires):
                    Vampires.Interaction(unit)
                elif isinstance(unit, Humans):
                    Humans.Growth(unit)

#define humans' positions
unitHu1 = Humans((3, 1), Level.level1)
unitHu2 = Humans((5, 3), Level.level2)
unitHu3 = Humans((2, 5), Level.level3)
unitHu4 = Humans((4, 6), Level.level1)

#define vampires' positions
unitVam1 = Vampires((4, 0), Level.level1)
unitVam2 = Vampires((6, 2), Level.level1)
unitVam3 = Vampires((0, 4), Level.level1)
unitVam4 = Vampires((7, 6), Level.level3)

#initialization of new game
new_game = Game('images/background.png', 'images/splash_screen.png', SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT, MANUAL_CURSOR, 1)

new_game.run_game_loop()

pygame.quit()
quit()