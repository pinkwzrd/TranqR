# Standard libraries
import math
import logging
import os

# External libraries
import pygame
from pygame.locals import *

# Internal libraries
from .event_listeners import *
from .gui import *
from .complex_gui import *

# set logging file
# DEBUG, INFO, WARNING, ERROR, CRITICAL (lowest to highest level)
logging.basicConfig(filename='LOG.log', level=logging.INFO, filemode="w")

print("Welcome to pygui! Use gui_help() to get help setting up your code for this library.")

def gui_help():
    pass
    #print("If you need further help, please contact the author via discord: pinkwizard")

def main():
    
    # Init
    
    # Window
    window_main = (500,300)
    screen = pygame.display.set_mode(window_main)
    pygame.font.init()
    pygame.display.set_caption("UI-Elemente in Pygame")
    
    # Window Refresh Settings
    running = True
    clock = pygame.time.Clock()
    pygame.key.set_repeat(200,0) # mindestens 100 empfohlen
    
    # Colors
    black = (0,0,0)
    white = (255,255,255)
    
    screen.fill(white)
    
    
    released = "../images/tb1.png"
    highlighted = "../images/../images/tb2.png"
    pressed = "../images/../images/../images/tb4.png"
    m = Button(screen,name="Test-Button",texture_released=None,texture_highlighted=None,texture_pressed=None)
    m.pos = (0,100)
    m.size = (100,100)
    m.text = "Button mit Text"
    m.text_color = (100,100,100)
    
    t = TextBox(screen,name="Textbox-editierbar",can_edit=True,texture="../images/tb1.png")
    t.pos = 100,50
    t.size = 200,200
    t.text = "Editierbare Textbox"
    
    d = TextBox(screen,name="Textbox-nicht editierbar",texture="../images/tb2.png")
    d.pos = 300,50
    d.size = 200,200
    d.text = "Nicht editierbare Textbox"
    
    
    #balken_image = pygame.image.load('balken.png')
    #rahmen_image = pygame.image.load('rahmen.png')
    rahmen_image = "../images/../images/../images/tb4.png"
    balken_image = "../images/../images/tb3.png"
    b = ProgressBar(screen,name="Test-Progressbar",texture_frame=None,texture_bar=None,max=200,progress=150)
    b.pos = 10,10
    b.size = 150,20
    
    c = Checkbox(screen,name="Test-Checkbox",text="Wow!", size=(100,100))
    
    i = Image(screen,name="Test-Bild",filename="../images/test2.png",mode="resize",pos=(0,200),size=(0,0))
    i.size = (80,100)
    
    ui_manager = EventListener()
    ui_manager.subscribe([m,t,d,b,c,i])
    
    lmb_pressed = False
    # Program Loop
    while running:
        # INPUT
        for event in pygame.event.get():
            if event.type == pygame.MOUSEWHEEL:
                #print(event.x, event.y)
                if event.y != 0:
                    dir = int((event.y/abs(event.y)))
                    t.moveto(pos=(t.pos[0],t.pos[1]+20*dir),speed=abs(event.y))
                    
            if event.type == pygame.QUIT:
                running = False
            ui_manager.notify(event)

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:
                    pass
                if event.key == pygame.K_1:
                    t.moveto(pos=(300,200),speed=1)
                    d.moveto(pos=(0,10),speed=1.2)
                    b.moveto(pos=(400,210),speed=0.8)
                    m.moveto(pos=(150,100),speed=0.9)
                if event.key == pygame.K_2:
                    t.moveto(pos=(100,50),speed=3)
                    d.moveto(pos=(300,50),speed=2)
                    b.moveto(pos=(10,10),speed=1.8)
                    m.moveto(pos=(0,50),speed=1.5)
                if event.key == pygame.K_UP:
                    b.progress += 10
                if event.key == pygame.K_DOWN:
                    b.progress -= 10
                
            
            if event.type == pygame.MOUSEBUTTONUP:
                lmb_pressed = False
                lmb_released = True
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                lmb_pressed = True
        
        
        # VISUAL
        screen.fill(white)
        ui_manager.tick()
        ui_manager.drawall()
        
        # RESET
        lmb_released = False
        
        # Refresh Window
        pygame.display.flip()
        clock.tick(60)
        
    pygame.quit()

if __name__ == "__main__":
    main()