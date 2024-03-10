import pygame
import sys
from ctypes import windll
from scripts.Game import Game
from scripts.interface import Button

class Menu:

    def __init__(self):
        
        self.screen_size = windll.user32 #get the screen size

        self.screen_size_x = self.screen_size.GetSystemMetrics(78) #get the screen size x
        self.screen_size_y = self.screen_size.GetSystemMetrics(79) #get the screen size y

        pygame.display.set_caption("Plateformer") #Name of the window
        self.screen = pygame.display.set_mode((self.screen_size_x, self.screen_size_y)) #Create the main window
        self.display = pygame.Surface((self.screen_size_x//2, self.screen_size_y//2)) #Create the sub window
        self.display.fill((200,200,200))

        self.clock = pygame.time.Clock() #Call the clock function

        self.game = Game(self.display)

        self.buttons = []
        self.buttons.append(Button((100,100),(100,100)))
    
    def run(self):

        while True:
            
            self.game.run()

            """for button in self.buttons:
                button.update()
                button.render(self.display)"""

            #Events loop
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    self.game.quit()

            self.screen.blit(pygame.transform.scale(self.display, (self.screen_size_x, self.screen_size_y)), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

if __name__ == "__main__":
    Menu().run()