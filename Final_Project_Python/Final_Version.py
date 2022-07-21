import tkinter as tk
import time
import threading
import random
from turtle import bgcolor, left
from matplotlib.ft2font import VERTICAL
import numpy as np
import pandas as pd
import csv
from PIL import Image, ImageTk
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class TypeSpeedGUI:
    def __init__(self):
        # init funtion for the TypeSpeedGUI
        self.counter = 0
        self.running = False
        self.highscore = 0
        self.error_count = 0
        self.is_wrong = False
        self.is_complete = False
        self.mode = 'WPM'
        self.username = 'Guest'

        #initlize Tkinter object
        self.root = tk.Tk()
        self.root.title('Typing Speed Application')
        self.root.geometry("1280x720")
        self.root.resizable(width=False, height=False)

        #initialize canvas in Tkinter object
        self.main_canvas = tk.Canvas(self.root, width=1280, height=720)
        self.main_canvas.pack(fill="both", expand=True)
        
        #store sample texts in variable
        self.texts = open('Text_Data/samples.txt', 'r').read().split('\n')
        self.scores_filepath = 'Text_Data/highscores.txt'

        #set background image
        self.bg = tk.PhotoImage(file='Pictures/retro-2426631_1280.png')
        self.main_canvas.create_image(0,0, image=self.bg, anchor='nw')
        
        #set image as headline
        self.header = tk.PhotoImage(file='Pictures/text-1657229404573.png')
        self.main_canvas.create_image(640,130, image=self.header)

        #set highscore picture for display of personal highscore on the left
        self.highscore_display = Image.open('Pictures/Highscore_display.png')
        self.highscore_display_resized = self.highscore_display.resize((124,66))
        self.highscore_display_converted = ImageTk.PhotoImage(self.highscore_display_resized)
        self.main_canvas.create_image(150,270,image = self.highscore_display_converted)

        #display sample texts 
        self.label = self.main_canvas.create_text(640,330,text=random.choice(self.texts), font=('Helvetica', 15, 'bold'))

        #create box for user input
        self.input_entry = tk.Entry(self.root, width=40, font=('Helvetica', 24), bg="white", insertbackground="black")
        self.main_canvas.create_window(640,380, window=self.input_entry)
        self.input_entry.bind("<KeyRelease>", self.start)
        self.input_entry.focus()

        # create performance attributes of the user and display with inital values 
        self.speed_label = self.main_canvas.create_text(640,600,text = '  Speed: \n0.00 CPM\n0.00 WPM\n0.00 ACC', font=('Helvetica', 20, 'bold'), fill="#d789d7")

        #create reset button
        reset_image = Image.open("Pictures/Reset_Button.png")
        resized_reset_image = reset_image.resize((70,35))
        converted_reset_image = ImageTk.PhotoImage(resized_reset_image)
        self.reset_button = tk.Button(self.main_canvas, image=converted_reset_image, command=self.reset, borderwidth=0)
        self.main_canvas.create_window(338, 440, anchor="nw", window=self.reset_button)

        #create highscore button
        highscore_image = Image.open("Pictures/Highscore_Button.png")
        resized_highscore_image = highscore_image.resize((100,35))
        converted_highscore_image = ImageTk.PhotoImage(resized_highscore_image)
        self.display_hs_button = tk.Button(self.main_canvas, image=converted_highscore_image, command=self.display_highscores, borderwidth=0)
        self.main_canvas.create_window(498,440, anchor="nw", window=self.display_hs_button)

        #create settings button
        settings_image = Image.open("Pictures/Settings_Button.png")
        resized_settings_image = settings_image.resize((85,35))
        converted_settings_image = ImageTk.PhotoImage(resized_settings_image)
        self.display_hs_button = tk.Button(self.main_canvas, image=converted_settings_image, command=self.settings, borderwidth=0)
        self.main_canvas.create_window(688,440, anchor="nw", window=self.display_hs_button)

        #create history button
        history_image = Image.open("Pictures/History_Button.png")
        resized_history_image = history_image.resize((80,35))
        converted_history_image = ImageTk.PhotoImage(resized_history_image)
        self.history_button = tk.Button(self.main_canvas, image=converted_history_image, command=self.show_history, borderwidth=0)
        self.main_canvas.create_window(863,440, anchor="nw", window=self.history_button)

        #create personal and overall highscore label and display below "highscore"-picture
        self.highscore_label = self.main_canvas.create_text(150,350, text=f'Overall: {self.get_highscore()[0]}{self.mode}\nYour:     {self.get_highscore()[1]}{self.mode}', font=('Helvetica', 15, 'bold'), fill="#14849F")        
        
        #display everything 
        self.main_canvas.pack(fill='both', expand=True)
        
        self.root.mainloop()

    def start(self, event):
        '''
        Starts the time thread and checks for spelling errors which are counted and stored in the self.error_count. 
        It also checks if the player is done (sentenced is finished).
        '''
        # starts and terminates the threaded main loop 
        if not self.is_complete:
            if not self.running:
                self.running = True
                t = threading.Thread(target=self.time_thread)
                t.start()
            if not self.main_canvas.itemcget(self.label, 'text').startswith(self.input_entry.get()):
                self.input_entry.config(fg='red')
                if not self.is_wrong:
                    self.is_wrong = True
                    self.error_count += 1
            else:
                self.input_entry.config(fg='black')
                self.is_wrong = False
            if self.input_entry.get() == self.main_canvas.itemcget(self.label, 'text'):
                self.input_entry.config(state='disabled')
                self.running = False
                self.is_complete = True

    def time_thread(self):
        '''
        Calculates the WPM, Accuracy and CPM. The results are displayed on the screen below the entry box.
        '''
        # main loop: computes cpm, wpm, acc and stores results
        while self.running:
            time.sleep(0.1)
            self.counter += 0.1
            cps = len(self.input_entry.get())/self.counter
            cpm = cps * 60
            wps = len(self.input_entry.get().split(" "))/self.counter
            wpm = wps * 60
            if len(self.input_entry.get()) != 0:
                accuracy = 100 * (len(self.input_entry.get()) - self.error_count) / len(self.input_entry.get())
            else:
                accuracy = 0
            self.main_canvas.itemconfig(self.speed_label, text=f'    Speed: \n{cpm:.2f} CPM\n{wpm:.2f} WPM\n{accuracy:.2f}% ACC')
        if self.is_complete:
            self.store_score(round(cpm, 2), round(wpm, 2), round(accuracy, 2))

            
    def reset(self):
        '''
        Resets all variables to the initial values, enables the input box again and deletes the previous typed text. 
        It also sets a new sentence for a new type test.
        '''
        # resets the game to a new input sentence
        self.running = False
        self.counter = 0
        self.error_count = 0
        self.is_complete = False
        self.main_canvas.itemconfig(self.speed_label, text='   Speed: \n0.00 CPM\n0.00 WPM\n0.00 ACC')
        self.main_canvas.itemconfig(self.highscore_label, text=f'Overall: {self.get_highscore()[0]}{self.mode}\nYour:     {self.get_highscore()[1]}{self.mode}')
        self.main_canvas.itemconfig(self.label, text=random.choice(self.texts))
        self.input_entry.config(state='normal')
        self.input_entry.delete(0, tk.END)
            
            
    def store_score(self, cpm, wpm, accuracy):
        '''
        Stores the score of CPM, WPM and Accuracy in a dictonary. The current score is then added to the csv with the previous scores and sorted to the right place.
       
        Parameter
        ---------
        cpm, wpm, accuracy: calculated score of the cpm, wpm and accuracy from the player
        '''
        # stores the current score in the user_database.csv file and sorts it
        now = datetime.now()
        date = now.strftime('%d/%m/%Y')
        time = now.strftime('%H:%M:%S')
        data = {'Username': [self.username], 'CPM': [cpm], 'WPM': [wpm], 'ACC': [f'{accuracy}%'], 'Date': [date], 'Time': [time]}
        
        new = pd.DataFrame(data=data)
        old = pd.read_csv('Text_Data/user_database.csv')
        
        df = pd.concat([old, new], ignore_index=True)
        df.reset_index()
        sorted_df = df.sort_values(by=[self.mode], ascending=False)
        sorted_df.to_csv('Text_Data/user_database.csv', index=False)
        
    def sort_scores(self):
        '''
        Sorts the highscore list after the selected mode.
        
        Modes
        ------
        CPM: Character per minute
        WPM: Words per minute
        '''
        # sorts the highscores in the user_database.csv file
        df = pd.read_csv('Text_Data/user_database.csv')
        sorted_df = df.sort_values(by=[self.mode], ascending=False)
        sorted_df.to_csv('Text_Data/user_database.csv', index=False)

    def get_highscore(self):
        '''
        Reads the current personal and overall highscore and returns them.
        '''
        # reads and returns the current personal and overall highscores from a csv file
        highscores = pd.read_csv('Text_Data/user_database.csv')
        if highscores.empty:
            return 0,0
        else:
            ovrl_high = highscores.iloc[0][self.mode]
            my_scores = highscores[highscores['Username']==self.username]
            if not my_scores.empty:
                my_high = my_scores.iloc[0][self.mode]
            else:
                my_high = 0
        return ovrl_high, my_high
    
    def show_history(self):
        '''
        Plots the users score history.

        Axes
        ----
        x-axis: Number of tries
        y-axis: Score
        '''
        # plots the user's scores using matplotlib
        highscores = pd.read_csv('Text_Data/user_database.csv')
        my_data = highscores[highscores['Username']==self.username]
        my_scores = my_data.sort_values(['Date', 'Time']).reset_index()[self.mode]
        
        sub = tk.Toplevel(self.root)
        sub.transient(self.root)
        sub.geometry('481x400')
        sub.title('My Typing History')
        figure = plt.Figure(figsize=(12,6), dpi=100)
        figure_canvas = FigureCanvasTkAgg(figure, sub)
        axes = figure.add_subplot()
        axes.plot(my_scores)
        axes.set_ylabel('Score')
        axes.set_xlabel(f'typing tests executed by {self.username}')
        
        figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    
    def display_highscores(self):
        '''
        Displays the highscore list in a new window. The highscore list is taken from the csv file where the values are stored.
        '''
       # function to display csv file in tkinter
        sub = tk.Toplevel(self.root)
        sub.transient(self.root)
        sub.geometry('577x381')
        sub.title('Highscores')
        sub.resizable(False, True)
        
        with open('Text_Data/user_database.csv') as f:
            reader = csv.reader(f)
            r = 0
            # for every entry in the csv file, create a label in tkinter toplevel
            for col in reader:
                c = 0
                for row in col:
                    label = tk.Label(sub, width = 10, height = 2, text = row, relief = tk.RIDGE)
                    label.grid(row=r, column=c)
                    c += 1
                r += 1
        
    def settings(self):
        '''
        Opens a window where the user can entry her name and define the mode in which the highscores should be stored.
        '''
        # create a settings window
        sub = tk.Toplevel(self.root)
        sub.transient(self.root)
        sub.geometry('400x300')
        sub.title('Settings')
        sub.resizable(False, False)   
        
        # change username 
        user_label = tk.Label(sub, width = 10, height = 2, text = 'Username:')
        user_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        
        input_variable = tk.StringVar()
        input_variable.set(self.username)
        entry_variable = tk.Entry(sub, width = 20, font=('Helvetica', 12), textvariable=input_variable)
        entry_variable.grid(row=0, column=2, columnspan=2, padx=5, pady=5)
        
        # select wpm / cpm ranking
        ranking_label = tk.Label(sub, width = 10, height = 2, text = 'Ranking:')
        ranking_label.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        
        cpm_button = tk.Button(sub, text='CPM', command=lambda: self.set_mode('CPM'))
        wpm_button = tk.Button(sub, text='WPM', command=lambda: self.set_mode('WPM'))

        cpm_button.grid(row=1, column=1, columnspan=2, padx=20, pady=5)
        wpm_button.grid(row=1, column=3, columnspan=2, padx=5, pady=5)
        
        # submit changes button
        button_submit = tk.Button(sub, text='save changes', command=lambda: self.commit_new_settings(input_variable, sub))
        button_submit.grid(row=2, column=2, columnspan=2, padx=5, pady=5)

        
    def commit_new_settings(self, username, sub):
        '''
        Stores the username of the user and closes the window. Then it resets the game.

        Parameter:
        ---------
        username: The text that was put in by the user. In the best case her username
        sub: The window where the setting is in
        '''
        # submit_button function
        self.username = username.get()
        sub.destroy()
        sub.update()
        self.reset()
    
    def set_mode(self, mode):
        '''
        Defines the function of the button that determines what the highscore list is ordered by. 

        Parameter
        ---------
        mode: is the selected mode by the user (WPM/CPM)
        '''
        # ranking buttons funtion
        self.mode = mode
        self.sort_scores()

def main():
    speedtest = TypeSpeedGUI()


if __name__ == "__main__":
    main()
