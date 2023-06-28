import pygame
from animation_folder import import_folder

class Particles(pygame.sprite.Sprite):
    def __init__(self, pos, type):
        super().__init__()
        # Particle attributes
        self.frames = 0
        self.animation_speed = 0.5
        # particles jumping or special effects
        if type == 'jump':
            self.animations = import_folder('./graphics/dust/dust_particles/jump')
        elif type == 'special':
            self.animations = import_folder('./graphics/dust/dust_particles/land')
        
        self.image = self.animations[int(self.frames)]
        self.rect = self.image.get_rect(center = pos)
    

    def animate(self):
        # changing between images
        self.frames += self.animation_speed
        
        # continuous loop of images
        if self.frames >= len(self.animations):
            self.frames = 0
            self.kill()
            
        
        self.image = self.animations[int(self.frames)]
        
    
    def update(self, shift):
        self.animate()
        self.rect.x += shift