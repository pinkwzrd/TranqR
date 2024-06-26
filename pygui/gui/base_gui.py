import logging
import math

import pygame

from .image import Image
from .functions import *

logger_ui = logging.getLogger("gui")
logger_ui.setLevel(logging.INFO)

# UI-Element-Klasse
class UIElement:
    '''
    This Class is the parent class of all UI-Element-Classes.
    It contains the general functions of every UI-Element.
    
    Attributes:
    screen (pygame.display.set_mode(size)): The windows the UI-Element gets displayed on.
    pos (tuple of 2 integers): UI-Element position (top left corner). Default: (0,0)
    size (tuple of 2 integers): Ui-Elements size. Default: (0,0)
    texture (pygame.image.load('image.png')): The UI-Elements Image. Default: None
    '''
    def __init__(self,screen,name="",pos=(0,0),size=(0,0)): # Parameter aller UI-Elemente
        '''
        Initializes an Instance of UIElement.
        '''
        self.name = name
        
        self.screen = screen
        self.pos = pos
        self.size = size
        
        self._moving_pos = self.pos
        self._moveto = None
        self.speed = 0
        
        self.target = None
        
        logger_ui.info(f"Instance initiated: {self}")
    
    def __str__(self):
        return f"UIElement-Instance({self.name})"
    
    def collision(self,object_pos): # Fkt zur Erkennung, ob Koordinaten in Feld liegen
        '''
        This function checks whether a given coordinate is within the image area of the UI-Element
        
        Parameters:
        object_pos (tuple of 2 Integers): The x and y coordinates you want to check.
        
        Returns:
        Boolean: If it is in the image area: True, if not: False
        '''
        try:
            button_x,button_y = self.pos
            button_xmax, button_ymax = self.size
            object_x,object_y = object_pos
            if (object_x >= button_x and object_x <= button_x+button_xmax) and (object_y >= button_y and object_y <= button_y+button_ymax): # Erkennen, ob die Koordinaten des Objekts im Feld des UI-Elements liegen
                return True
            else:
                return False
        except Exception as e:
            logger_ui.error(f"The collision could not be calculated.")
            return False
    
    def draw_image(self,texture=None,color=(100,100,100),color_frame=(20,20,20),pos=None,size=None): # Fkt zum Zeichnen des UI-Elements
        '''
        This function draws the image of the UI-Element.
        Depending on whether you have entered an image or not, the provided image will be generated or a rectangle with a frame.
        
        Parameters:
        texture (pygame.image.load('image.png')): The UI-Elements Image. Default: None
        color (tuple of 3 Integers): Color (in RGB format) of the rectangle that will be generated instead of the image. Default: (100,100,100)
        pos (tuple of 2 integers): UI-Element position (top left corner). Default: self.pos (own position)
        size (tuple of 2 integers): Ui-Elements size. Default: self.size (own size)
        '''
        if pos == None:
            pos = self.pos
        if size == None:
            size = self.size
        if texture == None: # Falls keine Textur eingegeben wurde, wird ein Standard verwendet
            pygame.draw.rect(self.screen, color_frame, (pos[0], pos[1], size[0], size[1])) # Rahmen
            pygame.draw.rect(self.screen, color, (pos[0]+1, pos[1]+1, size[0]-2, size[1]-2))
        else:
            try:
                self.screen.blit(texture,pos,(0,0,size[0],size[1]))
                logger_ui.debug(f"Image displayed.")
            except Exception as e:
                logger_ui.error(f"Image could not be displayed.")
    
    def display_text(self,text="",font=None,text_color=(0,0,0),spacing=0): # Fkt, die Textblöcke aufbereitet und darstellt
        '''
        This function displays a given text as lines.
        
        Parameters:
        text (str): Your text. Default: ""
        font (pygame.font.SysFont(FONT,FONT_SIZE)): Pygame font. Default: pygame.font.SysFont("Arial",20)
        text_color (tuple of 3 Integers): text color (in RGB format). Default: (0,0,0)
        spacing (int): Distance between lines and between text and frame. Default: 0
        '''
        if font == None: # Falls keine Font angegeben wurde, wird eine Standard-Font verwendet
            font = pygame.font.SysFont("Arial",20)
        lines = split_text(font,text,self.size[0]-self.spacing*2) # Text in einzelne Zeilen aufteilen
        
        try:
            for i in range(len(lines)): # Zeilen reihenweise darstellen
                text = font.render(lines[i],True,text_color)
                self.screen.blit(text,(self.pos[0]+spacing,self.pos[1]+spacing+(font.size("")[1])*i))
            logger_ui.debug(f"Text displayed.")
        except Exception as e:
            logger_ui.error(f"An error occured while trying to display text: {e}")
    
    def moveto(self,pos=(0,0),speed=1):
        '''
        This function lets the UI-Element move to a certain position.
        
        Parameters:
        pos (tuple of 2 Integers): The final position. Default: (0,0)
        speed (float): The movement speed in pixels/tick. Default: 1
        '''
        if isinstance(pos,tuple) and len(pos) == 2 and isinstance(pos[0],int) and isinstance(pos[1],int): # Prüfen, ob pos Tupel aus 2 Integern ist.
            self._moveto = pos
            if isinstance(speed,int) or isinstance(speed,float):
                self.speed = speed
            else:
                logger_ui.warning(f"Setting speed failed. Make sure 'speed' is a float.")
                self.speed = 1
            logger_ui.debug(f"New final position assigned to {self.name} (pos={pos}, speed={speed})")
        else:
            logger_ui.error(f"Setting movement position to {self.name} failed. Be sure it is pos=(int,int).")
    
    def _moving(self):
        '''
        This function is for internal use. Please use the EventListener class to update UI-Elements.
        This function calculates the movement of the UI-Elements.
        '''
        try:
            if self.speed > 0 and self._moveto is not None: # Es muss ein Ziel gesetzt sein und eine Geschwindigkeit über 0 vorhanden sein
                dist_x = self._moveto[0] - self._moving_pos[0]
                dist_y = self._moveto[1] - self._moving_pos[1]
                distance = math.sqrt(dist_x ** 2 + dist_y ** 2) # Distanz berechnen
                if distance > self.speed: # Falls die Distanz zu klein ist, werden die Zielkoordinaten direkt übernommen.
                    ratio = self.speed / distance # Vektorberechnung
                    move_x = dist_x * ratio
                    move_y = dist_y * ratio
                    self._moving_pos = (self._moving_pos[0] + move_x, self._moving_pos[1] + move_y) # Neue theoretische Position wird ermittelt
                else:
                    self._moving_pos = self._moveto
                    self._moveto = None
                self.pos = (int(self._moving_pos[0]),int(self._moving_pos[1])) # Aus der theoretischen Position wird die tatsächliche Position berechnet
            else:
                self._moving_pos = self.pos # Falls die Bedingungen nicht erfüllt werden, passt sich die theoretische Position der tatsächlichen an.
            
            logger_ui.debug(f"Object moved. (Theoretical position: {self._moving_pos})")
        except Exception as e:
            logger_ui.error(f"An error occured while moving: {e}")
    
    def update(self):
        '''
        This function gets called by the EventListener to update the UI-Element.
        By default this calls the _moving() function.
        '''
        self._moving()
        logger_ui.debug(f"Instance updated.")
    
    def handle_event(self,event):
        '''
        This function gets called by the EventListener to handle certain events.
        By default this calls no function.
        
        Parameters:
        event (): The event.
        '''
        pass
    
    def draw(self):
        '''
        This function gets called by the EventListener to draw the UI-Element.
        By default this calls no function.
        '''
        pass