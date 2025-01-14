import os
import pygame as py

BASE_IMG_PATH = 'data/images/'

# sets and loads in an image, and strips it of a background color(black)
def load_image(path):
    """
    Loads an image from the specified path, converts it for improved performance, and sets its background color to transparent.

    Args:
        path (str): The file path to the image, relative to the base image path.

    Returns:
        pygame.Surface: The loaded and processed image.
    """
    img = py.image.load(BASE_IMG_PATH + path).convert() # do this to images, it's good for performance
    img.set_colorkey((0, 0, 0))
    return img

def load_images(path):
    """
    Loads all images in the specified directory and its subdirectories, and returns them as a list.

    The images are sorted alphabetically by their file names.

    Args:
        path (str): The path to the directory containing the images, relative to the base image path.

    Returns:
        list: A list of the loaded images.
    """
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        if os.path.isfile(BASE_IMG_PATH + '/' + path + '/' + img_name):
            images.append(load_image(path + '/' + img_name))
    return images

class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0

    def copy(self):
        '''
        Copies this Animation, returning a new Animation with the same properties as this one.
        '''
        return Animation(self.images, self.img_duration, self.loop)
    
    def update(self):
        """
        Updates the animation by incrementing the frame count and checking if the animation is finished.

        If the animation is set to loop, the frame count will wrap around to the beginning of the animation after it has finished.
        If the animation is not set to loop, the frame count will be capped at the last frame of the animation and the done flag will be set to True.
        """
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True
    
    def img(self):
        """
        Returns the current frame of the animation as a pygame.Surface.

        The frame is determined by dividing the current frame count by the image duration.

        Returns:
            pygame.Surface: The current image frame of the animation.
        """
        return self.images[int(self.frame / self.img_duration)]