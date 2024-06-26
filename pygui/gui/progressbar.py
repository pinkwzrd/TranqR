from .base_gui import *
from .constants import progressbar_properties

# ProgressBar-Klasse
class ProgressBar(UIElement):
    '''
    This Class creates a Progressbar.
    
    Attributes:
    screen (pygame.display.set_mode(size)): The windows the UI-Element gets displayed on.
    pos (tuple of 2 integers): UI-Element position (top left corner). Default: (0,0)
    size (tuple of 2 integers): Ui-Elements size. Default: (20,20)
    texture (tuple of 2 pygame images): Frame and bar image. Default: (None,None)
    progress (Int): Progressbar progress. Default: 0
    max (Int): Maximum progress. Default: 100
    spacing (Int): distance between frame thickness.
    '''
    def __init__(self,screen,name="",pos=progressbar_properties.DEFAULT_POS,size=progressbar_properties.DEFAULT_SIZE,texture_frame=None,texture_bar=None,progress=progressbar_properties.PROGRESS,max=progressbar_properties.DEFAULT_MAX,spacing=progressbar_properties.SPACING):
        '''
        Initializes an Instance of ProgressBar.
        '''
        super().__init__(screen,name,pos,size)
        
        self.texture_frame = texture_frame
        self.texture_bar = texture_bar
        self.img_frame = None
        self.img_bar = None
        
        self.progress = progress
        self.max = max
        
        self.spacing = spacing
    
    def __str__(self):
        return f"ProgressBar({self.name})"
    
    def draw(self): # Fortschrittsanzeige darstellen
        '''
        This function gets called by the EventListener to draw the ProgressBar.
        '''
        
        if self.texture_frame is None:
            self.draw_image(color=progressbar_properties.FRAME_COLOR)
        else:
            if self.img_frame is None:
                self.img_frame = Image(self.screen,name=f"{self.name}-Frame",filename=self.texture_frame,mode="resize",pos=self.pos,size=self.size)
                self.img_frame.draw()
            else:
                self.img_frame.pos = self.pos
                self.img_frame.size = self.size
                self.img_frame.draw()
        
        bar_width = int((self.size[0] - self.spacing*2) * self.progress / self.max) # Balkenbreite ermitteln
        bar_height = int(self.size[1] - self.spacing*2) # Balkenhöhe ermitteln
        bar_x = self.pos[0] + self.spacing # Balken Position berechnen
        bar_y = self.pos[1] + self.spacing
        
        if self.texture_bar is None:
            self.draw_image(color=progressbar_properties.BAR_COLOR,pos=(bar_x,bar_y),size=(bar_width,bar_height))
        else:
            if self.img_bar is None:
                self.img_bar = Image(self.screen,name=f"{self.name}",filename=self.texture_bar,mode="crop",pos=(bar_x,bar_y),size=(bar_width,bar_height))
                self.img_bar.draw()
            else:
                self.img_bar.pos=(bar_x,bar_y)
                self.img_bar.size=(bar_width,bar_height)
                self.img_bar.draw()
        
        
        logger_ui.debug(f"Image drawn.")