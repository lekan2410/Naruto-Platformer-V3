import pygame
from animation_folder import import_folder
from datetime import datetime

steps = 10

jumping = True

y_gravity = 0.8
jump_height = -17
y_velocity = jump_height


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface, create_jump_particles, create_special_particles, ultimate_obj, target):
        super().__init__()
        # all of the players attributes
        self.minato = False
        self.pain = True
        self.surface = surface
        self.character_path = ""
        self.import_run_dust()
        self.frames = 0
        self.push = 0
        self.animation_speed = 0.4
        self.dust_speed = 0.8
        self.dust_frame = 0
        self.status = 'idle'
        self.image = pygame.Surface([64, 64]) 
        self.rect = self.image.get_rect(topleft = pos)
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.shift = 8
        self.create_jump_particles = create_jump_particles
        self.create_special_particles = create_special_particles
        self.ultimate_obj = ultimate_obj
        self.facing_right = True
        self.facing_left = False
        self.right = True
        self.left = False
        self.ground = False
        self.ceiling = False
        self.attack_type = 0
        self.target = target
        self.attacking = False
        self.attack_cooldown = 0
        self.ultimate_cooldown = 0
        self.animation_cooldown = 0
        self.health = 100
        self.energy = 100
        self.action = 0
        self.death = False
        self.block = False
        self.ultimate = False
        self.charge = False
        self.ultimate_activate = False
        self.jumping = False
        self.intro = False
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
        keys = pygame.key.get_pressed()
        
        # Ensures the player does the correct animations
        if self.direction.y > 1:
            self.status = 'fall'
        elif self.direction.y < 0:
            self.status = 'jump'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'
                self.block = False
        
        # Executes blocking and ensures player can't move
        if keys[pygame.K_l]:
            self.status = 'block'
            self.block = True
            self.direction.x = 0
        
        if self.death == False:
            if keys[pygame.K_j] and self.energy > 0:
                self.status = 'dash'
                self.energy -= 1
            
            if keys[pygame.K_c] and self.energy <= 100:
                self.status = 'charge'
                self.energy += 1.5
                self.direction.x = 0
                self.charge = True
            
            if self.status != 'charge':
                self.charge = False
            
            if keys[pygame.K_p] and self.energy >= 80 and self.ultimate_cooldown == 0:
                self.ultimate = True
                self.ultimate_activate = True
                self.energy -= 50
        
    
    def dash(self):
        # ensures the player dashes into the correct way
        if self.facing_right and self.energy > 0:
            self.direction.x = 4
        elif self.facing_left and self.energy > 0:
            self.direction.x = -4
        else:
            self.direction.x = 0
    
    def dashing(self):
        keys = pygame.key.get_pressed()
        
        # executes dashing as long as player is not dead
        if self.death == False:
            if pygame.KEYDOWN and keys[pygame.K_j] and self.charge == False:
                self.dash()
    
        
    def character_settings(self, path):
        # getting the images of the player

        self.character_path = path

        self.animations = {'idle':[], 'run':[], 'jump':[], 'push':[], 'fall':[], 'dash':[], 'attack_1':[] ,'attack_2':[], 'death':[], 'block':[], 'charge':[], 'hit':[], 'ultimate':[]}
        
         
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
        
        # prevents the player from moving if these states are true
        if self.attacking == False and self.death == False and self.block == False and self.charge == False:
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
                self.jumping = True
            else:
                self.jumping = False
            
            # checks if player has enough energy to perform ultimate
            if key[pygame.K_p] and self.energy >= 80:
                self.ultimate_active = True
                self.ultimate_obj(self.rect.center)
            
            
            #adding special particles for player jumping
            if self.ground and self.direction.y < 0:
                self.create_special_particles(self.rect.center)
            
            
            #attack movements
            if key[pygame.K_k]:
                self.attack_type = 1
            elif key[pygame.K_n]:
                self.attack_type = 2
            else:
                self.attack_type = 0
            
            #attack cooldown
            if self.attack_cooldown > 0:
                self.attack_cooldown -= 1
            
            if self.animation_cooldown > 0:
                self.animation_cooldown -= 1
            
            
            #ultimate cooldown
            if self.ultimate_cooldown > 0:
                self.ultimate_cooldown -= 1

    
            # if player is dead
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
        
       #checking if the player has attacked
       if self.attacking == True:
        if self.attack_type == 1:
            self.status = 'attack_1'
        elif self.attack_type == 2:
            self.status = 'attack_2'
        

        animation_cooldown = 20
        
        #sorting out how long the animation lasts for after the player has attacked
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frames += 1.5
            self.update_time = pygame.time.get_ticks()
        
        if self.frames >= len(self.animations[self.status]):
            self.frames = 0
        
            #check if an attack was executed
            if self.status == 'attack_1' or self.status == 'attack_2':
                self.attacking = False
                self.attack_cooldown = 20

    def ultimate_attacking(self):
        # Player has executed ultimate
        if self.ultimate == True:
            self.status = 'ultimate'

            animation_cooldown = 70
            
            # how long the animation lasts for after the player has used their ultimate
            if pygame.time.get_ticks() - self.update_time > animation_cooldown:
                self.frames += 1
                self.update_time = pygame.time.get_ticks()
            
            if self.frames >= len(self.animations[self.status]):
                self.frames = 0
                
                # check if an ultimate was executed
                if self.status == 'ultimate':
                    self.ultimate = False
                    self.ultimate_activate = False
                    self.ultimate_cooldown = 1
        
        
    def death_animate(self):
        
        #checking if the player is dead
        if self.death == True:
            self.status = 'death'
            self.direction.x = 0

            animation_cooldown = 1
            
            # how long the animation lasts after the player has been defeated
            if pygame.time.get_ticks() - self.update_time > animation_cooldown:
                self.frames += 0.5
                self.update_time = pygame.time.get_ticks()
            
            if self.frames >= len(self.animations[self.status]):
                self.frames = 0
            
                #don't allow the player to change animation
                if self.status == 'death':
                    self.frames = len(self.animations[self.status]) - 1
    

    def update(self):
        # runs all the functions
        self.movement()
        self.animation_status()
        self.dust_run_animations()
        self.animation_update()
        self.ultimate_attacking()
        self.death_animate()
        self.dashing()

        
    

        
        

            

    
    
    
    
    





        