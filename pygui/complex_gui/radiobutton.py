from .setup import *

class RadioButton:
    def __init__(self,name=""):
        
        self.name = name
        
        self.members = []
        
        self.value = None
    
    def __str__(self):
        return f"RadioButton({self.name})"
    
    def add_member(self,applicants,content=None):
        '''Adds a CheckBox instance to the RadioButton list.'''
        if isinstance(applicants, list):  # Prüfen, ob mehrere Applikanten in Liste übergeben wurden
            for applicant in applicants:
                self.members.append((applicant,content)) # Applikant der Liste hinzufügen
                
                logger_complex.info(f"A new instance added to {self.name}: {applicant}")
        else:
            self.members.append((applicants,content)) # Applikant der Liste hinzufügen
            
            logger_complex.info(f"A new instance added to {self.name}: {applicants}")
    
    def select(self,target):
        '''Selects the checked member of the RadioButton list.'''
        for member in self.members:
            if member[0].checked:
                member[0].unlock()
            member[0].checked = False
            if target in member:
                member[0].checked = True
                member[0].lock()
                self.value = member[1]
        logger_complex.info(f"New target selected in {self}: {target.name}")
        logger_complex.info(f"New value in {self}: {self.value}")