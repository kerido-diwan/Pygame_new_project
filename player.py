import pygame

from constants import PLAYER_SKIN_DIMENSIONS


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sprite_sheet = pygame.image.load("Player.png")
        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.images = {
            "down": self.get_image(0, 0),
            "left": self.get_image(0, 32),
            "right": self.get_image(0, 64),
            "up": self.get_image(0, 96)
        }
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5 , 12)
        self.old_position = self.position.copy()
        self.speed = 0.50 #vitesse du mouvement

    def save_location(self):
        self.old_position = self.position.copy()

    def change_animation(self, name):
        self.image = self.images[name]
        self.image.set_colorkey(0, 0)

    #def pour les mouvements
    def mouv_rigth(self): self.position[0] += self.speed

    def mouv_left(self): self.position[0] -= self.speed

    def mouv_up(self): self.position[1] -= self.speed

    def mouv_down(self): self.position[1] += self.speed

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def mouv_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom


    def get_image(self, x, y):
        image = pygame.Surface(PLAYER_SKIN_DIMENSIONS)
        image.blit(self.sprite_sheet, (0, 0), (x, y, PLAYER_SKIN_DIMENSIONS[0], PLAYER_SKIN_DIMENSIONS[1]))
        return image
