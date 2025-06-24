import pyautogui as ag
import time
import AutoClick
import multiprocessing as mp
import keyboard
import tkinter as tk
import threading

distance_multiplier = 10

def travel_distance(key, travel, player_speed, current_travel):
    travel *= distance_multiplier
    distance = 0
    time_0 = time.time()
    with player_speed.get_lock():
        speed_0 = float(player_speed.value)
    while distance < travel:
        for k in key:
            ag.keyDown(k)
        with current_travel.get_lock():
            current_travel.value = distance
        time_1 = time.time()
        elapsed_time = time_1 - time_0
        with player_speed.get_lock():
            speed_1 = float(player_speed.value)
        avg_speed = (speed_0 + speed_1) / 2
        added_distance = elapsed_time * avg_speed
        distance += added_distance
        
        time_0 = time_1
        speed_0 = speed_1

def snake_path(player_speed, current_travel, stop_flag=False, x=1, z=1):
    import pyautogui as ag
    import time


    

    while not stop_flag:
        for num in range(z):
            travel_distance(['d'], x, player_speed, current_travel)
            travel_distance(['s'], 1, player_speed, current_travel)
            travel_distance(['a'], x, player_speed, current_travel)
            travel_distance(['s'], 1, player_speed, current_travel)
        travel_distance(['w', 'a'], (z + 1) * 2, player_speed, current_travel)

class main:
    def __init__(self):
        self.player_speed = mp.Value('d', 20.0)
        self.start_time = time.time()
        self.end = False
        self.current_travel = mp.Value('d', 0.0)

        self.paths = {
            "snake" : snake_path
            #"square" : self.square,
            #"rectangle" : self.rectangle
        }


        

        self.processes = []
        self.update_thread = threading.Thread(target=self.update_loop, daemon=True)
        self.update_thread.start()

        #self.path_process = path(self.paths["snake"], self.current_travel)
        #self.path_process.start_process()
        #self.processes.append(self.path_process)

        self.path_process = mp.Process(target=self.paths["snake"], args=(self.player_speed, self.current_travel, self.end, 2, 2))
        self.path_process.start()
        self.processes.append(self.path_process)

        auto_clicker = AutoClick.AutoClick()
        self.processes.append(auto_clicker.click_process)

        self.start_gui()


    #def snake_path(self, x=1, z=1):
    #    while True:
    #        for num in range(z):
    #            self.travel_distance(['d'], x)
    #            self.travel_distance(['s'], 1)
    #            self.travel_distance(['a'], x)
    #            self.travel_distance(['s'], 1)
    #        self.travel_distance(['w', 'a'], (z+  1) * 2)
    #
    #def square(self, x=2):
    #    while True:
    #        for direction in ['d', 's', 'a', 'w']:
    #            self.travel_distance([direction], x)
    #
    #def rectangle(self, x=2, z=1):
    #    while True:
    #        self.travel_distance('d', x)
    #        self.travel_distance('s', z)
    #        self.travel_distance('a', x)
    #        self.travel_distance('w', z)

    


    def travel_distance(self, key, travel):
        travel *= distance_multiplier
        for k in key:
            ag.keyDown(k)
        distance = 0
        time_0 = time.time()
        speed_0 = self.player_speed
        while distance < travel:
            with self.current_travel.get_lock():
                self.current_travel.value = distance
            time_1 = time.time()
            elapsed_time = time_1 - time_0
            speed_1 = self.player_speed
            avg_speed = (speed_0 + speed_1) / 2
            added_distance = elapsed_time * avg_speed
            distance += added_distance
            
            time_0 = time_1
            speed_0 = speed_1
        for k in key:
            ag.keyUp(k)
        

    def update_loop(self):

        
        keyboard.on_press_key('-', lambda _: self.stop_program())
        
        with self.player_speed.get_lock():
            self.player_speed = mp.Value('d', 20.0)
    
    
    def stop_program(self):
        self.end = True
        for process in self.processes:
            process.terminate()

    def start_gui(self):
        root = tk.Tk()
        root.title("Live Number Display")

        label = tk.Label(root, text="0", font=("Helvetica", 48))
        label.pack(padx=20, pady=20)

        def update_display():
            with self.current_travel.get_lock():
                value = self.current_travel.value
            label.config(text=str(value))
            root.after(500, update_display)
        
        update_display()
        root.mainloop()


class path:
    def __init__(self, func, shared_value, args=()):
        self.func = func
        self.args = args
        self.shared_value = shared_value
    
    def start_process(self):
        ag.mouseDown(button="left")
        self.process = mp.Process(target=self.func, args=self.args)
        self.process.start()
    
    def terminate_process(self):
        self.process.terminate()
        ag.mouseUp(button="left")


if __name__ == '__main__':
    mp.freeze_support()
    time.sleep(5)
    print("Main is running")
    run = main()