import random

class Cloud:
    def __init__(self, pos, img, speed, depth):
        """
        Initializes a Cloud instance with the given parameters.

        Args:
            pos (tuple): The initial position of the cloud as a (x, y) tuple.
            img (pygame.Surface): The image of the cloud.
            speed (float): The speed of the cloud, in pixels per frame.
            depth (float): The depth of the cloud, used for sorting clouds for rendering.
        """
        
        self.pos = list(pos)
        self.img = img
        self.speed = speed
        self.depth = depth
    
    def update(self):
        """
        Updates the cloud's position by adding the speed to the x position
        """
        
        self.pos[0] += self.speed
        
    def render(self, surf, offset=(0, 0)):
        """
        Renders the cloud image onto the given surface at a position adjusted by the offset and depth.

        Args:
            surf (pygame.Surface): The surface to render the cloud image onto.
            offset (tuple): The offset applied to the cloud's position, affecting its depth, given as (x, y) coordinates.
        """
        render_pos = (self.pos[0] - offset[0] * self.depth, self.pos[1] - offset[1] * self.depth)
        surf.blit(self.img, (render_pos[0] % (surf.get_width() + self.img.get_width()) - self.img.get_width(), render_pos[1] % (surf.get_height() + self.img.get_height()) - self.img.get_height()))
        
class Clouds:
    def __init__(self, cloud_images, count=16):
        """
        Initializes the Clouds collection with a specified number of cloud instances.

        Args:
            cloud_images (list): A list of cloud images to randomly choose from for each cloud instance.
            count (int, optional): The number of cloud instances to create. Defaults to 16.

        Attributes:
            clouds (list): A list of Cloud objects, each initialized with random position, image,
                        speed, and depth, and sorted by their depth.
        """

        self.clouds = []
        
        for i in range(count):
            self.clouds.append(Cloud((random.random() * 99999, random.random() * 99999), random.choice(cloud_images), random.random() * 0.05 + 0.05, random.random() * 0.6 + 0.2))
        
        self.clouds.sort(key=lambda x: x.depth)
    
    def update(self):
        """
        Updates the position of each cloud in the collection.

        Iterates through all clouds and calls their update method,
        which adjusts their positions based on their speed.
        """

        for cloud in self.clouds:
            cloud.update()
    
    def render(self, surf, offset=(0, 0)):
        """
        Renders all the clouds in the collection onto the given surface at a position adjusted by the offset.

        Args:
            surf (pygame.Surface): The surface to render the clouds onto.
            offset (tuple): The offset applied to the cloud's position, affecting its depth, given as (x, y) coordinates.
        """
        for cloud in self.clouds:
            cloud.render(surf, offset=offset)