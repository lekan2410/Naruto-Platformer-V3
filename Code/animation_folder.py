import os 
import pygame

def import_folder(path):
    surface = []
    # getting the images
    for _,__,images in os.walk(path):
        for img in images:
            #getting the full path of the image location
            full_path = path + "/" + img
            image = pygame.image.load(full_path).convert_alpha()
            # adding the image onto the surface
            surface.append(image)
        return surface

