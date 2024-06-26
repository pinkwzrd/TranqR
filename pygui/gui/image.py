from .base_gui import *
from .functions import *
from .constants import image_properties

logger_image = logging.getLogger("image")
logger_image.setLevel(logging.INFO)

class Image():
    '''
    This Class creates an Image.
    '''
    def __init__(self,screen,name="",pos=image_properties.DEFAULT_POS,size=image_properties.DEFAULT_SIZE,filename=None,mode=image_properties.DEFAULT_MODE): # init-Fkt
        #super().__init__(screen,name,pos,size)
        self.screen = screen
        self.name = name
        self.pos = pos
        self.size = size
        
        self.filename = filename
        self.original_size = None
        self.image = None
        
        self.mode = mode
    
    def __str__(self):
        return f"Image({self.name})"
    
    def load_image(self):
        if file_exists(self.filename):
            try:
                self.image = pygame.image.load(self.filename)
                self.original_size = self.image.get_size()
                logger_image.info(f"Loading image succeeded: {self}")
            except Exception as e:
                logger_image.warning(f"Loading image failed: {self} ({e})")
        else:
            logger_image.warning(f"File could not be found: {self.filename}")
    
    def draw(self):
        if self.image is None:
            self.load_image()
        
        img = None
        
        if self.size:
            try:
                if self.mode == "resize":
                    img = pygame.transform.scale(self.image, self.size)
                    x,y = self.size
                elif self.mode == "crop":
                    img = self.image
                    x,y = self.size
                elif self.mode == "original":
                    img = self.image
                    x,y = self.original_size
                
                self.screen.blit(img,self.pos,(0,0,x,y))
                logger_image.debug(f"Image displayed: {self}")
            except Exception as e:
                logger_image.error(f"Image could not get displayed: {self} ({e})")
    
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
            logger_image.error(f"The collision could not be calculated.")
            return False
    
    def update(self):
        pass
    def handle_event(self,event):
        pass