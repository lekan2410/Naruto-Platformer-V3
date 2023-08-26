import pygame
import random
import time
from tiles import Tile
from map import screen_width, screen_height
from animation_folder import import_folder
from particles import Particles
from player import Player  
from enemy import Enemy 
from map import level1, level2, level3, level4
from ultimate_obj import Ultimate_Obj




class Level:
    def __init__(self, surface):
        # Level attributes
        self.display_surface = surface
        self.level = level4
        self.setup_level(self.level)
        self.shift = 0
        self.ultimate_pos = 0
        self.current_x = 0
    
        # special effects
        self.particles = pygame.sprite.GroupSingle()
        self.land_particles = pygame.sprite.GroupSingle()
        self.ultimate = pygame.sprite.GroupSingle()
        self.momoshiki_attack = pygame.sprite.GroupSingle()
        
        #sound effect
        self.player_sounds = ''

        self.player_onground = False

        #healthbar
        self.yellow = (255, 255, 0)
        self.red = (255, 0, 0)
        self.white = (255, 255, 255)

        #energybar
        self.blue = (0, 150, 255)
        self.black = (0, 0, 0)
        
    
    def player_on_ground(self):
        # checking if player is on the ground
        if self.player.sprite.ground:
            self.player_onground = True
        else:
            self.player_onground = False
    
    def create_jump_particles(self, pos):
        # player attributes
        player = self.player.sprite
        enemy = self.enemy.sprite
        jump_pos = pygame.math.Vector2(5, 5)
        flipped_jump_pos = pygame.math.Vector2(3, -5)
        
        # jump particles corresponding to the player movements
        if player.facing_right:
            pos += jump_pos
        else:
            pos -= flipped_jump_pos

        if enemy.facing_right:
            pos += jump_pos
        else:
            pos -= flipped_jump_pos
        
        # adding jump particles
        jump = Particles(pos, 'jump')
        self.particles.add(jump)
    
    
    def create_special_particles(self, pos):
        land_pos = pygame.Vector2(-40, 10)
        
        # if player is about to jump
        if self.player.sprite.ground and not self.player_onground and self.land_particles.sprites():
            pos += land_pos
        
        # adding special particles
        special  = Particles(pos, 'special')
        self.land_particles.add(special)
    
    def ultimate_obj(self, pos):
        player = self.player.sprite
        
        # Position for the ultimate object
        self.rock_pos = pygame.math.Vector2(0, -20)
        pos += self.rock_pos
        
        # Ensuring ultimate attack is visible
        ultimate = Ultimate_Obj(pos, player.character_path)
        self.ultimate.add(ultimate)


    def setup_level(self, layout):
        # getting attributes
        self.player = pygame.sprite.GroupSingle()
        self.tiles = pygame.sprite.Group()
        self.enemy = pygame.sprite.GroupSingle()
      
        # iterating through the map
        for row_index, col in enumerate(layout):
            for col_index, cell in enumerate(col):
                x = col_index * 64
                y = row_index * 64
                # creating tiles
                if cell == "X":
                    tile = Tile((x, y), 64)
                    self.tiles.add(tile)
                # creating player
                elif cell == "P" :
                    player = Player((x, y), self.display_surface, self.create_jump_particles, self.create_special_particles, self.ultimate_obj, self.enemy)
                    self.player.add(player)
                # creating enemy
                elif cell == "E":
                    enemy = Enemy((x, y), self.display_surface, self.create_jump_particles, self.create_special_particles, self.player)
                    self.enemy.add(enemy)
                                
                    
    def player_scroll(self):
        # getting player attribute
        player = self.player.sprite
        player_direction = player.direction.x
        width = screen_width / 4
        
        # moving the map when the player moves left or right
        if player.rect.centerx < width and player_direction < 0:
            self.shift = 8
            player.speed = 0
        elif player.rect.centerx > screen_width - width and player_direction > 0:
            self.shift = -8
            player.speed = 0
        elif self.level == level4:
            self.shift = 0
            player.speed = 8
        else:
            self.shift = 0
            player.speed = 8
        
    
    def collision_y(self):
        # applying attributes
        player = self.player.sprite
        # allowing the player to jump
        player.gravity()
       
       # checking for collisions between tiles
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.ceiling = True
            
            # checking if player isn't on ground or ceiling
            if player.ground and player.direction.y < 0 or player.direction.y > 1:
                player.ground = False
            elif player.ceiling and player.direction.y > 0:
                player.ceiling = False
            
        
                    
    

    def collision_x(self):

        # player attribute for collision
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        
        # checking for collistion 
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.left = True
                    self.current_x = player.rect.left
                    player.direction.x = 0
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.direction.x = 0
                    player.right = True
                    self.current_x = player.rect.left
        
        # if the player isn't left or right to the tiles
        if player.left and (player.left < self.current_x or player.direction.x >= 0):
            player.left = False
        elif player.right and (player.right > self.current_x or player.direction.x <= 0):
            player.right = False
    
            
    
     
    def enemy_collision_y(self):
        # applying attributes
        enemy = self.enemy.sprite

        #allowing enemy to jump
        enemy.gravity()
       
       # checking for collisions between tiles
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(enemy.rect):
                if enemy.direction.y > 0:
                    enemy.rect.bottom = sprite.rect.top
                    enemy.direction.y = 0
                    enemy.ground = True
                elif enemy.direction.y < 0:
                    enemy.rect.top = sprite.rect.bottom
                    enemy.direction.y = 0
                    enemy.ceiling = True
            
            # checking if enemy isn't on ground or ceiling
            if enemy.ground and enemy.direction.y < 0 or enemy.direction.y > 1:
                enemy.ground = False
            elif enemy.ceiling and enemy.direction.y > 0:
                enemy.ceiling = False

    
    def enemy_collision_x(self):

        # player attribute for collision
        enemy = self.enemy.sprite
        enemy.rect.x += enemy.direction.x * enemy.speed
        
        # checking for collistion 
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(enemy.rect):
                if enemy.direction.x < 0:
                    enemy.rect.left = sprite.rect.right
                    enemy.left = True
                    self.current_x = enemy.rect.left
                    enemy.direction.x = 0
                elif enemy.direction.x > 0:
                    enemy.rect.right = sprite.rect.left
                    enemy.direction.x = 0
                    enemy.right = True
                    self.current_x = enemy.rect.left
        
        # if the player isn't left or right to the tiles
        if enemy.left and (enemy.left < self.current_x or enemy.direction.x >= 0):
            enemy.left = False
        elif enemy.right and (enemy.right > self.current_x or enemy.direction.x <= 0):
            enemy.right = False
        
    def player_attack(self):
            key = pygame.key.get_pressed()
            enemy = self.enemy.sprite
            player = self.player.sprite

            # Checks keys being pressed to execute attack
            if player.attacking == False:
                if key[pygame.K_k]:
                    self.player_attacking(self.display_surface, enemy.rect)
                if key[pygame.K_n]:
                    self.player_attacking(self.display_surface, enemy.rect)
            
            # Checks keys being prssed to execute ultimate
            if key[pygame.K_p] and player.ultimate == True:
                self.player_ultimate_attacks()
        


        
    def player_attacking(self, surface, target):
        player = self.player.sprite
        enemy = self.enemy.sprite
        
        # implementing a cooldown to prevent spamming
        if player.attack_cooldown == 0:
            player.attacking = True
            attacking_rect = pygame.Rect(player.rect.centerx - (2 * player.rect.width * player.facing_left), player.rect.y, 2 * player.rect.width, player.rect.height)
            
            # hitbox hitting enemy
            if attacking_rect.colliderect(target):
                enemy.health -= 10
        
           # pygame.draw.rect(surface, (0, 255, 0), attacking_rect)
    
    def player_ultimate_attacks(self):
        player = self.player.sprite
        enemy = self.enemy.sprite
        ultimate = self.ultimate.sprite
         
        # Ensures the attacks goes the correct way
        if player.ultimate_cooldown == 0 and player.ultimate == True and player.attacking == False and player.charge == False:
            if player.facing_right:
                self.ultimate_pos = 20
            elif player.facing_left:
                self.ultimate_pos = -20
            
            # hitbox for the ultimate
            if ultimate.rect.colliderect(enemy.rect):
                enemy.health -= 5
            
        
            # pygame.draw.rect(self.display_surface, (0, 255, 0), ultimate.rect)
        
    
    def enemy_attacks(self):
            enemy = self.enemy.sprite
            player = self.player.sprite
            
            # Enemy executing attacking
            if enemy.attacking == False:
                if enemy.attack_type == 1:
                    self.enemy_attacking(player.rect)
                if enemy.attack_type == 2:
                    self.enemy_attacking(player.rect)
                    
                

   
    def enemy_attacking(self, target):
        player = self.player.sprite
        enemy = self.enemy.sprite
        
        # prevents enemy from spamming
        if enemy.attack_cooldown == 0:
            enemy.attacking = True
            attacking_rect = pygame.Rect(enemy.rect.centerx - (2 * enemy.rect.width * enemy.facing_left), enemy.rect.y, 2 * enemy.rect.width, enemy.rect.height)
            
            # hitbox colliding with player
            if attacking_rect.colliderect(target) and player.block == False:
                player.health -= 30
            
            # hitbox colliding with player while player is blocking
            if attacking_rect.colliderect(target) and player.block == True:
                player.health -= 15
        
            # pygame.draw.rect(surface, (0, 255, 0), attacking_rect)
     

    
    def draw_health_bar(self, health, x, y):
        # designing the health bar
        ratio = health / 100
        pygame.draw.rect(self.display_surface, self.white, (x - 2 , y - 2, 404, 34))
        pygame.draw.rect(self.display_surface, self.red, (x, y, 400, 30))
        pygame.draw.rect(self.display_surface, self.yellow, (x, y, 400 * ratio, 30))
    
    def draw_energy_bar(self, energy, x, y):
        #designing energy bar
        ratio = energy / 100
        pygame.draw.rect(self.display_surface, self.white, (x - 2 , y - 2, 404, 34)) 
        pygame.draw.rect(self.display_surface, self.black, (x, y, 400, 30))
        pygame.draw.rect(self.display_surface, self.blue, (x, y, 400 * ratio, 30))   

    
    def enemy_ai(self):
        #Enemy attacks
        attacks = ['attack1', 'attack2']
        

        enemy = self.enemy.sprite
        player = self.player.sprite
        ultimate = self.ultimate.sprite


        # making sure the enemy chases the player
        dirvect = pygame.math.Vector2(player.rect.x - enemy.rect.x, player.rect.y - enemy.rect.y)
       
        
        
        # checking if the enemy is jumping or running on ground
        if dirvect.length_squared() > 0 and enemy.ground:
            dirvect.scale_to_length(enemy.speed - 3)
            enemy.status = 'run'
        elif dirvect.length_squared() > 0 and enemy.ground == False:
            dirvect.scale_to_length(enemy.speed)
            enemy.status = 'jump'
            enemy.status = 'fall'

 
       # ensuring that the player attacks once it collides with the player
        if enemy.rect.colliderect(player.rect) and enemy.death == False:
            enemy.status = 'idle'
            if enemy.attack_cooldown == 0:
                attack = random.choice(attacks)
                if attack == attacks[0]:
                    enemy.attack_type = 1
                    enemy.status = 'attack_1'
                elif attack == attacks[1]:
                    enemy.status = 'attack_2'
                    enemy.attack_type = 2
        
        # positioning the enemy to face the correct way
        if dirvect.x < 0:
            enemy.facing_right = False
        elif dirvect.x > 0:
            enemy.facing_right = True

        # positioning the enemy to face the player
        if enemy.rect.colliderect(player.rect) and player.facing_right:
            enemy.facing_right = False
        elif enemy.rect.colliderect(player.rect) and player.facing_right == False:
            enemy.facing_right = True
        
        # ensuring that the enemy is dead and doesn't follow the player
        if enemy.health > 0:
            enemy.rect.move_ip(dirvect)
        elif enemy.health <= 0 and enemy.status == 'run':
            enemy.rect.move_ip(0, 0)
            enemy.status = 'death'
        
        # animations to show that the player has been hit
        if player.attacking and player.rect.colliderect(enemy.rect):
            enemy.status = 'hit'
        elif enemy.attacking and enemy.rect.colliderect(player.rect) and player.block == False:
            player.status = 'hit'
        elif player.ultimate and ultimate.rect.colliderect(enemy.rect):
            enemy.rect.move_ip(0, 0)
            enemy.status = 'hit_2'
        
        # Ensuring the enemy also jumps with the player
        if player.jumping == True:
            enemy.jump()
           
    
    def character_select(self, path):
        # Ensures player can change into preferred character
        player = self.player.sprite
        
        player.character_settings(path)
    
    def change_enemies_n_maps(self):
        enemy = self.enemy.sprite
        
        # All enemies
        self.characters = ['./graphics/edomadara_character/','./graphics/pre-jubidara_character/', './graphics/jubito_character/',
                           './graphics/jubidara_character/','./graphics/kaguya_character/', './graphics/momoshiki_character/', 
                           './graphics/isshiki_character/']
        
        # first enemy
        true_path = './graphics/obito_character/'

        if enemy.health <= 700: true_path = self.characters[0]
        if enemy.health <= 600: true_path = self.characters[1]
        if enemy.health <= 500: true_path = self.characters[2]
        if enemy.health <= 400: true_path = self.characters[3]
        if enemy.health <= 300: true_path = self.characters[4]
        if enemy.health <= 200: true_path = self.characters[5]
        if enemy.health <= 100: true_path = self.characters[6]
       
        # loads the enemies
        enemy.character_settings(true_path)
    
    
    def add_health(self):
        player = self.player.sprite
        enemy = self.enemy.sprite
        
        # Enemy health state
        health =  {1: 800, 2: 795, 3: 700, 4: 695, 5: 600, 6: 595, 7: 500, 8: 495, 9: 400, 10: 395, 11: 300, 12: 295,
                   13: 200, 14: 195, 15: 100, 16: 95}
        
        # Ensures player gets back to full health once enemy has been defeated
        for helth in health.keys():
            if enemy.health == health[helth]:
                player.health = 100
                
    # playing the sounds
    def play_sounds(self):
        pygame.mixer.music.load(self.player_sounds)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(0, 0.0, 00) 
    
    # loading sounds
    def load_sounds(self, path):
        player = self.player.sprite

        self.player_sounds = path + 'sound_effects'

        keys = pygame.key.get_pressed()
        
        #Sound plays only when player is alive
        if player.death == False:
            # ultimate sound
            if keys[pygame.K_p] and player.ultimate:
                self.player_sounds = self.player_sounds + '/ultimate.wav'
                self.play_sounds()
            # attacking sound
            elif player.attacking:
                self.player_sounds = self.player_sounds + '/attack.wav'
                self.play_sounds()
            # dashing sound
            elif keys[pygame.K_j]:
                self.player_sounds = self.player_sounds + '/dash.wav'
                self.play_sounds()
    
    def draw_bg(self, screen):
        enemy = self.enemy.sprite
        
        # first level
        level = './graphics/maps/forest.png'
        
        # changing the level based on enemy's health 
        if enemy.health <= 700: level = './graphics/maps/war_1.png'
        if enemy.health <= 500: level = './graphics/maps/kaguya.png' 
        if enemy.health <= 200:  level = './graphics/maps/war_2.png'
        if enemy.health <= 100:  level = './graphics/maps/isshiki.png'
        
        # loading each image and changing the background
        img = pygame.image.load(level)

        scaled_bg = pygame.transform.scale(img, (screen_width, screen_height)).convert_alpha()
        screen.blit(scaled_bg, (0, 0))
    
    

    # all previous functions are performed in this function
    def run(self):

        #Getting player and enemy
        player = self.player.sprite
        enemy = self.enemy.sprite

        self.tiles.update(self.shift)
        self.tiles.draw(self.display_surface)

        
        # Particles attributes
        self.particles.draw(self.display_surface)
        self.particles.update(self.shift)
       
        # Land Particles attributes
        self.land_particles.draw(self.display_surface)
        self.land_particles.update(self.shift)
        
        
        # Player attributes
        self.player.draw(self.display_surface)
        self.player.update()
        self.player_attack()
        self.player_on_ground()
        self.collision_x()
        self.collision_y()
        self.add_health()

        # Enemy attributes
        self.enemy.draw(self.display_surface)
        self.enemy.update()
        self.enemy_attacks()
        self.enemy_collision_x()
        self.enemy_collision_y()
        self.enemy_ai()


        #drawing health bars
        self.draw_health_bar(player.health, 20, 20)
        self.draw_health_bar(enemy.health, 750, 20)

        #drawing energy bars
        self.draw_energy_bar(player.energy, 50, 50)
        
        # Player ultimate attributes
        self.ultimate.draw(self.display_surface)
        self.ultimate.update(self.ultimate_pos)



    




    


     





        

    
        

    