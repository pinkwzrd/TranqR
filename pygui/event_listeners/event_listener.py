from .mouse_button import *

logger_event_listener = logging.getLogger("listener")
logger_event_listener.setLevel(logging.INFO)

# Event-Listener-Klasse
class EventListener:
    '''
    This Class triggers different functions of Observers.
    '''
    def __init__(self,name="Standard"):
        '''
        Initializes an Instance of EventListener.
        '''
        self.name = name
        
        self.mouse_left = MouseButton(name="left_click",type=1)
        self.mouse_middle = MouseButton(name="middle_click",type=2)
        self.mouse_right = MouseButton(name="right_click",type=3)
        
        self.observers = []
        self.essential_observers = [self.mouse_left,self.mouse_middle,self.mouse_right]
        
        logger_event_listener.info(f"Instance initiated: {self}")
    
    def __str__(self):
        return f"EventListener({self.name})"
    
    def subscribe(self,observer): # Neue Observer (Beobachter) aufnehmen
        '''
        Registers new Observer.
        
        Parameters:
        observer (list of classes or class): Class that subscribes to the EventListener's functions.
        '''
        if isinstance(observer, list):  # Prüfen, ob mehrere Observer in Liste übergeben wurden
            for object in observer:
                self.observers.append(object) # Observer der Liste hinzufügen
                object.target = self
                
                logger_event_listener.info(f"A new instance subscribed to {self.name}: {object}")
        else:
            self.observers.append(observer) # Observer der Liste hinzufügen
            observer.target = self
            
            logger_event_listener.info(f"A new instance subscribed to {self.name}: {observer}")
    
    def unsubscribe(self,observer):
        '''
        
        '''
        if isinstance(observer, list):  # Prüfen, ob mehrere Observer in Liste übergeben wurden
            for object in observer:
                if object in self.observers:
                    self.observer.remove(object)
                    logger_event_listener.info(f"{object} unsubscribed to {self}.")
                else:
                    logger_event_listener.warning(f"{object} tried to unsubscribed to {self}. It was not found in the subscriber list.")
        else:
            if object in self.observers:
                self.observer.remove(observer)
                
                logger_event_listener.info(f"{observer} unsubscribed to {self}.")
            else:
                logger_event_listener.warning(f"{observer} tried to unsubscribed to {self}. It was not found in the subscriber list.")
    
    def notify(self, event): # Observer über das Event informieren
        '''
        Triggers the Observers event-handling functions.
        
        Parameters:
        event (): Event that gets transferred to the Observers
        '''
        for observer in self.essential_observers:
            try:
                observer.handle_event(event) # Eventhandler-Funktion der essenziellen Observer auslösen
                logger_event_listener.debug(f"{self} notified the essential observer {observer}")
            except Exception as e:
                logger_event_listener.error(f"Triggering handle_event() of an essential observer ({observer}) failed: {e}")
        for observer in self.observers:
            try:
                observer.handle_event(event) # Eventhandler-Funktion der Observer auslösen
                logger_event_listener.debug(f"{self} notified the  observer {observer}")
            except Exception as e:
                logger_event_listener.warning(f"Triggering handle_event() of an observer ({observer}) failed: {e}")
    def tick(self):
        '''
        Triggers the Observers update functions.
        '''
        self.mouse_pos = pygame.mouse.get_pos()
        for observer in self.observers:
            try:
                observer.update() # Update-Funktion der Observer auslösen
            except Exception as e:
                logger_event_listener.warning(f"Triggering update() of the observer {observer} failed: {e}")
        for observer in self.essential_observers:
            try:
                observer.reset()
            except Exception as e:
                logger_event_listener.error(f"Triggering reset() of the essential observer ({observer}) failed: {e}")
        logger_event_listener.debug(f"\nTick is over.\n")
    def drawall(self):
        '''
        Triggers the Observers draw functions.
        '''
        for observer in self.observers:
            try:
                observer.draw() # Draw-Funktion der Observer auslösen
            except Exception as e:
                logger_event_listener.warning(f"Triggering draw() of the observer ({observer}) failed: {e}")