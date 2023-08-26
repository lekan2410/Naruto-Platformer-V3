import pygame, sys
from map import *
import button
from animation_folder import import_folder
from setting import Level

# setting up the volume
pygame.init()
pygame.mixer.pre_init(44100, 16, 1, 4096)



 # Set Up the drawing window
screen = pygame.display.set_mode((screen_width, screen_height))

#creating the paths
borushiki_path = "./graphics/borushiki_character/"
itachi_path = './graphics/itachi_character/'
lastsasuke_path = './graphics/lastsasuke_character/'
final_sasuke_path = './graphics/finalsasuke_character/'
pain_path = './graphics/pain_character/'
naruto_path = './graphics/naruto_character/'
path = naruto_path

level = Level(screen)


#all booleans
map_select = False
running = True
game_active = True
resume = False


#get FPS
clock = pygame.time.Clock()
menu_state = "menu"


#menu variables
#loading button images for menu state
resume_img = pygame.image.load("graphics/menu/resume.png").convert_alpha()
options_img = pygame.image.load("graphics/menu/options.png").convert_alpha()
quit_img = pygame.image.load("graphics/menu/quit.png").convert_alpha()

#loading button images for options state
character_settingimg = pygame.image.load("graphics/menu/character.png").convert_alpha()
audio_img = pygame.image.load("graphics/menu/audio.png").convert_alpha()
back_img = pygame.image.load("graphics/menu/back.png").convert_alpha()

#creating buttons for menu state
resume_button = button.Button(475, 100, resume_img, 1)
options_button = button.Button(475, 225, options_img, 1)
quit_button = button.Button(475, 350, quit_img, 1)

# creating buttons for options state
character_button = button.Button(475, 100, character_settingimg, 1)
back_button = button.Button(475, 500, back_img, 1)

# creating images state
borushiki_img = pygame.image.load("graphics/borushiki_character/start_icon/1.png").convert_alpha()
lastsasuke_img = pygame.image.load("graphics/lastsasuke_character/start_icon/1.png").convert_alpha()
itachi_img = pygame.image.load("graphics/itachi_character/start_icon/1.png").convert_alpha()
pain_img = pygame.image.load("graphics/pain_character/start_icon/1.png").convert_alpha()
naruto_img = pygame.image.load("graphics/naruto_character/start_icon/1.png").convert_alpha()
finalsasuke_img = pygame.image.load("graphics/finalsasuke_character/start_icon/1.png").convert_alpha()

# creating the buttons for each character
borushiki_button = button.Button(300, 200, borushiki_img, 1)
itachi_button = button.Button(600, 200, itachi_img, 1)
lastsasuke_button = button.Button(900, 200, lastsasuke_img, 1)
pain_button = button.Button(600, 400, pain_img, 1)
naruto_button = button.Button(300, 400, naruto_img, 1)
finalsasuke_button = button.Button(900, 400, finalsasuke_img, 1)

#Background Images
DBFZ_img = pygame.image.load("graphics/maps/forest.png").convert_alpha()


DBFZ_button = button.Button(300, 100, DBFZ_img, 0.5)


#Drawing the background images

while running:
    menu = True
    key = pygame.key.get_pressed()
    screen.fill("black")

    # different menu states
    if menu_state == "menu":
        if resume_button.draw(screen):
            resume = True 
        elif options_button.draw(screen):
            menu_state = "options"
        elif quit_button.draw(screen):
            running = False
    
    # Options state
    if menu_state == "options":
        if character_button.draw(screen):
            menu_state = "character"
        elif back_button.draw(screen):
            menu_state = "menu"
    
    # changing character state
    if menu_state == "character":
        # changes enemy once player has clicked on a character
        if borushiki_button.draw(screen):
            path = borushiki_path
        elif itachi_button.draw(screen):
            path = itachi_path
        elif lastsasuke_button.draw(screen):
            path = lastsasuke_path
        elif pain_button.draw(screen):
            path = pain_path
        elif naruto_button.draw(screen):
            path = naruto_path
        elif finalsasuke_button.draw(screen):
            path = final_sasuke_path
        elif back_button.draw(screen):
            menu_state = "options"
        

    
    #load up the game
    if resume == True:
        level.draw_bg(screen)
        level.character_select(path)
        level.change_enemies_n_maps()
        level.load_sounds(path)
        level.run()

          
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        
    pygame.display.update()    
    clock.tick(60)
