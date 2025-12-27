import time
import threading
import tkinter as tk
from tkinter import scrolledtext

# -------------------------------------------------------
# Original main code STARTS here (NOT changed)
# -------------------------------------------------------

def slow_print(text, delay=0.04):
    for char in text:
        gui_print(char)
        time.sleep(delay)
    gui_print("\n")

def ask(question):
    slow_print(question)
    return gui_input()

# -------------------------------------------------------
# Original main code ENDS here
# -------------------------------------------------------


# -----------------------
# GUI FUNCTIONS
# -----------------------

def gui_print(text):
    text_area.config(state="normal")
    text_area.insert(tk.END, text)
    text_area.see(tk.END)
    text_area.config(state="disabled")
    window.update()

def gui_input():
    global user_input_value
    user_input_value = None

    def submit():
        global user_input_value
        user_input_value = input_box.get()
        input_box.delete(0, tk.END)

    submit_button.config(command=submit)

    while user_input_value is None:
        window.update()
        time.sleep(0.05)

    return user_input_value


# ---------------------------------------------
# Run main meditation program in another thread
# ---------------------------------------------

def run_program():
    slow_print("\nWelcome to the inner Journey Program.")
    slow_print("A space to explore awareness, existence, surrender, and the void.\n")

    slow_print("Let's begin...\n")

    name = ask("Before we start, what shall I call you?")

    slow_print(f"\nHello {name}. Let us explore the deeper layers of your existence.\n")

    q1 = ask("who do you believe,who you are:\n"
             "A) The body\n"
             "B) The mind\n"
             "C) The emotions\n"
             "D) The awareness\n"
             "\nI can give a clue:Your answer must be permanent, ever lasting, stable and constant"
             "\nChoose A, B, C, or D:")

    if q1.lower() == "d":
        slow_print("\nYou chose Awareness — the observer behind all experience.")
    else:
        slow_print("\nInteresting perspective. Let's go deeper.")

    slow_print("\nNow tell me in one word what you feel your true nature is.")
    nature = ask("Examples: peace, void, happiness, energy, silence:")

    slow_print(f"\nYou feel your true nature is: {nature.upper()}. Beautiful.\n")

    slow_print("Here is a deeper reflection...")
    time.sleep(1.5)

    slow_print("\nIf you surrender everything — identity, thoughts, fears —")
    slow_print("what remains is often described as the VOID.")
    slow_print("But this void is not empty... it is full of infinite potential.\n")

    q2 = ask("How does this void feel to you like:\n"
             "A) Peaceful nothingness\n"
             "B) Powerful silence\n"
             "C) Spacious awareness\n"
             "D) Presence without identity\n"
             "E) All of the above\n"
             "\nChoose A, B, C, D, or E:")

    slow_print("\nA profound choice.")

    slow_print("\nFinal Reflection:")
    slow_print("-----------------------------------------------")
    slow_print(f"{name}, you have explored:")
    slow_print(f" • Your identity as {nature}")
    slow_print(" • The awareness behind your thoughts")
    slow_print(" • The surrender into the void")
    slow_print("-----------------------------------------------")

    slow_print("\nRemember:")
    slow_print("The one who is watching all of this unfold...")
    slow_print("is not the mind, not the body, but pure awareness.\n")

    slow_print("Thank you for taking this inner journey.\n")
    slow_print("Goodbye, traveller of consciousness. \n")


# --------------------------------------
# BEAUTIFUL UI WITH IMPRESSIVE BACKGROUND
# --------------------------------------

window = tk.Tk()
window.title("PERSONAL ANALYSIS CHATBOT")
window.geometry("800x650")

# Beautiful gradient-like background
window.configure(bg="#0a0f24")   # deep cosmic blue

# Outer glowing frame
frame = tk.Frame(window, bg="#1c2440", highlightbackground="#4c6eff",
                 highlightthickness=3, bd=0)
frame.pack(expand=True, fill="both", padx=20, pady=20)

title = tk.Label(frame, text=" PERSONAL ANALYSIS CHATBOT ",
                 font=("Georgia", 24, "bold"),
                 fg="#8faaff", bg="#1c2440")
title.pack(pady=10)

text_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD,
                                      font=("Consolas", 13),
                                      bg="#0f162f",
                                      fg="#e6e9ff",
                                      insertbackground="white",
                                      relief="flat",
                                      borderwidth=0)
text_area.pack(expand=True, fill="both", padx=10, pady=10)
text_area.config(state="disabled")

input_box = tk.Entry(frame, font=("Consolas", 14),
                     bg="#141f3c", fg="white",
                     insertbackground="white",
                     relief="flat")
input_box.pack(fill="x", padx=10, pady=5)

submit_button = tk.Button(frame, text="Submit",
                          font=("Consolas", 13, "bold"),
                          bg="#4458ff", fg="white",
                          activebackground="#5a6dff",
                          cursor="hand2",
                          relief="flat")
submit_button.pack(pady=5)

threading.Thread(target=run_program, daemon=True).start()

window.mainloop()