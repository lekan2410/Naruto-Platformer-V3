import pygame
from animation_folder import import_folder
from datetime import datetime
import random

steps = 10

jumping = True

y_gravity = 0.8
jump_height = -17
y_velocity = jump_height

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, surface, create_jump_particles, create_special_particles, target):
        super().__init__()
        # all of the enemys attributes
        self.health = 800
        self.death = False
        self.surface = surface
        self.character_path = ""
        self.import_run_dust()
        self.frames = 0
        self.push = 0
        self.animation_speed = 0.4
        self.dust_speed = 0.8
        self.dust_frame = 0
        self.image = pygame.Surface([64, 64])
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
        self.special_attacking = False
        self.stage = 0
        self.change = False

        self.update_time = pygame.time.get_ticks()


    def import_run_dust(self):
        # getting dust particles
        self.dust_run = import_folder("./graphics/dust/dust_particles/run")


    def dust_run_animations(self):
         #implenting dust particles on enemy
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
        # getting status for enemy animation
        if self.direction.y > 1:
            self.status = 'fall'
        elif self.direction.y < 0:
            self.status = 'jump'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'
        
    
    def character_settings(self, path):
        # getting the images of the enemy

        self.character_path = path

        self.animations = {'idle':[], 'run':[], 'jump':[], 'attack_1':[], 'attack_2':[], 'fall':[], 'death':[], 'hit':[], 'hit_2':[]}
        

        # setting the animations
        for animation in self.animations.keys():
            full_path = self.character_path + animation
            self.animations[animation] = import_folder(full_path)
        
        
        animation1 = self.animations[self.status]
        
        #changing between images
        self.frames += self.animation_speed
        
        # continous loop of images
        if self.frames >= len(animation1):
            self.frames = 0
        
        image = animation1[int(self.frames)]
        
        # corresponds to enemy movement
        if self.facing_right:
            self.image = image
        else:
            flipped = pygame.transform.flip(image, True, False) 
            self.image = flipped  

        # positioning the enemy on the map
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
        
        if self.attacking == False and self.special_attacking == False and self.death == False:
            #adding special particles for enemy jumping
            if self.ground and self.direction.y < 0:
                self.create_special_particles(self.rect.center)

             #attack cooldown
            if self.attack_cooldown > 0:
                self.attack_cooldown -= 1
            
            #if enemy is dead
            if self.health <= 0:
                self.death = True
            elif self.health > 0:
                self.death = False
        

    def gravity(self):
        # determines enemy gravity
        global y_velocity
       

        self.direction.y += y_gravity
        self.rect.y += self.direction.y 

    
    def jump(self):
        # determines how high the enemy jumps
        self.direction.y = jump_height

    def animation_update(self):
       # Executes the attacking
       if self.attacking == True:
        if self.attack_type == 1:
            self.status = 'attack_1'
        elif self.attack_type == 2:
            self.status = 'attack_2'
          
        animation_cooldown = 50
        
        # Checks how long the animation lasts for
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frames += 1
            self.update_time = pygame.time.get_ticks()
        
        if self.frames >= len(self.animations[self.status]):
            self.frames = 0
        
            #check if an attack was executed
            if self.status == 'attack_1' or self.status == 'attack_2':
                self.attacking = False
                self.attack_cooldown = 50

    
    def death_animate(self):
        # Enemy has died
        if self.death == True:
            self.status = 'death'

            animation_cooldown = 50
            
            # checks how long the animation lasts for
            if pygame.time.get_ticks() - self.update_time > animation_cooldown:
                self.frames += 1
                self.update_time = pygame.time.get_ticks()
            
            if self.frames >= len(self.animations[self.status]):
                self.frames = 0
            
                #don't allow the enemy to change animation
                if self.status == 'death':
                    self.frames = len(self.animations[self.status]) - 1
        

    def update(self):
        # runs all the functions
        self.movement()
        self.animation_status()
        self.dust_run_animations()
        self.animation_update()
        self.death_animate()
     
