import tkinter as tk
import random
from tkinter import messagebox

class RockPaperScissorsGame:
    def __init__(self, root):
        self.player_score = 0
        self.computer_score = 0
        self.tie_score = 0
        
        self.root = root
        self.root.title("Rock, Paper, Scissors Game")
        self.root.geometry("350x450") # change size of the window
        self.root.config(bg="lightyellow") # change color
        
        self.title_label = tk.Label(root, text="Rock, Paper, Scissors", font=("Arial", 18), bg="lightyellow")
        self.title_label.pack(pady=20)
        
        self.player_choice_label = tk.Label(root, text="Player: ", font=("Arial", 14), bg="lightyellow")
        self.player_choice_label.pack(pady=10)
        
        self.computer_choice_label = tk.Label(root, text="Computer: ", font=("Arial", 14), bg="lightyellow")
        self.computer_choice_label.pack(pady=10)
        
        self.result_label = tk.Label(root, text="", font=("Arial", 14), bg="lightyellow")
        self.result_label.pack(pady=20)
        
        self.score_label = tk.Label(root, text="Player: 0  |  Computer: 0  |  Ties: 0", font=("Arial", 14), bg="lightyellow")
        self.score_label.pack(pady=10)
        
        button_frame = tk.Frame(root, bg="lightyellow")
        button_frame.pack(pady=20)
        
        rock_button = tk.Button(button_frame, text="Rock💎", font=("Arial", 12), width=8, command=lambda: self.play('rock'))
        rock_button.grid(row=0, column=0, padx=10)
        
        paper_button = tk.Button(button_frame, text="Paper📃", font=("Arial", 12), width=8, command=lambda: self.play('paper'))
        paper_button.grid(row=0, column=1, padx=10)
        
        scissors_button = tk.Button(button_frame, text="Scissors✂️", font=("Arial", 12), width=10, command=lambda: self.play('scissors'))
        scissors_button.grid(row=0, column=2, padx=10)
        
        exit_button = tk.Button(root, text="Exit", font=("Arial", 12), command=self.on_closing)
        exit_button.pack(pady=20)
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def play(self, player_choice):
        choices = ['rock', 'paper', 'scissors']
        computer_choice = random.choice(choices)
        
        self.player_choice_label.config(text=f"Player: {player_choice.capitalize()}")
        self.computer_choice_label.config(text=f"Computer: {computer_choice.capitalize()}")
        
        if player_choice == computer_choice:
            self.tie_score += 1
            self.result_label.config(text="Just saved, It's a Tie!", fg="blue")
        elif (player_choice == 'rock' and computer_choice == 'scissors') or \
             (player_choice == 'scissors' and computer_choice == 'paper') or \
             (player_choice == 'paper' and computer_choice == 'rock'):
            self.player_score += 1
            self.result_label.config(text="Great! You Win!", fg="green")
        else:
            self.computer_score += 1
            self.result_label.config(text="Aaah! You Lose!", fg="red")
        
        self.update_scores()
    
    def update_scores(self):
        self.score_label.config(text=f"Player: {self.player_score}  |  Computer: {self.computer_score}  |  Ties: {self.tie_score}")
    
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    game = RockPaperScissorsGame(root)
    root.mainloop()
