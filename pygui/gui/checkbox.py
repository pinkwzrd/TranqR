from .base_gui import *
from .constants import text_properties
from .constants import checkbox_properties

# Checkbox-Klasse
class Checkbox(UIElement):
    '''
    This Class creates a Checkbox that you can click on/off.
    
    Attributes:
    screen (pygame.display.set_mode(size)): The windows the UI-Element gets displayed on.
    pos (tuple of 2 integers): UI-Element position (top left corner). Default: (0,0)
    size (tuple of 2 integers): Ui-Elements size. Default: (20,20)
    locked (boolean): Whether the check-option should be locked or not.
    text (str): text, Default: ""
    text_color (tuple of 3 Int): text color, Default: (0,0,0)
    spacing (Int): distance between text lines. Default: 5
    '''
    def __init__(self, screen, name="", pos=checkbox_properties.DEFAULT_POS, size=checkbox_properties.DEFAULT_SIZE, locked = False, text="", checked=False, text_color=text_properties.DEFAULT_COLOR, spacing=checkbox_properties.DEFAULT_SPACING,func_on=None,parameters_on=None,func_off=None,parameters_off=None,texture_checked=None,texture_unchecked=None,texture_checked_locked=None,texture_unchecked_locked=None):
        '''
        Initializes an Instance of Checkbox.
        '''
        super().__init__(screen, name, pos, size)
        
        self.locked = locked
        
        self.font = pygame.font.SysFont(text_properties.FONT,text_properties.FONT_SIZE)
        self.text = text
        self.text_color = text_color
        
        self.spacing = spacing
        
        self.checked = checked
        
        self.func_on = func_on
        self.parameters_on = parameters_on
        self.func_off = func_off
        self.parameters_off = parameters_off
        
        self.texture_checked = texture_checked
        self.texture_unchecked = texture_unchecked
        self.texture_checked_locked = texture_checked_locked
        self.texture_unchecked_locked = texture_unchecked_locked
        
        self.img_checked = None
        self.img_unchecked = None
        self.img_checked_locked = None
        self.img_unchecked_locked = None
    
    def __str__(self):
        return f"Checkbox({self.name})"
    
    def lock(self):
        self.locked = True
    
    def unlock(self):
        self.locked = False
    
    def check(self):
        self.checked = True
        if self.func_on:
            if self.parameters_on:
                self.func_on(self.parameters_on)
            else:
                self.func_on()
    
    def uncheck(self):
        self.checked = False
        if self.func_off:
            if self.parameters_off:
                self.func_off(self.parameters_off)
            else:
                self.func_off()

    def handle_event(self, event):
        '''
        This function gets called by the EventListener to handle click on/off.
        
        Parameters:
        event (): The event.
        '''
        if self.target.mouse_left.state == "clicked":
            if self.collision(pygame.mouse.get_pos()):
                if self.locked:
                    logger_ui.info(f"User tried checking a locked {self}.")
                else:
                    if self.checked:
                        self.uncheck()
                    else:
                        self.check()
                    
                    logger_ui.info(f"{self} set to {self.checked}")

    def draw(self):
        '''
        This function gets called by the EventListener to draw the Checkbox.
        '''
        if self.locked:
            if self.checked:
                if self.texture_checked_locked: # checked AND locked AND image
                    if self.img_checked_locked: # update and print the image
                        self.img_checked_locked.pos = self.pos
                        self.img_checked_locked.size = self.size
                        self.img_checked_locked.draw()
                    else: # initiate the image
                        self.img_checked_locked = Image(self.screen,name=f"{self.name}-Frame",filename=self.texture_checked_locked,mode="resize",pos=self.pos,size=self.size)
                        self.img_checked_locked.draw()
                else: # checked AND locked AND (NOT image)
                    self.draw_image(color=checkbox_properties.LOCKED_INNER,color_frame=checkbox_properties.LOCKED_OUTER)
                    pygame.draw.line(self.screen, checkbox_properties.DEFAULT_LINE, (self.pos[0]+4, self.pos[1]+4), (self.pos[0]+self.size[0]-4, self.pos[1]+self.size[1]-4), 2)
                    pygame.draw.line(self.screen, checkbox_properties.DEFAULT_LINE, (self.pos[0]+4, self.pos[1]+self.size[1]-4), (self.pos[0]+self.size[0]-4, self.pos[1]+4), 2)
            
            else:
                if self.texture_unchecked_locked: # (NOT checked) AND locked AND image
                    if self.img_unchecked_locked: # update and print the image
                        self.img_unchecked_locked.pos = self.pos
                        self.img_unchecked_locked.size = self.size
                        self.img_unchecked_locked.draw()
                    else: # initiate the image
                        self.img_unchecked_locked = Image(self.screen,name=f"{self.name}-Frame",filename=self.texture_unchecked_locked,mode="resize",pos=self.pos,size=self.size)
                        self.img_unchecked_locked.draw()
                else: # (NOT checked) AND locked AND (NOT image)
                    self.draw_image(color=checkbox_properties.LOCKED_INNER,color_frame=checkbox_properties.LOCKED_OUTER)
        
        else:
            if self.checked:
                if self.texture_checked: # checked AND (NOT locked) AND image
                    if self.img_checked: # update and print the image
                        self.img_checked.pos = self.pos
                        self.img_checked.size = self.size
                        self.img_checked.draw()
                    else: # initiate the image
                        self.img_checked = Image(self.screen,name=f"{self.name}-Frame",filename=self.texture_checked,mode="resize",pos=self.pos,size=self.size)
                        self.img_checked.draw()
                else: # checked AND (NOT locked) AND (NOT image)
                    self.draw_image(color=checkbox_properties.DEFAULT_INNER,color_frame=checkbox_properties.DEFAULT_OUTER)
                    pygame.draw.line(self.screen, checkbox_properties.DEFAULT_LINE, (self.pos[0]+4, self.pos[1]+4), (self.pos[0]+self.size[0]-4, self.pos[1]+self.size[1]-4), 2)
                    pygame.draw.line(self.screen, checkbox_properties.DEFAULT_LINE, (self.pos[0]+4, self.pos[1]+self.size[1]-4), (self.pos[0]+self.size[0]-4, self.pos[1]+4), 2)
            
            else:
                if self.texture_unchecked: # (NOT checked) AND (NOT locked) AND image
                    if self.img_unchecked: # update and print the image
                        self.img_unchecked.pos = self.pos
                        self.img_unchecked.size = self.size
                        self.img_unchecked.draw()
                    else: # initiate the image
                        self.img_unchecked = Image(self.screen,name=f"{self.name}-Frame",filename=self.texture_unchecked,mode="resize",pos=self.pos,size=self.size)
                        self.img_unchecked.draw()
                else: # (NOT checked) AND (NOT locked) AND (NOT image)
                    self.draw_image(color=checkbox_properties.DEFAULT_INNER,color_frame=checkbox_properties.DEFAULT_OUTER)
                    
        '''
        # Draw checkbox square
        if self.locked:
            pygame.draw.rect(self.screen, checkbox_properties.LOCKED_OUTER, (self.pos[0], self.pos[1], self.size[0], self.size[1]))
            pygame.draw.rect(self.screen, checkbox_properties.LOCKED_INNER, (self.pos[0]+2, self.pos[1]+2, self.size[0]-4, self.size[1]-4))
        else:
            pygame.draw.rect(self.screen, checkbox_properties.DEFAULT_OUTER, (self.pos[0], self.pos[1], self.size[0], self.size[1]))
            pygame.draw.rect(self.screen, checkbox_properties.DEFAULT_INNER, (self.pos[0]+2, self.pos[1]+2, self.size[0]-4, self.size[1]-4))

        # Draw checkmark if checked
        if self.checked:
            pygame.draw.line(self.screen, checkbox_properties.DEFAULT_LINE, (self.pos[0]+4, self.pos[1]+4), (self.pos[0]+self.size[0]-4, self.pos[1]+self.size[1]-4), 2)
            pygame.draw.line(self.screen, checkbox_properties.DEFAULT_LINE, (self.pos[0]+4, self.pos[1]+self.size[1]-4), (self.pos[0]+self.size[0]-4, self.pos[1]+4), 2)
        '''

        # Draw text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=(self.pos[0] + self.size[0] + self.spacing + text_surface.get_width() // 2, self.pos[1] + self.size[1] // 2))
        self.screen.blit(text_surface, text_rect)
        
        logger_ui.debug(f"Image drawn.")