import pyautogui as ag
import time
import Test as cs
import multiprocessing as mp
import keyboard
import tkinter as tk
import threading

def click(click_speed):
    ag.click()
    time.sleep(click_speed)
    click(click_speed)

class AutoClick:
    def __init__(self):
        self.click_speed = 1 / 8
        self.status = mp.Value('b', 0)

        self.update_thread = threading.Thread(target=self.update_loop, daemon=True)
        self.update_thread.start()

        self.click_process = mp.Process(target=click(), args=(self.click_speed))
        self.click_process.start()

        self.start_gui()

    def update_loop(self):
        if keyboard.on_press('-'):
            self.status = mp.Value('b', 0)
            self.click_process.terminate()



    def start_gui(self):
        root = tk.Tk()
        root.title("Live Number Display")

        label = tk.Label(root, text="Off", font=("Helvetica", 48))
        label.pack(padx=20, pady=20)

        def update_display():
            with self.status.get_lock():
                value = "On" if self.status.value == 1 else "Off"
            label.config(text=str(value))
            root.after(500, update_display)
        
        update_display()
        root.mainloop()

#if __name__ == '__main__'
mp.freeze_support()
time.sleep(5)
run = AutoClick()