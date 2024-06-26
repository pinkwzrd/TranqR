from .base_gui import *
from .constants import text_properties
from .constants import button_properties

# Button-Klasse
class Button(UIElement):
    '''
    This Class creates a Button.
    
    Attributes:
    screen (pygame.display.set_mode(size)): The windows the UI-Element gets displayed on.
    pos (tuple of 2 integers): UI-Element position (top left corner). Default: (0,0)
    size (tuple of 2 integers): Ui-Elements size. Default: (0,0)
    texture (tuple of 3 pygame image): Button background image: (released, clicked, pressed). Default: None
    text (str): text, Default: ""
    text_color (tuple of 3 Int): text color, Default: (0,0,0)
    spacing (Int): distance between text lines. Default: 5
    '''
    def __init__(self,screen,name="",pos=button_properties.DEFAULT_POS,size=button_properties.DEFAULT_SIZE,texture_released=None,texture_highlighted=None,texture_pressed=None,text="",text_color=text_properties.DEFAULT_COLOR,spacing=button_properties.DEFAULT_SPACING,func_pressed=None,parameters_pressed=None,func_clicked=None,parameters_clicked=None): # init-Fkt
        super().__init__(screen,name,pos,size)
        
        self.texture_released = texture_released
        self.texture_highlighted = texture_highlighted
        self.texture_pressed = texture_pressed
        
        self.img_released = None
        self.img_highlighted = None
        self.img_pressed = None

        self.status = "released"
        
        self.font = pygame.font.SysFont(text_properties.FONT,text_properties.FONT_SIZE)
        self.text = text
        self.text_color = text_color
        
        self.spacing = spacing
        
        self.func_pressed = func_pressed
        self.parameters_pressed = parameters_pressed
        self.func_clicked = func_clicked
        self.parameters_clicked = parameters_clicked
    
    def __str__(self):
        return f"Button({self.name})"
    
    
    def update(self):
        '''
        This function gets called by the EventListener to update an instance of this class frequently.
        '''
        self._moving()
        
        pos = pygame.mouse.get_pos()
        if pygame.mouse.get_focused():
            if self.collision(pos):
                if self.target.mouse_left.state == "released":
                    self.status = "highlighted"
                    logger_ui.debug(f"{self.name} {self.status}")
                else:
                    self.status = self.target.mouse_left.state
                    if self.status == "clicked":
                        logger_ui.info(f"{self.name} clicked.")
                    else:
                        logger_ui.debug(f"{self.name} {self.status}")
            
            else:
                self.status = "released"
        else:
            self.status = "released"
        if self.status == "pressed" and self.func_pressed:
            if self.parameters_pressed:
                self.func_pressed(self.parameters_pressed)
            else:
                self.func_pressed()
        if self.status == "clicked" and self.func_clicked:
            if self.parameters_clicked:
                self.func_clicked(self.parameters_clicked)
            else:
                self.func_clicked()
        self._mouse_up = False
    
    def draw(self): # Fkt zur Bestimmung des Status und Darstellung
        '''
        This function gets called by the EventListener to draw the Button.
        '''
        if self.status == "pressed":
            if self.texture_pressed is None:
                self.draw_image(color=button_properties.DEFAULT_PRESSED_COLOR)
            else:
                if self.img_pressed is None:
                    self.img_pressed = Image(self.screen,name=f"{self.name}",filename=self.texture_pressed,mode="resize",pos=self.pos,size=self.size)
                    self.img_pressed.draw()
                else:
                    self.img_pressed.pos = self.pos
                    self.img_pressed.size = self.size
                    self.img_pressed.draw()
        elif self.status == "clicked" or self.status == "highlighted":
            if self.texture_highlighted is None:
                self.draw_image(color=button_properties.DEFAULT_HIGHLIGHT_COLOR)
            else:
                if self.img_highlighted is None:
                    self.img_highlighted = Image(self.screen,name=f"{self.name}",filename=self.texture_highlighted,mode="resize",pos=self.pos,size=self.size)
                    self.img_highlighted.draw()
                else:
                    self.img_highlighted.pos = self.pos
                    self.img_highlighted.size = self.size
                    self.img_highlighted.draw()
        elif self.status == "released":
            if self.texture_released is None:
                self.draw_image(color=button_properties.DEFAULT_RELEASED_COLOR)
            else:
                if self.img_released is None:
                    self.img_released = Image(self.screen,name=f"{self.name}",filename=self.texture_released,mode="resize",pos=self.pos,size=self.size)
                    self.img_released.draw()
                else:
                    self.img_released.pos = self.pos
                    self.img_released.size = self.size
                    self.img_released.draw()
        
        self.display_text(text=self.text,font=self.font,text_color=self.text_color,spacing=self.spacing)
        
        logger_ui.debug(f"Image drawn.")


class InvisibleButton(Button):
    '''
    This Class creates an invisible Button.
    
    Attributes:
    screen (pygame.display.set_mode(size)): The windows the UI-Element gets displayed on.
    pos (tuple of 2 integers): UI-Element position (top left corner). Default: (0,0)
    size (tuple of 2 integers): Ui-Elements size. Default: (0,0)
    '''
    def __init__(self,screen,name="",pos=button_properties.DEFAULT_POS,size=button_properties.DEFAULT_SIZE):
        '''
        This function creates an instance of InvisibleButton.
        '''
        super().__init__(screen,name,pos,size)
    
    def __str__(self):
        return f"InvisibleButton({self.name})"
    
    def draw(self):
        pass