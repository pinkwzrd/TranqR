import os
def file_exists(file):
    if os.path.exists(file):
        return True
    else:
        return False