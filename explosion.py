from pygame.sprite import Sprite
import pygame

class Explosion(Sprite):
    """ A class to manage the explosion animation."""
    def __init__(self, screen, center, explosion_type="alien"):
        """Initialize animation elements"""
        super().__init__()
        self.screen = screen
        self.explosion_type = explosion_type
        self.images = [] # List to hold the explosion images
        self.set_frame_details() # Set the number of frames and base path based on the type
        self.load_images() # Load the images
        self.index = 0 # Current image index
        self.image = self.images[self.index] # current image
        self.rect = self.image.get_rect(center=center) # Position the explosion
        self.frame_rate = 4 # How many game loops each frame should show for
        self.frame_counter = 0 # Counts the game loops to track when to switch frames

    def set_frame_details(self):
        """Allows for different explosion animations based on object type."""
        if self.explosion_type == "alien":
            self.explosion_frames = 12
            self.base_path = 'images/explosion1/'
        elif self.explosion_type == "player":
            self.explosion_frames = 16
            self.base_path = 'images/explosion2_0/'
        elif self.explosion_type == "power_shot":
            self.explosion_frames = 15
            self.base_path = 'images/PowerShotExplosionFrames/'
        # NOTE: Add more conditions here for other types of explosion if needed

    def load_images(self):
        """Load the images from a sprite sheet or individual images."""
        # Load each frame of the explosion from separate files or a spritesheet
        for i in range(self.explosion_frames):
            # Constructing file name: tile000.png, tile001.png, ... , tile011.png
            file_name = f'{self.base_path}tile00{i}.png' if i < 10 else f'{self.base_path}tile0{i}.png'
            img = pygame.image.load(file_name).convert_alpha()
            img = pygame.transform.scale(img, (230, 230)) # Scale if necessary
            self.images.append(img)

    def update(self):
        """Update the explosion animation."""
        self.frame_counter += 1
        if self.frame_counter >= self.frame_rate:
            self.frame_counter = 0 # Reset the frame counter
            self.index += 1 # Move to the next frame
            if self.index == len(self.images):
                self.kill() # End the animation and remove the sprite
            else:
                self.image = self.images[self.index] # Set the next image