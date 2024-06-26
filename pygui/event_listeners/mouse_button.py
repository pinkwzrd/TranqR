import logging
import pygame
from pygame.locals import *

logger_mouse = logging.getLogger("mb")
logger_mouse.setLevel(logging.INFO)

# Maus-Button-Klasse
class MouseButton:
    def __init__(self,name="",type=1):
        self.name = name
        
        self.type = type
        
        self._down = False
        self._up = False
        
        self.state = "released"
        
        logger_mouse.info(f"Instance initiated: {self}")
    
    def __str__(self):
        return f"MouseButton({self.name})"
        
    def handle_event(self,event):
        try:
            if event.type == MOUSEBUTTONDOWN or event.type == MOUSEBUTTONUP:
                #print(event.button,self.type)
                if event.button == self.type:
                    if event.type == pygame.MOUSEBUTTONUP: # Mausbutton losgelassen
                        self._down = False
                        self._up = True
                    
                    if event.type == pygame.MOUSEBUTTONDOWN: # Mausbutton gedrückt
                        self._down = True
                        self._up = False
                    
                    self.get_state()
        except Exception as e:
            logger_mouse.error(f"{self} could not handle events properly ({e})")
    
    def get_state(self):
        if self._down:
            self.state = "pressed"
        elif self._up:
            self.state = "clicked"
        else:
            self.state = "released"
        logger_mouse.debug(f"Mouse button[{self.type}] set to {self.state}")
    
    def reset(self):
        self_down = False
        self._up = False
        self.get_state()
        logger_mouse.debug(f"Instance reset.")