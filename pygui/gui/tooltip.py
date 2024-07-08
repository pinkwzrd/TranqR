import time

from .base_gui import *
from .textbox import *

class TooltipTextBox(TextBox):
    def __init__(self,screen):
        super().__init__(screen)
    
    def draw(self): # Fkt zur Bestimmung des Status und Darstellung
        '''
        
        '''
        if self.box_visible:
            if self.texture is None:
                self.draw_image(color=(255,255,255),color_frame=(0,0,0))
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

class TooltipManager:
    def __init__(self,screen,trigger_time=0.5):
        self.screen = screen
        
        self.text = None # Text, der im Tooltip angezeigt wird
        
        self.spacing = 3
        
        self.trigger_time = trigger_time # Zeit, die der Mauszeiger stehen bleiben soll bis der Tooltip erscheint
        
        self.start_pos = (0,0)
        self.start_time = 0
        
        self.tooltip_list = []
        
        self.tooltip_box = TooltipTextBox(self.screen)
        self.tooltip_box.box_visible = False
        self.tooltip_box.text_box_visible = False
        #self.tooltip_box.font = pygame.font.SysFont("Arial",15)
    
    def update(self): # update-Funktion, kann vom EventListener aufgerufen werden
        if pygame.mouse.get_focused():
            now_pos = pygame.mouse.get_pos()
            now_time = time.time()
            if now_pos == self.start_pos:
                if now_time-self.start_time >= self.trigger_time and not(self.text):
                    for element in self.tooltip_list:
                        if (now_pos[0] >= element.pos[0] and now_pos[0] <= (element.pos[0]+element.size[0])) and (now_pos[1] >= element.pos[1] and now_pos[1] <= (element.pos[1]+element.size[1])):
                            self.text = element.text
                    
                            self.tooltip_box.text = self.text
                            self.tooltip_box.box_visible = True
                            self.tooltip_box.text_box_visible = True
                            
                            self.tooltip_box.spcing = self.spacing
                            
                            font = self.tooltip_box.font
                            size = font.size(self.text)
                            self.tooltip_box.size = (size[0]+self.spacing,size[1]+self.spacing)
                            
                            self.tooltip_box.pos = (now_pos[0],now_pos[1]-self.tooltip_box.size[1])
            else:
                self.start_pos = now_pos
                self.start_time = now_time
                self.text = None
                self.tooltip_box.box_visible = False
                self.tooltip_box.text_box_visible = False
    
    def add_tooltip(self,tooltip):
        if isinstance(tooltip,list):
            for object in tooltip:
                self.tooltip_list.append(object)
        else:
            self.tooltip_list.append(tooltip)
    
    def handle_event(self,event):
        pass
    
    def draw(self):
        pass

class TooltipArray:
    def __init__(self,pos=(0,0),size=(0,0),text="TOOLTIP :3"):
        self.pos = pos
        self.size = size
        
        self.text = text # Text, der im Tooltip angezeigt wird