import pygame
import sys
from scripts.utilities import load_image, load_images, Animation
from scripts.entities import Player, Enemi
from scripts.tilemap import TileMap

class Game:

    def __init__(self, display, map="map_tuto"):
        
        self.display = display
        self.map = map

        self.background = pygame.image.load("plateformer\\ressources\\background\\background.png").convert() #Background image

        #The assets dictionnary
        self.assets = {
            "player": load_image("plateformer\\ressources\\entities\\player\\player_idle.png"),
            "enemi": load_image("plateformer\\ressources\\entities\\enemi\\idle\\enemi_idle.png"),

            "grass" : load_images("plateformer\\ressources\\tiles\\grass"),
            "dirt" : load_images("plateformer\\ressources\\tiles\\dirt"),

            "map_tuto": load_image("plateformer\\ressources\\maps\\tutoriel\\tutoriel_bits.png"),

            "player/idle": Animation(load_images("plateformer\\ressources\\entities\\player\\idle"), image_duration=60),
            "player/run": Animation(load_images("plateformer\\ressources\\entities\\player\\run"), image_duration=4),
            "player/jump": Animation(load_images("plateformer\\ressources\\entities\\player\\jump")),
            "enemi/idle": Animation(load_images("plateformer\\ressources\\entities\\enemi\\idle"), image_duration=6),
            "enemi/run": Animation(load_images("plateformer\\ressources\\entities\\enemi\\run"), image_duration=4)
        }
        self.color_code = {
            "grass": (0,255,0),
            "dirt": (180,90,0),

            "player": (0,0,255),
            "enemi": (255,0,0)
        }

        #make the player spawn where we put the blue square on the map
        for y in range(self.assets[self.map].get_height()):
            for x in range(self.assets[self.map].get_width()):
                if self.assets[self.map].get_at((x,y)) == self.color_code["player"]:
                    self.player = Player(self, (x*32,y*32), (x*32, y*32)) #Player creation
        self.mouvement = [0,0] #Player mouvement for the right and left
        self.dead = False
        
        self.enemi = []

        #check if there is enemi on the map
        for y in range(self.assets[self.map].get_height()):
            for x in range(self.assets[self.map].get_width()):
                if self.assets[self.map].get_at((x,y)) == self.color_code["enemi"]:
                    self.enemi.append(Enemi(self, (x*32, y*32)))

        self.map2D = TileMap(self, (32,32)) #Map creation
        self.map2D.mapping() #Call the mapping function

        self.scroll = [(self.player.rect().centerx - self.display.get_width() / 2), (self.player.rect().centery - self.display.get_height() / 2)] #Make the camera mouving

    def run(self):

        #background
        self.display.blit(self.background, (0,0))

        #variables for the mouving camera
        self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
        self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30

        render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

        #Tiles
        self.map2D.render(self.display, offset=render_scroll)

        #Render the enemis
        for enemi in self.enemi.copy():
            #if the enemi touche the player, we restart the level
            if enemi.rect().colliderect(self.player.rect()):
                self.dead = True
            enemi.update(self.map2D)
            enemi.render(self.display, offset=render_scroll)

        if not self.dead: #render the player if he's not dead
            #Check if the player is mouving, falling, or if there's a collision
            self.player.update(self.map2D, (self.mouvement[1] - self.mouvement[0], 0))
            self.player.render(self.display, offset=render_scroll) #Render the player
        else: #else, we restart the level
            self.restart()

        #Events loop
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.quit()
            
            if event.type == pygame.KEYDOWN:
                    
                if event.key == pygame.K_RIGHT:
                    self.mouvement[1] = 2.1
                if event.key == pygame.K_LEFT:
                    self.mouvement[0] = 2.1
                if event.key == pygame.K_UP:
                    self.player.jump()
                       
            if event.type == pygame. KEYUP:
                    
                if event.key == pygame.K_RIGHT:
                    self.mouvement[1] = 0
                if event.key == pygame.K_LEFT:
                    self.mouvement[0] = 0
    
    def quit(self):
        pygame.quit()
        sys.exit()
    
    def restart(self):
        Game.__init__(self, self.display, self.map)