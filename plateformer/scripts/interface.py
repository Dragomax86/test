import pygame

class Button:

    def __init__(self, position, size):
        
        self.position = position
        self.size = size
        self.trigger = False
        self.surf = self.surface()
        self.color = (255,255,255)
    
    def rect(self):
        return pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])

    def surface(self):
        return pygame.Surface((self.size[0], self.size[1]))
    
    def update(self):

        pygame.draw.rect(self.surf, self.color, (0, 0, self.size[0], self.size[1]))
        
        if pygame.mouse.get_pos()[0] > self.position[0]*2 and pygame.mouse.get_pos()[0] < (self.position[0] + self.size[0])*2 and pygame.mouse.get_pos()[1] > self.position[1]*2 and pygame.mouse.get_pos()[1] < (self.position[1] + self.size[1])*2:
            self.color = (255,0,0)
        else:
            self.color = (255,255,255)

    def render(self, surface):
        surface.blit(self.surf, self.position)