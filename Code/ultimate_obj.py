import pygame
from animation_folder import import_folder

class Ultimate_Obj(pygame.sprite.Sprite):
    def __init__(self, pos, path):
        super().__init__()
        # Ultimate attributes
        self.frames = 0
        self.animation_speed = 0.20
        self.animations = import_folder(path + '/ultimate_obj')
        self.image = self.animations[int(self.frames)]
        self.rect = self.image.get_rect(center = pos)
    
    def animation(self):
        
        # changing between imagess
        self.frames += self.animation_speed
        
        # continuous loop of images 
        if self.frames >= len(self.animations):
            self.frames = 0
            self.kill()
         
        self.image = self.animations[int(self.frames)]

    
    def update(self, pos):
        self.animation()
        self.rect.x += pos
        
    
