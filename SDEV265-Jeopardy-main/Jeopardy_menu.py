import tkinter as tk
import Jeopardy_Gui

main_bg = '#FAD02C'
fg = '#E9EAEC'
category_bg = '#333652'
button_bg = '#90ADC6'

class Menu:
    def __init__(self, root, main_bg, fg, button_bg):
        self.root = root
        self.button = button_bg
        self.main_bg = main_bg
        self.fg = fg
        self.team_one = tk.StringVar()
        self.team_two = tk.StringVar()
        self.setup_root()
        self.create_title_entry_and_button_frame()
        
    def setup_root(self):
        self.root.geometry("1500x800")
        self.root.title("SDEV 265 - Jeopardy")
        self.root.configure(background=(main_bg))
        
    def on_submit(self):
        team_one_name = self.team_one.get()
        team_two_name = self.team_two.get()
        print("Team One name is: ", team_one_name)
        print("Team Two name is: ", team_two_name)
        self.root.destroy()  
        Jeopardy_Gui.start_game(team_one_name, team_two_name)
        
    def create_title_entry_and_button_frame(self):
        title_entry_button_frame = tk.Frame(self.root, background=main_bg)
        
        title_entry_button_frame.grid_columnconfigure(0, weight=1)
        title_entry_button_frame.grid_columnconfigure(1, weight=1)
        
        main_title = tk.Label(title_entry_button_frame, text="Jeopardy", font=('monospace', 100), background=main_bg, foreground=category_bg)
        main_title.grid(row=0, column=0, columnspan=2, pady=(10, 10), sticky="n")

        subtitle = tk.Label(title_entry_button_frame, text="(Enter your team names)", font=('monospace', 25), background=main_bg, foreground=category_bg)
        subtitle.grid(row=1, column=0, columnspan=2, pady=(10, 20), sticky="n")

        team_one_label = tk.Label(title_entry_button_frame, font=('monospace', 30), text="Team One", background=category_bg, foreground=main_bg)
        team_one_label.grid(row=2, column=0, padx=(20, 10), pady=(10, 20), sticky="e")
        
        team_name_one_entry_field = tk.Entry(title_entry_button_frame, textvariable = self.team_one, font=('monospace', 30), background=main_bg, foreground=category_bg)
        team_name_one_entry_field.grid(row=2, column=1, padx=(10, 20), pady=(10, 20), sticky="w")

        team_two_label = tk.Label(title_entry_button_frame, font=('monospace', 30), text="Team Two", background=category_bg, foreground=main_bg)
        team_two_label.grid(row=3, column=0, padx=(20, 10), pady=(10, 20), sticky="e")
        
        team_name_two_entry_field = tk.Entry(title_entry_button_frame, textvariable = self.team_two, font=('monospace', 30), background=main_bg, foreground=category_bg)
        team_name_two_entry_field.grid(row=3, column=1, padx=(10, 20), pady=(10, 20), sticky="w")

        submit_button = tk.Button(title_entry_button_frame, text="Submit", font=('monospace', 30), background=category_bg, foreground=self.main_bg, command= lambda: self.on_submit())
        submit_button.grid(row=4, column=0, columnspan=2, pady=(30, 30), sticky="n")
        
        title_entry_button_frame.place(relx=0.5, rely=0.5, anchor='center')        
        
if __name__ == "__main__":
    root = tk.Tk()
    menu = Menu(root, main_bg, fg, button_bg)
    root.mainloop()
