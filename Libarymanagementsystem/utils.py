import os
import time

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def wait_and_clear(seconds=2):
    time.sleep(seconds)
    clear_screen()
