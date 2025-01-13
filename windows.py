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

        enter_haus = tmx_data.get_object_by_name("enter_haus")
        self.enter_haus_rect = pygame.Rect(enter_haus.x , enter_haus.y , enter_haus.width, enter_haus.height)

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

    def switch_haus(self):
        # importer et charger la carte (carte_pygame)
        tmx_data = pytmx.util_pygame.load_pygame('interieur.tmx')
        map_data = pyscroll.TiledMapData(tmx_data)  # Permet de deplacer la carte dans la fenetre
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data,
                                                           self.screen.get_size())  # Renu graphique en fonction de la taille de
        map_layer.zoom = 1  # la fenetre avec get_size()


        # definir list de colision
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # dessiner groupe de calces
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=4)
        self.group.add(self.player)

        enter_haus = tmx_data.get_object_by_name("door_exit_haus")
        self.enter_haus_rect = pygame.Rect(enter_haus.x, enter_haus.y, enter_haus.width, enter_haus.height)
         #spawn point
        spawn_haus_point  = tmx_data.get_object_by_name("spawn_haus")
        self.player.position[0] = spawn_haus_point.x
        self.player.position[1] = spawn_haus_point.y

    def switch_world(self):
        # importer et charger la carte (carte_pygame)
        tmx_data = pytmx.util_pygame.load_pygame('carte_pygame.tmx')
        map_data = pyscroll.TiledMapData(tmx_data)  # Permet de deplacer la carte dans la fenetre
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data,
                                                           self.screen.get_size())  # Renu graphique en fonction de la taille de
        map_layer.zoom = 1.5  # la fenetre avec get_size()


        # definir list de colision
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # dessiner groupe de calces
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=4)
        self.group.add(self.player)

        enter_haus = tmx_data.get_object_by_name("enter_haus")
        self.enter_haus_rect = pygame.Rect(enter_haus.x, enter_haus.y, enter_haus.width, enter_haus.height)

         #spawn point
        spawn_haus_point  = tmx_data.get_object_by_name("haus_exit")
        self.player.position[0] = spawn_haus_point.x
        self.player.position[1] = spawn_haus_point.y + 20

    def update(self):
        self.group.update()
        #verifier entre
        if self.player.feet.colliderect(self.enter_haus_rect):
            self.switch_haus()
        # verifier sortie
        if self.player.feet.colliderect(self.enter_haus_rect):
            self.switch_world()

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




