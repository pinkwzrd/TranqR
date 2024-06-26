from .base_gui import *
from .constants import text_properties
from .constants import textbox_properties

# Textbox-Klasse
class TextBox(UIElement):
    '''
    This Class creates a Textbox.
    
    Attributes:
    screen (pygame.display.set_mode(size)): The windows the UI-Element gets displayed on.
    pos (tuple of 2 integers): UI-Element position (top left corner). Default: (0,0)
    size (tuple of 2 integers): Ui-Elements size. Default: (0,0)
    texture (pygame image): Textbox background image. Default: None
    can_edit (boolean): Whether a user should be able to edit the text content or not.
    text (str): text, Default: ""
    text_color (tuple of 3 Int): text color, Default: (0,0,0)
    max_length (Int): Maximum amount of characters. 
    spacing (Int): distance between text lines. Default: 5
    '''
    def __init__(self,screen,name="",pos=textbox_properties.DEFAULT_POS,size=textbox_properties.DEFAULT_SIZE,texture=None,text="",can_edit=False,text_color=text_properties.DEFAULT_COLOR,max_length=textbox_properties.DEFAULT_MAX_LENGTH,spacing=textbox_properties.SPACING): # init-Fkt
        '''
        Initializes an instance of TextBox
        '''
        super().__init__(screen,name,pos,size)
        
        self.texture = texture
        self.img = None
        
        self.font = pygame.font.SysFont(text_properties.FONT,text_properties.FONT_SIZE)
        self.text = text
        self.text_color = text_color
        
        self.can_edit = can_edit
        self.editable_mode = False
        self.max_length = max_length
        self.spacing = spacing
        
        self.box_visible = True
        self.text_box_visible = True
        
        self._time = 0
        self.fps = 60
    
    def __str__(self):
        return f"TextBox({self.name})"
    
    def handle_event(self,event): # Event-Handler -> Text schreiben
        if self.editable_mode:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.editable_mode:
                        logger_ui.info(f"Focus lost (ESC): {self.name}")
                    self.editable_mode = False
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                    logger_ui.debug(f"Keyboard input to {self.name}: BACKSPACE")
                    logger_ui.debug(f"New text: {self.text}")
                elif event.key == pygame.K_RETURN:
                    self.text += "\n"
                else:
                    if len(self.text) < self.max_length:
                        self.text += event.unicode
                        logger_ui.debug(f"Keyboard input to {self.name}: {event.unicode}")
                        logger_ui.debug(f"New text: {self.text}")
    
    def update(self):
        '''
        This function gets called by the EventListener to update an instance of this class frequently.
        '''
        self._moving()
        
        self._time += 1
        if self._time == self.fps:
            self._time = 0
        
        pos = pygame.mouse.get_pos()
        if self.can_edit:
            if self.target.mouse_left.state == "clicked":
                if self.collision(pos):
                    self.editable_mode = True
                    logger_ui.info(f"Focus gained (MOUSECLICK): {self.name}")
                else:
                    if self.editable_mode:
                        logger_ui.info(f"Focus lost (MOUSECLICK): {self.name}")
                    self.editable_mode = False
    
    def draw(self): # Fkt zur Bestimmung des Status und Darstellung
        '''
        This function gets called by the EventListener to draw the TextBox.
        '''
        if self.box_visible:
            if self.texture is None:
                self.draw_image(color=textbox_properties.COLOR)
            else:
                if self.img is None:
                    self.img = Image(self.screen,name=f"{self.name}",filename=self.texture,mode="resize",pos=self.pos,size=self.size)
                    self.img.draw()
                else:
                    self.img.pos = self.pos
                    self.img.size = self.size
                    self.img.draw()
        
        if self.text_box_visible:
            text = self.text
            
            if self.editable_mode:
                if self._time < (self.fps/2):
                    text += "_"
            self.display_text(text=text,font=self.font,text_color=self.text_color,spacing=self.spacing)
            
            logger_ui.debug(f"Image drawn.")