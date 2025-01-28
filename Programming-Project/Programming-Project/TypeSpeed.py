import tkinter as tk
from tkinter import messagebox
import random
import time
from tkinter import ttk

# Function to load words from file
def load_words_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            words = file.read().splitlines()  # Reads each line as a separate word
        return words
    except FileNotFoundError:
        messagebox.showerror("Error", "Words file not found. Please check the file path.")
        return []
    
# Constants
WORDS = load_words_from_file("words.txt")  # Load words from file

if not WORDS:  # Stop program if file is empty or not found
    raise ValueError("Word list is empty or not loaded correctly.")
   

# Global Variables
correct_word_count = 0
total_word_count = 0
start_time = None
time_left = 60
current_word = None


# Timer Functions
def start_timer():
    global time_left
    if time_left > 0:
        time_left -= 1
        timer_label.config(text=f"Remaining time: {time_left} sec")
        window.after(1000, start_timer)
    else:
        end_game()


def end_game():
    input_field.config(state="disabled")
    accuracy = (correct_word_count / total_word_count) * 100 if total_word_count > 0 else 0
    wpm = correct_word_count
    messagebox.showinfo("Time is up!",
                        f"Correct Words: {correct_word_count}\n"
                        f"Words Per Minute (WPM): {wpm}\n"
                        f"Total Words: {total_word_count}\n"
                        f"Accuracy: {accuracy:.2f}%")
    window.quit()


def handle_space_press(event):
    global correct_word_count, total_word_count, start_time, current_word

    if start_time is None:
        start_time = time.time()
        instruction_label.destroy()
        start_timer()
        display_new_word()

    user_input = input_field.get().strip()
    total_word_count += 1

    if not user_input:
        return "break"

    event.widget.delete(0, tk.END)

    if user_input == current_word:
        correct_word_count += 1
        input_field.config(foreground="green")
    else:
        input_field.config(foreground="red")

    update_labels()
    input_field.delete(0, tk.END)
    display_new_word()


def validate_partial_input(event):
    user_input = input_field.get().strip()
    if current_word and current_word.startswith(user_input):
        input_field.config(foreground="green")
    else:
        input_field.config(foreground="red")


def display_new_word():
    global current_word
    current_word = random.choice(WORDS)
    word_label.config(text=current_word)


def update_labels():
    correct_label.config(text=f"Correct Words: {correct_word_count}")
    total_label.config(text=f"Total Words: {total_word_count}")


# UI Setup
window = tk.Tk()
window.title("Type Speed Calculator")
window.geometry("600x400")
window.configure(background="#1c1e24")

style = ttk.Style()
style.theme_use("clam")  


style.configure(
    "CustomEntry.TEntry",
    fieldbackground="#2b2d35",  
    foreground="#ffffff",  
    font=("Helvetica", 20) 
)

style.configure(
    "CustomLabel.TLabel",
    background="#1c1e24",  
    foreground="#ffffff", 
    font=("Helvetica", 18)  
)

style.configure(
    "HighlightLabel.TLabel",
    background="#1c1e24",
    foreground="#ffc107",
    font=("Helvetica", 22)
)

style.configure(
    "SuccessLabel.TLabel",
    background="#1c1e24",
    foreground="#28a745",
    font=("Helvetica", 20)
)

# Instruction Label
instruction_label = ttk.Label(window, text="PRESS SPACE TO START!", style="HighlightLabel.TLabel")
instruction_label.pack(pady=20)

# Word Display Label
word_label = ttk.Label(window, text="", style="CustomLabel.TLabel")
word_label.pack(pady=20)

# Input Field
input_field = ttk.Entry(window, style="CustomEntry.TEntry",font=("Helvetica",15))
input_field.pack(pady=10, ipadx=5, ipady=5)
input_field.bind("<space>", handle_space_press)
input_field.bind("<KeyRelease>", validate_partial_input)

# Timer Label
timer_label = ttk.Label(window, text="Remaining time: 60 sec", style="HighlightLabel.TLabel")
timer_label.pack(pady=10)

# Correct Words Label
correct_label = ttk.Label(window, text="Correct Words: 0", style="SuccessLabel.TLabel")
correct_label.pack(pady=5)

# Total Words Label
total_label = ttk.Label(window, text="Total Words: 0", style="CustomLabel.TLabel")
total_label.pack(pady=5)

window.mainloop()