import pygame
shift = 0

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([size, size])
        self.image.fill("black")
        self.rect = self.image.get_rect(topleft= pos)
        self.shift = 0
        self.direction = pygame.math.Vector2(0, 0)
        
    
    def update(self, shift):
        self.rect.x += shift
 
    




    
