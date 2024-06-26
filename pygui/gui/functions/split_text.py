# Fkt um Text in einzelne Zeilen zu teilen
def split_lines(font,text,width):
    '''
    Diese Funktion teilt einen Text in einzelne Zeilen in Abhängikeit von einer Breite.
    
    Parameters:
    font (pygame.font.SysFont(FONT,FONT_SIZE)): Pygame font.
    text (str): Text, der geteilt werden soll.
    width (int): Maximale Breite der Zeilen in Pixeln.
    
    Returns:
    list: Liste der einzelnen Zeilen.
    '''
    try:
        words = str(text).split(" ")
        lines = []
        line = ""
        for word in words:
            if font.size(f"{line}{word}")[0] < width:
                if font.size(f"{line}{word} ")[0] < width:
                    line = f"{line}{word} "

                else:
                    line = f"{line}{word}"
                    lines += [line]
                    line = ""
            else:
                lines += [line]
                line = f"{word} "
        if line != "":
            lines += [line]
        return lines
    except Exception as e:
        logging.warning(f"An error occured: {e}")
        return text

def split_text(font,text,width):
    lines = str(text).replace("\\n","\n").split("\n")
    lines_split = []
    for line in lines:
        single_lines = split_lines(font,line,width)
        for single_line in single_lines:
            lines_split.append(single_line)
    return lines_split