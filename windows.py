import pygame
import pytmx
import pyscroll

from constants import DIMENSIONS, TITRE
from player import Player


class Windows:
    def __init__(self):
        #creer la fenetre
        self.screen = pygame.display.set_mode(DIMENSIONS)
        pygame.display.set_caption(TITRE)
        #importer et charger la carte (carte_pygame)
        tmx_data = pytmx.util_pygame.load_pygame('carte_pygame.tmx')
        map_data = pyscroll.TiledMapData(tmx_data) #Permet de deplacer la carte dans la fenetre
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size()) # Renu graphique en fonction de la taille de
        map_layer.zoom = 1.5                                                                              #la fenetre avec get_size()
        # generer player
        player_position = tmx_data.get_object_by_name("spawn_player")
        self.player = Player(player_position.x, player_position.y)

        #definir list de colision
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x , obj.y, obj.width, obj.height))
        #dessiner groupe de calces
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=4)
        self.group.add(self.player)

    def handel_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            self.player.mouv_up()
            self.player.change_animation("up")

        if pressed[pygame.K_DOWN]:
            self.player.mouv_down()
            self.player.change_animation("down")

        if pressed[pygame.K_LEFT]:
            self.player.mouv_left()
            self.player.change_animation("left")

        if pressed[pygame.K_RIGHT]:
            self.player.mouv_rigth()
            self.player.change_animation('right')


    def update(self):
        self.group.update()
        #verifier collision
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.mouv_back()


    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            self.player.save_location()
            self.handel_input()
            self.update()
            self.group.center(self.player.rect)
            self.group.draw(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        clock.tick(60)
        pygame.quit()




