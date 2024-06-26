import os
import pygame as py

BASE_IMG_PATH = 'data/images/'

# sets and loads in an image, and strips it of a background color(black)
def load_image(path):
    img = py.image.load(BASE_IMG_PATH + path).convert() # do this to images, it's good for performance
    img.set_colorkey((0, 0, 0))
    return img

def load_images(path):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name))
    return images