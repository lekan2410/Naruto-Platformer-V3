import pygame
from animation_folder import import_folder

class Door(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        # Door attributes
        self.frames = 0
        self.animation_speed = 0.15
        self.animations = import_folder('./graphics/pain_character/door')
        self.image = self.animations[int(self.frames)]
        self.rect = self.image.get_rect(topleft = pos)
    
    def animation(self):
        
        # changing between images
        self.frames += self.animation_speed
        
        # continuous loop of images 
        if self.frames >= len(self.animations):
            self.frames = 0
         
        self.image = self.animations[int(self.frames)]

    
    def update(self, shift):
        self.animation()
        self.rect.x += shift
        
    
