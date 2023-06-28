import pygame
from tiles import Tile
from map import screen_width, screen_height
from animation_folder import import_folder
from particles import Particles
from player import Player  
from enemy import Enemy
from door import Door 
from map import level1, level2, level3, level4
import button


class Level:
    def __init__(self, surface, player):
        # Level attributes
        self.display_surface = surface
        self.level = level4
        self.character_path = player
        self.setup_level(self.level)
        self.shift = 0
        self.current_x = 0
    
        # special effects
        self.particles = pygame.sprite.GroupSingle()
        self.land_particles = pygame.sprite.GroupSingle()
        self.tensei = pygame.sprite.GroupSingle()
        self.momoshiki_attack = pygame.sprite.GroupSingle()
        
        #position for the chibaku tensei to move in 
        self.rock_pos = pygame.math.Vector2(5, 5)
        self.rock_move_pos = 0

        self.player_onground = False

        #healthbar
        self.yellow = (255, 255, 0)
        self.red = (255, 0, 0)
        self.white = (255, 255, 255)
        
    
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

    def setup_level(self, layout):
        # getting attributes
        self.player = pygame.sprite.GroupSingle()
        self.tiles = pygame.sprite.Group()
        self.tensei = pygame.sprite.GroupSingle()
        self.door = pygame.sprite.Group()
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
                    player = Player(self.character_path, (x, y), self.display_surface, self.create_jump_particles, self.create_special_particles, self.enemy)
                    self.player.add(player)
                # creating door
                elif cell == "D":
                    door = Door((x, y))
                    self.door.add(door)
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
        
    def enemy_scroll(self):
        # getting player attribute
        enemy = self.enemy.sprite
        enemy_direction = enemy.direction.x
        width = screen_width / 4
        
        # moving the map when the player moves left or right
        if enemy.rect.centerx < width and enemy_direction < 0:
            self.shift = 8
            enemy.speed = 0
        elif enemy.rect.centerx > screen_width - width and enemy_direction > 0:
            self.shift = -8
            enemy.speed = 0
        elif self.level == level4:
            self.shift = 0
            enemy.speed = 8
        else:
            self.shift = 0
            enemy.speed = 8 
    
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
    
            
    
    def next_level(self):
        player = self.player.sprite
        
        # checking for collision to move the player to the next level
        for sprite in self.door.sprites():
            if player.rect.colliderect(sprite.rect) and self.level == level1:
                self.level = level2
                self.setup_level(self.level)
            elif player.rect.colliderect(sprite.rect) and self.level == level2:
                self.level = level3
                self.setup_level(self.level)
            elif player.rect.colliderect(sprite.rect) and self.level == level3:
                self.level = level1
                self.setup_level(self.level)
            
            
        # if the player dies on a level, they go back to the beginning of the level
        for sprite in self.door.sprites():
            if player.direction.y > 50 and self.level == level1:
                self.level = level1
                self.setup_level(self.level)
            elif player.direction.y > 50 and self.level == level2:
                self.level = level2
                self.setup_level(self.level)
            elif player.direction.y > 50 and self.level == level3:
                self.level = level3
                self.setup_level(self.level)
    
     
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

            if player.attacking == False:
                if key[pygame.K_k]:
                    self.player_attacking(self.display_surface, enemy.rect)
                if key[pygame.K_n]:
                    self.player_attacking(self.display_surface, enemy.rect)
            
            
        
        
    def player_attacking(self, surface, target):
        player = self.player.sprite
        enemy = self.enemy.sprite
        
        if player.attack_cooldown == 0:
            player.attacking = True
            attacking_rect = pygame.Rect(player.rect.centerx - (2 * player.rect.width * player.facing_left), player.rect.y, 2 * player.rect.width, player.rect.height)

            if attacking_rect.colliderect(target):
                print("Collision")
                enemy.health -= 10
        
            pygame.draw.rect(surface, (0, 255, 0), attacking_rect)
    
    def enemy_attacks(self):
            key = pygame.key.get_pressed()
            enemy = self.enemy.sprite
            player = self.player.sprite

            if enemy.attacking == False:
                if key[pygame.K_o]:
                    self.enemy_attacking(self.display_surface, player.rect)
                if key[pygame.K_p]:
                    self.enemy_attacking(self.display_surface, player.rect)
                if key[pygame.K_l]:
                    enemy.direction.y = 0
                    
                

   
    def enemy_attacking(self, surface, target):
        player = self.player.sprite
        enemy = self.enemy.sprite
        
        if enemy.attack_cooldown == 0:
            enemy.attacking = True
            attacking_rect = pygame.Rect(enemy.rect.centerx - (2 * enemy.rect.width * enemy.facing_left), enemy.rect.y, 2 * enemy.rect.width, enemy.rect.height)

            if attacking_rect.colliderect(target) and player.block == False:
                player.health -= 10
            
            if attacking_rect.colliderect(target) and player.block == True:
                player.health -= 5
        
            pygame.draw.rect(surface, (0, 255, 0), attacking_rect)
     

    
    def draw_health_bar(self, health, x, y):
        # designing the health bar
        ratio = health / 100
        pygame.draw.rect(self.display_surface, self.white, (x - 2 , y - 2, 404, 34))
        pygame.draw.rect(self.display_surface, self.red, (x, y, 400, 30))
        pygame.draw.rect(self.display_surface, self.yellow, (x, y, 400 * ratio, 30))
    
    def character_select(self, path):
        player1 = self.player.sprite

        player1.character_settings(path)
    

    # all previous functions are performed in this function
    def run(self, player):
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

        # Enemy attributes
        self.enemy.draw(self.display_surface)
        self.enemy.update()
        self.enemy_attacks()
        self.enemy_collision_x()
        self.enemy_collision_y()
        
        # Door attributes
        self.door.draw(self.display_surface)
        self.door.update(self.shift)

        self.next_level()

        #drawing health bars
        self.draw_health_bar(player.health, 20, 20)
        self.draw_health_bar(enemy.health, 750, 20)
    


     





        

    
        

    