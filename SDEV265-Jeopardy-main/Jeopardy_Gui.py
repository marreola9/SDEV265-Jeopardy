import tkinter as tk
from tkinter import simpledialog, messagebox
import csv
import difflib
import Jeopardy_menu  # Importing the menu module where team names are entered

main_bg = '#333652'
fg = '#E9EAEC'
category_bg = '#333652'
button_bg = '#90ADC6'

class GUI:
    def __init__(self, root, main_bg, fg, category_bg, button_bg, team_one_name, team_two_name):
        self.root = root
        self.button_bg = button_bg
        self.main_bg = main_bg
        self.fg = fg
        self.category_bg = category_bg
        self.questions = []
        self.team_one_name = team_one_name  # Initialize team names from the parameter
        self.team_two_name = team_two_name
        self.setup_root()
        self.create_category_frame()
        self.create_button_frame()
        self.create_team_frame()

    def setup_root(self):
        self.root.geometry("1500x900")
        self.root.title("SDEV 265 - Jeopardy")
        self.root.configure(background=main_bg)

    def create_team_frame(self):
        label_frame = tk.Frame(self.root, background=(category_bg))
        
        team_label = tk.Label(label_frame, text=("Team Names"),font=('monospace', 30), background=(main_bg), foreground=(fg))
        team_label.grid(row=1, column=0, sticky="n", padx="5", pady="5"  )
        
        team_one_label = tk.Label(label_frame, text=f"Team One: {self.team_one_name}",font=('monospace', 20), background=(button_bg), foreground=(fg))
        team_one_label.grid(row=2, column=0, sticky='n', padx="5", pady="5"  )
        team_two_label = tk.Label(label_frame, text=f"Team Two: {self.team_two_name}",font=('monospace', 20), background=(button_bg), foreground=(fg))
        team_two_label.grid(row=3, column=0, sticky="n", padx="5", pady="5"  )
        
        label_frame.pack(fill="x")

    def create_category_frame(self):
        category_frame = tk.Frame(self.root, background=main_bg)
        
        for category_heading in range(6):
            category_frame.columnconfigure(category_heading, weight = 1)

        # Read categories from CSV
        categories = self.read_categories_from_csv('questions.csv')

        for category_title, category in enumerate(categories):
            category_label = tk.Label(category_frame, text=category, font=('monospace', 35), background=category_bg, foreground=fg)
            category_label.grid(row=0, column=category_title, sticky=tk.W+tk.E, padx="5", pady="5")

        category_frame.pack(fill="both")

    def read_categories_from_csv(self, filename):
        categories = []
        try:
            with open(filename, 'r', newline='', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    category = row['Category']
                    if category not in categories:
                        categories.append(category)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        return categories

    def create_button_frame(self):
        button_frame = tk.Frame(self.root, background=self.category_bg)

        # Read questions from CSV
        self.questions = self.read_questions_from_csv('questions.csv')

        # Configure columns to expand proportionally
        num_categories = len(self.questions)
        for column_index in range(num_categories):
            button_frame.grid_columnconfigure(column_index, weight=1)

        # Create buttons dynamically based on categories and values
        for category_index, category in enumerate(self.questions):
            for value_index, question in enumerate(category):
                button_text = f"${(value_index + 1) * 200}"
                button = tk.Button(button_frame, text=button_text, font=('monospace', 40), background=self.button_bg, foreground=self.fg)
                button.grid(row=value_index + 1, column=category_index, sticky=tk.W+tk.E, padx="5", pady="5")
                button.config(command=lambda q=question: self.show_question(q))

        button_frame.pack(fill="x")


    def read_questions_from_csv(self, filename):
        questions = [[] for _ in range(5)]  # 5 rows (values) per category
        try:
            with open(filename, 'r', newline='', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    category = row['Category']
                    value = row['Value']
                    question = {'Question': row['Question'], 'Answer': row['Answer']}
                    index = (int(value[1:]) // 200) - 1  # Calculate index based on value ($200, $400, etc.)
                    if index < 5:  # Ensure index is within range of 0-4 (for rows 0 to 4)
                        questions[index].append(question)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        return questions

    def show_question(self, question_data):
        question_text = question_data['Question']
        answer_text = question_data['Answer']

        # Display question in a messagebox
        messagebox.showinfo("Question", question_text)

        # Prompt user for their answer
        user_answer = simpledialog.askstring("Answer", "Please enter your answer:")

        if user_answer:
            # Check if the answer is close enough to be considered correct
            if self.is_answer_close_enough(user_answer, answer_text):
                messagebox.showinfo("Correct!","That's right! The full correct answer is: " + answer_text)
            else:
                messagebox.showinfo("Incorrect", f"Sorry, that's incorrect. The correct answer is: {answer_text}")
        else:
            messagebox.showwarning("No Answer", "No answer was entered.")

    def is_answer_close_enough(self, user_answer, correct_answer):
        # Convert both answers to lowercase and remove leading/trailing spaces
        user_answer = user_answer.lower().strip()
        correct_answer = correct_answer.lower().strip()
        
        # Token-based matching
        user_tokens = set(user_answer.split())
        correct_tokens = set(correct_answer.split())

        # Check for significant overlap in tokens
        common_tokens = user_tokens & correct_tokens
        token_match_ratio = len(common_tokens) / len(correct_tokens)

        # If a significant number of tokens match, consider it correct
        if token_match_ratio >= 0.5:
            return True

        # Use SequenceMatcher for a finer similarity measurement
        similarity_ratio = difflib.SequenceMatcher(None, user_answer, correct_answer).ratio()

        # If similarity ratio is above a threshold (e.g., 0.6), consider it close enough
        return similarity_ratio >= 0.6

def start_game(team_one_name, team_two_name):
    root = tk.Tk()
    game_gui = GUI(root, main_bg, fg, category_bg, button_bg, team_one_name, team_two_name)
    root.mainloop()

if __name__ == "__main__":
    # Retrieve team names from Jeopardy_menu module
    team_one_name, team_two_name = Jeopardy_menu.get_team_names()

    # Start the game with retrieved team names
    start_game(team_one_name, team_two_name)
