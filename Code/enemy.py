import pygame
from animation_folder import import_folder
from datetime import datetime

steps = 10

jumping = True

y_gravity = 0.8
jump_height = -17
y_velocity = jump_height

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, surface, create_jump_particles, create_special_particles, target):
        super().__init__()
        # all of the players attributes
        self.character_settings()
        self.import_run_dust()
        self.frames = 0
        self.push = 0
        self.surface = surface
        self.animation_speed = 0.10
        self.dust_speed = 0.8
        self.dust_frame = 0
        self.image = self.animations['idle'][self.frames]
        self.rect = self.image.get_rect(topleft = pos)
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.shift = 8
        self.status = 'idle'
        self.create_jump_particles = create_jump_particles
        self.create_special_particles = create_special_particles
        self.facing_right = True
        self.facing_left = False
        self.right = True
        self.left = False
        self.ground = False
        self.ceiling = False
        self.attack_type = 0
        self.special_move = 0
        self.target = target
        self.attacking = False
        self.attack_cooldown = 0
        self.health = 100
        self.special_attacking = False
        self.death = False

        self.update_time = pygame.time.get_ticks()


    def import_run_dust(self):
        # getting dust particles
        self.dust_run = import_folder("./graphics/dust/dust_particles/run")


    def dust_run_animations(self):
         #implenting dust particles on player
         if self.status == 'run' and self.ground:
            self.dust_frame += self.dust_speed
            if self.dust_frame >= len(self.dust_run):
                self.dust_frame = 0
            
            dust_particles = self.dust_run[int(self.dust_frame)]
            
            # dust particles facing 
            if self.facing_right:
                pos = self.rect.midleft
                self.surface.blit(dust_particles, pos)
            else:
                pos = self.rect.midright
                flipped_particles = pygame.transform.flip(dust_particles, True, False)
                self.surface.blit(flipped_particles, pos)
    
    
    
    
    def animation_status(self):
        # getting status for player animation
        if self.direction.y > 1:
            self.status = 'fall'
        elif self.direction.y < 0:
            self.status = 'jump'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'
        
    
    def character_settings(self):
        # getting the images of the player
        character_path = './graphics/momoshiki_character/'
        self.animations = {'idle':[], 'run':[], 'jump':[], 'spear':[], 'hammer':[], 'fall':[], 'death':[], 'special_move1':[], 'special_move2':[]}
        
        # setting the animations
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)
        
    
    
    def animate(self):
        animation = self.animations[self.status]
        
        #changing between images
        self.frames += self.animation_speed
        
        # continous loop of images
        if self.frames >= len(animation):
            self.frames = 0
        
        image = animation[int(self.frames)]
        
        # corresponds to player movement
        if self.facing_right:
            self.image = image
        else:
            flipped = pygame.transform.flip(image, True, False) 
            self.image = flipped  
        

        # positioning the player on the map
        if self.ceiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)
        elif self.ceiling and self.right:
            self.rect = self.image.get_rect(topright = self.rect.topleft)
        elif self.ceiling and self.left:
            self.rect = self.image.get_rect(topleft = self.rect.topright)
        elif self.ground:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        elif self.ground and self.right:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.ground and self.left:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        else:
            self.rect = self.image.get_rect(center = self.rect.center)
  
    

    def movement(self):
        
        #input from player
        key = pygame.key.get_pressed()
        

        if self.attacking == False and self.special_attacking == False and self.death == False:
            if key[pygame.K_d]:
                self.direction.x = 1
                self.facing_right = True  
                self.facing_left = False
            elif key[pygame.K_a]:
                self.direction.x  = -1
                self.facing_right = False   
                self.facing_left = True
            else:
                self.direction.x = 0
        
            # checking if the player has jumped
            if key[pygame.K_SPACE] and self.ground:
                self.jump()
                self.create_jump_particles(self.rect.center)
            
            #adding special particles for player jumping
            if self.ground and self.direction.y < 0:
                self.create_special_particles(self.rect.center)
        
            
            #attack movements
            if key[pygame.K_o]:
                self.attack_type = 1
            if key[pygame.K_p]:
                self.attack_type = 2

             #attack cooldown
            if self.attack_cooldown > 0:
                self.attack_cooldown -= 1
            
            #if enemy is dead
            if self.health <= 0:
                self.death = True

    def gravity(self):
        # determines player gravity
        global y_velocity
       

        self.direction.y += y_gravity
        self.rect.y += self.direction.y 

    
    def jump(self):
        # determines how high the player jumps
        self.direction.y = jump_height

    def animation_update(self):
        
       if self.attacking == True:
        if self.attack_type == 1:
            self.status = 'spear'
        elif self.attack_type == 2:
            self.status = 'hammer'
          
        animation_cooldown = 50
        

        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frames += 1
            self.update_time = pygame.time.get_ticks()
        
        if self.frames >= len(self.animations[self.status]):
            self.frames = 0
        
            #check if an attack was executed
            if self.status == 'spear' or self.status == 'hammer':
                self.attacking = False
                self.attack_cooldown = 50

    
    def death_animate(self):
    
        if self.death == True:
            self.status = 'death'

            animation_cooldown = 50

            if pygame.time.get_ticks() - self.update_time > animation_cooldown:
                self.frames += 1
                self.update_time = pygame.time.get_ticks()
            
            if self.frames >= len(self.animations[self.status]):
                self.frames = 0
            
                #don't allow the player to change animation
                if self.status == 'death':
                    self.frames = len(self.animations[self.status]) - 1
        
        


    def update(self):
        # runs all the functions
        self.movement()
        self.animate()
        self.animation_status()
        self.death_animate()
        self.dust_run_animations()
        self.animation_update()
     



#Website for removing background: https://www.remove.bg/
