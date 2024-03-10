import pygame
import random

class PhysicsEntity:

    def __init__(self, game, entity_type, position, size):
        self.game = game
        self.type = entity_type
        self.position = list(position)
        self.size = list(size)
        self.velocity = [0,0]
        self.collisions = {"up": False, "down": False, "right": False, "left": False}

        self.action = ""
        self.anim_offset = (0, 0)#padding on the x side of the image
        self.flip = False
        self.set_action("idle")
    
    def rect(self):
        return pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])
    
    def set_action(self, action):
        
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + "/" + self.action].copy()

    def update(self, tilemap, mouvement=(0,0)):
        
        self.collisions = {"up": False, "down": False, "right": False, "left": False}

        frame_mouvement = (mouvement[0] + self.velocity[0], mouvement[1] + self.velocity[1]) #Player mouvements

        self.position[0] += frame_mouvement[0]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.position):
            if entity_rect.colliderect(rect): #Check if there's a collision on the right or left
                if frame_mouvement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions["right"] = True
                if frame_mouvement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions["left"] = True
                self.position[0] = entity_rect.x
        
        self.position[1] += frame_mouvement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.position):
            if entity_rect.colliderect(rect): #Check if there's a collision on top or the bottom
                if frame_mouvement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions["down"] = True
                if frame_mouvement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions["up"] = True
                self.position[1] = entity_rect.y
        
        if mouvement[0] > 0:
            self.flip = False
        if mouvement[0] < 0:
            self.flip = True

        #gravity
        self.velocity[1] = round(min(9.8, self.velocity[1] + 0.2),1)

        #stop the jump or the fall of the player if ther's collision
        if self.collisions["down"] or self.collisions["up"]:
            self.velocity[1] = 0
        
        self.animation.update()
        
    def render(self, surface, offset=[0,0]):
        surface.blit(pygame.transform.flip(self.animation.image(), self.flip, False), (self.position[0] - offset[0] + self.anim_offset[0], self.position[1] - offset[1] + self.anim_offset[1]))

class Player(PhysicsEntity):
    
    def __init__(self, game, position, spawner):

        self.size = (16,16)
        self.jumps = 1
        self.air_time = 0
        self.coyote_time_value = 0.6 #0.6, no coyote time, 1.6, a little
        self.spawner = spawner

        super().__init__(game, "player", position, self.size)

    def jump(self): #jump function
        if self.jumps:
            self.velocity[1] = -5.5
            self.jumps -= 1
            self.air_time = 5
    
    def update(self, tilemap, mouvement=(0,0)):

        super().update(tilemap, mouvement)

        #set the player action in order to his mouvement
        self.air_time += 1
        if self.collisions["down"]:
            self.air_time = 0
        if self.air_time > 4:
            self.set_action("jump")
        elif mouvement[0] != 0:
            self.set_action("run")
        else:
            self.set_action("idle")

        #check if the player is touching the ground, if it's true, then he can jump
        if self.collisions["down"]:
            self.jumps = 1
        
        #check if the fall speed player is superior to 0.6, it means that he's falling
        if self.velocity[1] > self.coyote_time_value:
            self.jumps = 0
        
        #check if the player is falling, but out the screen
        if self.game.scroll[1] - self.game.player.position[1] < -550:
            self.game.dead = True

    def render(self, surface, offset=[0,0]):
        super().render(surface, offset)

class Enemi(PhysicsEntity):

    def __init__(self, game, position):

        self.size = (16,16)
        self.walking = 0

        super().__init__(game, "enemi", position, self.size)
    
    def update(self, tilemap, mouvement=(0,0)):

        if self.walking:
            #check if the tile in front of and below the ennemi is physic or not
            if tilemap.solide_check((self.rect().centerx + (-self.size[0]//2 if self.flip else self.size[0]//2), self.position[1] + self.size[1])):
                if self.flip:
                    mouvement = (mouvement[0] -0.5, mouvement[1])
                else:
                    mouvement = (mouvement[0] +0.5, mouvement[1])
            else:
                self.flip = not self.flip

            self.walking = max(0, self.walking - 1)

        elif random.random() < 0.015:
            self.walking = random.randint(64, 128)

        super().update(tilemap, mouvement)

        if mouvement[0] != 0:
            self.set_action("run")
        else:
            self.set_action("idle")
    
    def render(self, surface, offset=[0,0]):
        super().render(surface, offset)