import configparser
from wx import App
from keyboard import add_hotkey
from tray_frame import TrayFrame
from main_frame import MainFrame




import tkinter as tk
root = tk.Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()





# Startup settings
config = configparser.ConfigParser()
config.read('settings.ini')
API_KEY = config['App settings']['api_key']
FPS = int(config['App settings']['fps'])
TRAY_POSITION = config['App settings']['tray_position']

HOTKEY_HELP = config['Hotkey settings']['hotkey_help']
HOTKEY_SCAN = config['Hotkey settings']['hotkey_scan']
HOTKEY_EXIT = config['Hotkey settings']['hotkey_exit']


# Init app
app = App()
main_frame = MainFrame(FPS, API_KEY, screen_width, screen_height)
tray_frame = TrayFrame(TRAY_POSITION, HOTKEY_HELP, HOTKEY_SCAN, HOTKEY_EXIT, screen_width)


# Turn scan
add_hotkey(HOTKEY_SCAN, lambda: main_frame.turn_thread())
add_hotkey(HOTKEY_SCAN, lambda: tray_frame.turn_active())


# Turn help
add_hotkey(HOTKEY_HELP, lambda: tray_frame.turn_help())


# Debug hotkey for view hash
add_hotkey('F4', lambda: main_frame.note_item())


# Close app
add_hotkey(HOTKEY_EXIT, lambda: main_frame.Close())
add_hotkey(HOTKEY_EXIT, lambda: tray_frame.Close())


app.MainLoop()
