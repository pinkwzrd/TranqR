# Start: 2024/04
# Latest Update: 2024/06/26
# by pinki<3

import threading
from tkinter import filedialog
import logging
import time

import pygame
from moviepy.editor import VideoFileClip, AudioFileClip
import torch.cuda
from faster_whisper import WhisperModel
import pyperclip

import pygui as ui

import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "True" # Keep to prevent intel crash issue

def take_screenshot(screen,size):
    # Capture the screen into a pygame surface
    screenshot_surface = pygame.Surface(size)
    screenshot_surface.blit(screen, (0, 0))
    # Convert the surface to a bytes object
    screenshot_bytes = pygame.image.tostring(screenshot_surface, 'RGBA')
    # Create a pygame image from the bytes
    screenshot_img = pygame.image.fromstring(screenshot_bytes, size, 'RGBA')
    # Display the screenshot image on the screen
    screen.blit(screenshot_img, (0, 0))
    pygame.display.flip()
    pygame.time.Clock().tick(1)

def thread_save_func(parameters):
    thread = threading.Thread(target=save_func,args=(parameters,))
    thread.daemon = True
    thread.start()

def save_func(parameters):
    timestamps = parameters.timestamps
    text_output = parameters.text_output_raw
    
    if isinstance(text_output, list):
        init_file = f"{file_from_path(parameters.source_file).split('.')[0]}(Transcript)"
        path = filedialog.asksaveasfilename(initialfile=init_file,defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if path:
            text = ""
            if timestamps:
                for line in text_output:
                    text += f"[{print_time(line[0])} - {print_time(line[1])}] {line[2]}\n"
                print("Saved with timestamps")
            
            else:
                for line in text_output:
                    text += f"{line[2]}\n"
                print("Saved without timestamps")
            
            with open(path,"w") as file:
                file.write(text)

def copy_func(parameters): # whisper_handler
    timestamps = parameters.timestamps
    text_output = parameters.text_output_raw
    
    if isinstance(text_output, list):
        text = ""
        if timestamps:
            for line in text_output:
                text += f"[{print_time(line[0])} - {print_time(line[1])}] {line[2]}\n"
            print("Copied with timestamps")
        
        else:
            for line in text_output:
                text += f"{line[2]}\n"
            print("Copied without timestamps")
        pyperclip.copy(text)
    

def start_whisper(parameters):
    if not(parameters.running):
        parameters.running = True
        parameters.progress_bar.progress = 0
        parameters.progress = None
        parameters.language = None
        parameters.language_percentage = 1
        #parameters.textbox.moveto(pos=(510,0),speed=5)
        thread = threading.Thread(target=thread_whisper,args=(parameters,))
        thread.daemon = True
        thread.start()

def thread_whisper(parameters):
    if not(parameters.source_file):
        thread = threading.Thread(target=load_file,args=(parameters,))
        thread.daemon = True
        thread.start()
        thread.join()
    else:
        parameters.get_duration()
        parameters.pass_info()
    try:
        parameters.run_whisper()
    except Exception as e:
        logging.critical(f"Whisper cannot run: {e}")
        parameters.textbox.text = ("Failed! Please contact support.")

def thread_load_file(parameters):
    thread = threading.Thread(target=load_file,args=(parameters,))
    thread.daemon = True
    thread.start()

def load_file(parameters):
    path = filedialog.askopenfilename()
    if path:
        parameters.source(path)
        parameters.text = file_from_path(path)
        parameters.get_duration()
        parameters.pass_info()

def file_from_path(path):
    file = path.split("/")[-1]
    return file

def time_format(num):
    num = str(num)
    if len(num) < 2:
        num = f"0{num}"
    return num

def print_time(sec):
    if isinstance(sec,int) or isinstance(sec,float):
        sec = int(sec)
        min = int(sec/60)
        sec = sec%60
        
        time = f"{time_format(min)}:{time_format(sec)}"
        return time
    else:
        return None


class WhisperHandler:
    def __init__(self):
        self.running = False
        
        # Constants
        self.default_font = None
        
        # Input
        self.source_file = None
        self.model = None
        self.model_size = None
        self.timestamps = None
        
        # Output
        self.language = None
        self.language_percentage = 1
        self.text_output = None
        self.text_output_raw = "Please run Whisper before attempting to copy the output."
        
        self.source_textbox_link = None
        
        self.duration = None
        self.progress = None
        self.progress_bar = None
        
        # EventHandler
        self.textbox = None # textbox_output
        self.infobox = None
        
        self.start_button = None
    
    def timestamps_on(self):
        self.timestamps = True
        if isinstance(self.text_output_raw, list):
            self.text_output = ""
            for l in self.text_output_raw:
                self.text_output += f"[{print_time(l[0])} - {print_time(l[1])}] {l[2]}\n"
            self.pass_output()
    
    def timestamps_off(self):
        self.timestamps = False
        if isinstance(self.text_output_raw, list):
            self.text_output = ""
            for l in self.text_output_raw:
                self.text_output += f"{l[2]}\n"
            self.pass_output()
    
    def check_source_length(self,text):
        text_width = self.default_font.size(text)[0]
        max_width = self.source_textbox_link.size[0] - self.source_textbox_link.spacing * 2 - 130
        
        if True: # "Dateianfa..."
            if text_width > max_width:
                while text_width > max_width:
                    text = text[:-1]
                    text_width = self.default_font.size(f"{text}...")[0]
                text = f"{text}..."
            return text
        
        elif True: # "...teiende.Endung"
            if text_width > max_width:
                while text_width > max_width:
                    text = text[1:]
                    text_width = self.default_font.size(f"...{text}")[0]
                text = f"...{text}"
            return text
        
        elif True: # "Dateianfa...Endung"
            if text_width > max_width:
                text_spl = text.split(".")
                print(text_spl)
                while text_width > max_width:
                    text_spl[0] = text_spl[0][:-1]
                    text_width = self.default_font.size(f"{text_spl[0]}...{text_spl[1]}")[0]
                print(text,text_spl)
                text = f"{text_spl[0]}...{text_spl[1]}"
            return text
    
    def source(self,path):
        self.source_file = path
        if self.source_textbox_link:
            file = file_from_path(path)
            self.source_textbox_link.text = self.check_source_length(file)
        
    
    def pass_output(self):
        self.textbox.text = self.text_output
    
    def pass_info(self):
        text = ""
        if self.language and self.language_percentage:
            text += f"( {self.language.upper()}: {int(self.language_percentage*100)}% )  -  "
        if self.progress or self.duration:
            if self.progress == self.duration:
                text = "( Finished )"
            else:
                text += "( "
                if self.progress:
                    text += f"{print_time(self.progress)} / "
                if self.duration:
                    text += f"{print_time(self.duration)}"
                text += " )"
        self.infobox.text = text
    
    def set_model(self,model=None,model_size=None):
        if model:
            self.model = model
        if model_size:
            self.model_size = model_size
    
    def get_duration(self):
        try:
            file = VideoFileClip(self.source_file)
        except:
            file = AudioFileClip(self.source_file)
        
        self.duration = file.duration
        self.progress_bar.max = int(self.duration)
        file.close()
        
    
    def run_whisper(self):
        self.textbox.pos = (510,0)
        self.running = True
        self.textbox.text = "Loading..."
        self.start_button.text = "Running..."
        self.text_output_raw = []
        print(f"Running Whisper-Model({self.model.value[0]}-{self.model.value[1]}, {self.model_size.value})")
        
        model = WhisperModel(self.model_size.value, device=self.model.value[0], compute_type=self.model.value[1])
        self.textbox.text = ("Detecting language...")
        segments, info = model.transcribe(self.source_file, beam_size=5)
        
        print("Detected language '%s' with probability %f" % (info.language, info.language_probability))
        self.language = info.language
        self.language_percentage = info.language_probability
        self.pass_info()
        self.textbox.text = ("Transcribing audio...")
        
        self.text_output = ""
        for segment in segments:
            line = (segment.start, segment.end, segment.text)
            self.text_output_raw += [line]
            self.text_output = ""
            if self.timestamps:
                for l in self.text_output_raw:
                    self.text_output += f"[{print_time(l[0])} - {print_time(l[1])}] {l[2]}\n"
            else:
                for l in self.text_output_raw:
                    self.text_output += f"{l[2]}\n"
            
            self.progress = segment.end
            if self.progress > self.duration:
                self.progress = self.duration
            self.progress_bar.progress = int(self.progress)
            self.pass_info()
            self.pass_output()
        self.progress = self.duration
        self.progress_bar.progress = int(self.progress)
        self.pass_info()
        self.running = False
        self.start_button.text = "Start Transcription"

def main():
    
    cuda_available = torch.cuda.is_available()
    
    # Init
    pygame.init()
    
    icon = pygame.image.load("images/icon.png")
    #pygame.mouse.set_visible(False)
    
    
    
    # Window
    window_size = (1000,450)
    screen = pygame.display.set_mode(window_size)
    pygame.font.init()
    pygame.display.set_caption("TranqR")
    pygame.display.set_icon(icon)
    
    # Window Refresh Settings
    running = True
    clock = pygame.time.Clock()
    pygame.key.set_repeat(100,0) # mindestens 100 empfohlen
    
    # Colors
    black = (0,0,0)
    white = (255,255,255)
    
    screen.fill(white)
    
    # Key instances
    
    whisper_handler = WhisperHandler()
    tooltip_manager = ui.TooltipManager(screen,trigger_time=0.6)
    
    # Constants
    
    fps = 60
    settings_spacing = 10
    
    default_font = pygame.font.SysFont("Arial",20)
    whisper_handler.default_font = default_font
    
    # GUI instances
    
    textbox_output_overlay = ui.Image(screen,name="Text-Output-Overlay",filename="images/overlay-500x450.png",mode="resize")
    textbox_output_overlay.pos = (window_size[0]-500,0)
    textbox_output_overlay.size = (500,window_size[1])
    
    textbox_output = ui.TextBox(screen,name="Text-Output",can_edit=False,spacing=16)
    textbox_output.size = (textbox_output_overlay.size[0]-settings_spacing*2,0)
    textbox_output.pos = (textbox_output_overlay.pos[0]+settings_spacing,0)
    textbox_output.text = "Welcome to Whisper, a speech-to-text AI made by OpenAI.\nSelect a video or audio file and click the start button to run Whisper."
    textbox_output.font = pygame.font.SysFont("Helvetica",18)
    whisper_handler.textbox = textbox_output
    
    info_box_height = 14
    
    whisper_progress = ui.ProgressBar(screen,name="Wisper-Progress",texture_frame="images/frame_progressbar_whisper.png",texture_bar="images/bar_progressbar_whisper.png",spacing=4)
    whisper_progress.size = (int(textbox_output_overlay.size[0]*0.8),16)
    whisper_progress.pos = (textbox_output_overlay.pos[0]+(textbox_output_overlay.size[0]-whisper_progress.size[0])/2,window_size[1]-whisper_progress.size[1]-info_box_height-settings_spacing)
    whisper_handler.progress_bar = whisper_progress
    
    info_box = ui.TextBox(screen,name="Info Box",texture=None,can_edit=False,spacing=0)
    info_box.size = whisper_progress.size[0],info_box_height
    info_box.pos = (whisper_progress.pos[0],textbox_output_overlay.pos[1]+textbox_output_overlay.size[1]-info_box.size[1]-settings_spacing)
    info_box.text = "(lang/lang_prob) - (progress/max)"
    info_box.font = pygame.font.SysFont("Helvetica",12)
    info_box.box_visible = False
    whisper_handler.infobox = info_box
    
    
    # Settings
    
    settings_pos = (settings_spacing,settings_spacing+100)
    settings_size = 480,170
    
    settings_overlay = ui.Image(screen,name="Settings-Overlay",filename="images/overlay-480x170.png",mode="resize")
    settings_overlay.pos = settings_pos
    settings_overlay.size = settings_size
    
    
    whisper_handler.model = ui.RadioButton(name="Model")
    
    gpu_fp16 = ui.Checkbox(screen,name="Model GPU FP16",text="GPU FP16")
    gpu_fp16.texture_unchecked = "images/checkbox_unchecked.png"
    gpu_fp16.texture_checked = "images/checkbox_checked.png"
    gpu_fp16.texture_unchecked_locked = "images/checkbox_unchecked_locked.png"
    gpu_fp16.size = (30,30)
    gpu_fp16.pos = (settings_pos[0]+5,settings_pos[1]+5)
    gpu_fp16.func_on = whisper_handler.model.select
    gpu_fp16.parameters_on = gpu_fp16
    whisper_handler.model.add_member(gpu_fp16,("cuda","float16"))
    
    gpu_int8 = ui.Checkbox(screen,name="Model GPU INT8",text="GPU INT8")
    gpu_int8.texture_unchecked = "images/checkbox_unchecked.png"
    gpu_int8.texture_checked = "images/checkbox_checked.png"
    gpu_int8.texture_unchecked_locked = "images/checkbox_unchecked_locked.png"
    gpu_int8.size = (30,30)
    gpu_int8.pos = (settings_pos[0]+5,settings_pos[1]+5+40)
    gpu_int8.func_on = whisper_handler.model.select
    gpu_int8.parameters_on = gpu_int8
    whisper_handler.model.add_member(gpu_int8,("cuda","float16_int8"))
    
    cpu_int8 = ui.Checkbox(screen,name="Model CPU INT8",text="CPU INT8")
    cpu_int8.texture_unchecked = "images/checkbox_unchecked.png"
    cpu_int8.texture_checked = "images/checkbox_checked.png"
    cpu_int8.size = (30,30)
    cpu_int8.pos = (settings_pos[0]+5,settings_pos[1]+5+40*2)
    cpu_int8.func_on = whisper_handler.model.select
    cpu_int8.parameters_on = cpu_int8
    whisper_handler.model.add_member(cpu_int8,("cpu","int8"))
    
    
    
    whisper_handler.model_size = ui.RadioButton(name="Model-Size")
    
    model_large = ui.Checkbox(screen,name="Model-Size: Large",text="Large Model")
    model_large.texture_unchecked = "images/checkbox_unchecked.png"
    model_large.texture_checked = "images/checkbox_checked.png"
    model_large.size = (30,30)
    model_large.pos = (settings_pos[0]+310,settings_pos[1]+5)
    model_large.func_on = whisper_handler.model_size.select
    model_large.parameters_on = model_large
    whisper_handler.model_size.add_member(model_large,"large-v3")
    
    model_medium = ui.Checkbox(screen,name="Model-Size: Medium",text="Medium Model")
    model_medium.texture_unchecked = "images/checkbox_unchecked.png"
    model_medium.texture_checked = "images/checkbox_checked.png"
    model_medium.size = (30,30)
    model_medium.pos = (settings_pos[0]+310,settings_pos[1]+5+40)
    model_medium.func_on = whisper_handler.model_size.select
    model_medium.parameters_on = model_medium
    whisper_handler.model_size.add_member(model_medium,"medium")
    
    model_small = ui.Checkbox(screen,name="Model-Size: Small",text="Small Model")
    model_small.texture_unchecked = "images/checkbox_unchecked.png"
    model_small.texture_checked = "images/checkbox_checked.png"
    model_small.size = (30,30)
    model_small.pos = (settings_pos[0]+310,settings_pos[1]+5+40*2)
    model_small.func_on = whisper_handler.model_size.select
    model_small.parameters_on = model_small
    whisper_handler.model_size.add_member(model_small,"small")
    
    
    timestamp_setting = ui.Checkbox(screen,name="Timestamp Setting",text="Show Timestamps")
    timestamp_setting.texture_unchecked = "images/checkbox_unchecked.png"
    timestamp_setting.texture_checked = "images/checkbox_checked.png"
    timestamp_setting.size = (30,30)
    timestamp_setting.pos = (settings_pos[0]+5,settings_pos[1]+5+40*3+10)
    timestamp_setting.func_on = whisper_handler.timestamps_on
    timestamp_setting.func_off = whisper_handler.timestamps_off
    
    
    # Run Program GUI
    
    program_gui_pos = (settings_pos[0],settings_pos[1]+settings_size[1]+settings_spacing)
    program_gui_size = (settings_size[0],window_size[1]-settings_size[1]-settings_pos[1]-settings_spacing*2)
    
    button_spacing = 5
    
    program_gui_overlay = ui.Image(screen,name="Program-GUI-Overlay",filename="images/overlay-480x150.png",mode="resize")
    program_gui_overlay.pos = program_gui_pos
    program_gui_overlay.size = program_gui_size
    
    load_file_textbox = ui.TextBox(screen,name="Load-File-Textbox",can_edit=False,spacing=10,texture="images/search_box.png")
    load_file_textbox.size = (program_gui_size[0]-button_spacing*2,50)
    load_file_textbox.pos = (program_gui_pos[0]+button_spacing,program_gui_pos[1]+button_spacing)
    load_file_textbox.text = "..."
    load_file_textbox.font = default_font
    whisper_handler.source_textbox_link = load_file_textbox
    
    search_load_file = ui.Button(screen,name="Select file",spacing=5,texture_released="images/search_released.png",texture_highlighted="images/search_highlighted.png",texture_pressed="images/search_pressed.png")
    search_load_file.func_clicked = thread_load_file
    search_load_file.parameters_clicked = whisper_handler
    search_load_file.size = (125,load_file_textbox.size[1]-button_spacing*2)
    search_load_file.pos = (load_file_textbox.pos[0]+load_file_textbox.size[0]-button_spacing-search_load_file.size[0],load_file_textbox.pos[1]+button_spacing)
    search_load_file.text = "Select file"
    
    
    save_button = ui.Button(screen,name="Save output",spacing=5,texture_released="images/copy_released.png",texture_highlighted="images/copy_highlighted.png",texture_pressed="images/copy_pressed.png")
    save_button.func_clicked = thread_save_func
    save_button.parameters_clicked = whisper_handler
    save_button.size = (search_load_file.size[0]+button_spacing,(program_gui_overlay.size[1]-load_file_textbox.size[1]-button_spacing*2-button_spacing*2)/2)
    save_button.pos = (program_gui_overlay.pos[0]+program_gui_overlay.size[0]-save_button.size[0]-button_spacing,load_file_textbox.pos[1]+load_file_textbox.size[1]+button_spacing)
    save_button.text = "Save"
    
    copy_button = ui.Button(screen,name="Copy output",spacing=5,texture_released="images/copy_released.png",texture_highlighted="images/copy_highlighted.png",texture_pressed="images/copy_pressed.png")
    copy_button.func_clicked = copy_func
    copy_button.parameters_clicked = whisper_handler
    copy_button.size = save_button.size
    copy_button.pos = (program_gui_overlay.pos[0]+program_gui_overlay.size[0]-save_button.size[0]-button_spacing,load_file_textbox.pos[1]+load_file_textbox.size[1]+save_button.size[1]+button_spacing*2)
    copy_button.text = "Copy"
    
    start_button = ui.Button(screen,name="Start output",spacing=5,texture_released="images/start_released.png",texture_highlighted="images/start_highlighted.png",texture_pressed="images/start_pressed.png")
    start_button.func_clicked = start_whisper
    start_button.parameters_clicked = whisper_handler
    start_button.size = (program_gui_overlay.size[0]-button_spacing*2-button_spacing-save_button.size[0],program_gui_overlay.size[1]-load_file_textbox.size[1]-button_spacing-button_spacing*2)
    start_button.pos = (program_gui_overlay.pos[0]+button_spacing,load_file_textbox.pos[1]+load_file_textbox.size[1]+button_spacing)
    start_button.text = "Start Transcription"
    whisper_handler.start_button = start_button
    
    
    # Head
    
    head_pos = (settings_spacing,settings_spacing)
    head_size = 480,90
    
    head_overlay = ui.Image(screen,name="Head-Overlay",filename="images/overlay-480x90.png",mode="resize")
    head_overlay.pos = head_pos
    head_overlay.size = head_size
    
    # Presets
    gpu_fp16.locked = not(cuda_available)
    gpu_int8.locked = not(cuda_available)
    cpu_int8.check()
    
    model_small.check()
    
    timestamp_setting.check()
    
    # Tooltip-Arrays
    
    tooltip_gpu_fp16 = ui.TooltipArray()
    tooltip_gpu_fp16.pos = gpu_fp16.pos
    tooltip_gpu_fp16.size = gpu_fp16.size
        
    tooltip_gpu_int8 = ui.TooltipArray()
    tooltip_gpu_int8.pos = gpu_int8.pos
    tooltip_gpu_int8.size = gpu_int8.size
    
    tooltip_cpu_int8 = ui.TooltipArray()
    tooltip_cpu_int8.pos = cpu_int8.pos
    tooltip_cpu_int8.size = cpu_int8.size
    tooltip_cpu_int8.text = "Use CPU in memory efficiency mode"
    
    if not(cuda_available):
        tooltip_gpu_int8.text = "Unavailable on this system"
        tooltip_gpu_fp16.text = "Unavailable on this system"
    else:
        tooltip_gpu_int8.text = "Use GPU in memory efficiency mode"
        tooltip_gpu_fp16.text = "Use GPU in precision mode"
        
        
    tooltip_manager.add_tooltip([tooltip_gpu_fp16,tooltip_gpu_int8,tooltip_cpu_int8])
    
    tooltip_timestamps = ui.TooltipArray()
    tooltip_timestamps.pos = timestamp_setting.pos
    tooltip_timestamps.size = timestamp_setting.size
    tooltip_timestamps.text = "Turn timestamps on/off"
    
    tooltip_manager.add_tooltip([tooltip_timestamps])
    
    
    tooltip_model_large = ui.TooltipArray()
    tooltip_model_large.pos = model_large.pos
    tooltip_model_large.size = model_large.size
    tooltip_model_large.text = "Highest precision, Worst Performance"
    
    tooltip_model_medium = ui.TooltipArray()
    tooltip_model_medium.pos = model_medium.pos
    tooltip_model_medium.size = model_medium.size
    tooltip_model_medium.text = "Medium precision, Medium Performance"
    
    tooltip_model_small = ui.TooltipArray()
    tooltip_model_small.pos = model_small.pos
    tooltip_model_small.size = model_small.size
    tooltip_model_small.text = "Lowest precision, Best Performance"
    
    tooltip_manager.add_tooltip([tooltip_model_large,tooltip_model_medium,tooltip_model_small])

    
    tooltip_save = ui.TooltipArray()
    tooltip_save.pos = save_button.pos
    tooltip_save.size = save_button.size
    tooltip_save.text = "Save the text to a file"
    
    tooltip_copy = ui.TooltipArray()
    tooltip_copy.pos = copy_button.pos
    tooltip_copy.size = copy_button.size
    tooltip_copy.text = "Copy the text to the clipboard"
    
    tooltip_start = ui.TooltipArray()
    tooltip_start.pos = start_button.pos
    tooltip_start.size = start_button.size
    tooltip_start.text = "Start the transcription process"
    
    tooltip_search = ui.TooltipArray()
    tooltip_search.pos = search_load_file.pos
    tooltip_search.size = search_load_file.size
    tooltip_search.text = "Load a video or audio file"
    
    tooltip_manager.add_tooltip([tooltip_save,tooltip_copy,tooltip_start,tooltip_search])
    
    
    # Manager
    
    ui_manager = ui.EventListener()
    ui_manager.subscribe([textbox_output,textbox_output_overlay])
    ui_manager.subscribe([whisper_progress,info_box])
    ui_manager.subscribe([load_file_textbox,search_load_file])
    for member in whisper_handler.model.members:
        ui_manager.subscribe(member[0])
    for member in whisper_handler.model_size.members:
        ui_manager.subscribe(member[0])
    ui_manager.subscribe([timestamp_setting])
    ui_manager.subscribe([settings_overlay])
    ui_manager.subscribe([copy_button,save_button,start_button])
    ui_manager.subscribe([program_gui_overlay])
    ui_manager.subscribe([head_overlay])
    
    ui_manager.subscribe([tooltip_manager,tooltip_manager.tooltip_box]) # Tooltips überlagern alles andere
    
    
    
    
    # Program Loop
    while running:
        # INPUT
        for event in pygame.event.get():
            if event.type == pygame.MOUSEWHEEL:
                if event.y != 0 and textbox_output_overlay.collision(pygame.mouse.get_pos()):
                    dir = int((event.y/abs(event.y)))
                    new_pos = (textbox_output.pos[0],textbox_output.pos[1]+20*event.y)
                    if new_pos[1] >= 0:
                        new_pos = (new_pos[0],0)
                    textbox_output.moveto(pos=new_pos,speed=abs(event.y*2))
                    
            if event.type == pygame.QUIT:
                running = False
            ui_manager.notify(event)

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_t:
                    print(f"Time: {print_time(whisper_handler.progress)} / {print_time(whisper_handler.duration)}")
                if event.key == pygame.K_i:
                    print(f"Language: {whisper_handler.language} ({(whisper_handler.language_percentage*100):.2f}%)")
                if event.key == pygame.K_s:
                    take_screenshot(screen,window_size)
                if event.key == pygame.K_1:
                    pass
                if event.key == pygame.K_2:
                    print(whisper_handler.text_output)
                    '''
                    t.moveto(pos=(100,50),speed=3)
                    d.moveto(pos=(300,50),speed=2)
                    b.moveto(pos=(10,10),speed=1.8)
                    m.moveto(pos=(0,50),speed=1.5)
                    '''
                if event.key == pygame.K_UP:
                    pass
                if event.key == pygame.K_DOWN:
                    pass
                
            
            if event.type == pygame.MOUSEBUTTONUP:
                pass
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
        
        
        # LOGIC
        
        # VISUAL
        screen.fill(white)
        ui_manager.tick()
        ui_manager.drawall()
        
        
        # RESET
        
        # Refresh Window
        pygame.display.flip()
        clock.tick(fps)
        
    pygame.quit()

if __name__ == "__main__":
    main()