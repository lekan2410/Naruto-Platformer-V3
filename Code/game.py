import pygame, sys
from map import *
import button
from animation_folder import import_folder
from setting import Level


pygame.init()


 # Set Up the drawing window
screen = pygame.display.set_mode((screen_width, screen_height))
minato = False
pain = False
minato_path = "./graphics/minato_character/"
pain_path = './graphics/pain_character/'
path = minato_path
level = Level(screen, path)



#all booleans
map_select = False
running = True
game_active = True
resume = False


#get FPS
clock = pygame.time.Clock()
menu_state = "menu"

#naruto specified music
kakazu_ost = "graphics/music/Kakazu.wav"
pain_ost = "graphics/music/Crimson_Flames.wav"
music = kakazu_ost

#Creating Music Player
def music_player():
    pygame.mixer.music.load(music)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1, 0.0, 5000)

#menu variables
#loading button images for menu state
resume_img = pygame.image.load("graphics/menu/resume.png")
options_img = pygame.image.load("graphics/menu/options.png")
quit_img = pygame.image.load("graphics/menu/quit.png")

#loading button images for options state
character_settingimg = pygame.image.load("graphics/menu/character.png")
audio_img = pygame.image.load("graphics/menu/audio.png")
back_img = pygame.image.load("graphics/menu/back.png")



#creating buttons for menu state
resume_button = button.Button(475, 100, resume_img, 1)
options_button = button.Button(475, 225, options_img, 1)
quit_button = button.Button(475, 350, quit_img, 1)

# creating buttons for options state
character_button = button.Button(475, 100, character_settingimg, 1)
audio_button = button.Button(475, 300, audio_img, 1)
back_button = button.Button(475, 500, back_img, 1)

# creating images and buttons for character state
minato_img = pygame.image.load("graphics/minato_character/start_icon/1.png")
pain_img = pygame.image.load("graphics/pain_character/start_icon/1.png")

minato_button = button.Button(300, 200, minato_img, 1)
pain_button = button.Button(600, 200, pain_img, 1)

# creating images and buttons for audio state
kakazu_img = pygame.image.load("graphics/music/kakazu.png")
pain_img = pygame.image.load("graphics/music/Pain.png")

kakazu_ostbutton = button.Button(300, 200, kakazu_img, 1) 
pain_ostbutton = button.Button(600, 200, pain_img, 1)


#Background Images
DBFZ_img = pygame.image.load("graphics/maps/DBFZmap.png")
windmill_img = pygame.image.load("graphics/maps/windmill.gif")


DBFZ_button = button.Button(300, 100, DBFZ_img, 0.5)
windmill_button = button.Button(600 ,100, windmill_img, 0.5)

#Drawing the background images
def draw_bg(img):
    scaled_bg = pygame.transform.scale(img, (screen_width, screen_height))
    screen.blit(scaled_bg, (0, 0))


while running:
    menu = True
    key = pygame.key.get_pressed()
    screen.fill("black")

    # different menu states
    if menu_state == "menu":
        if resume_button.draw(screen):
            resume = True
            music_player()
        elif options_button.draw(screen):
            menu_state = "options"
        elif quit_button.draw(screen):
            running = False
    
    if menu_state == "options":
        if character_button.draw(screen):
            menu_state = "character"
        elif audio_button.draw(screen):
            menu_state = "audio"
        elif back_button.draw(screen):
            menu_state = "menu"
    
    if menu_state == "character":
        if minato_button.draw(screen):
            path = minato_path
            minato = True
        elif pain_button.draw(screen):
            path = pain_path
        elif back_button.draw(screen):
            menu_state = "options"
    
    
    if menu_state == "audio":
        if kakazu_ostbutton.draw(screen):
            music = kakazu_ost
        elif pain_ostbutton.draw(screen):
            music = pain_ost
        elif back_button.draw(screen):
            menu_state = "options"    
    
    #load up the game
    if resume == True:
        draw_bg(DBFZ_img)
        level.character_select(path)
        level.run(path)

          
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        

    pygame.display.update()    
    clock.tick(60)
