import tkinter as tk
from tkinter import ttk

# --------------------------
# DATA
# --------------------------

DIRECTIONS = {
    "main gate": "From PESU RR Main Gate → walk straight → take left at the library → you're at the main block.",
    "library": "From PESU RR Main Gate → walk straight for 200m → library is on your left.",
    "atm": "From main block → take right → walk 50m → ATM is beside the stationery shop.",
    "food court": "From library → walk straight → take first right → food court is ahead.",
    "parking": "From main gate → take immediate right → parking lot is straight ahead.",
    "gjbc": "GJBC → Enter PESU RR → walk straight → pass the library → GJBC is the big building on the right with glass front."
}

PLACE_LIST = [
    "Main Gate",
    "Library",
    "ATM",
    "Food Court",
    "Parking",
    "GJBC"
]

# --------------------------
# CHATBOT LOGIC
# --------------------------

def get_response(user_input):
    user_input = user_input.lower()

    # directions
    for place in DIRECTIONS:
        if place in user_input:
            return DIRECTIONS[place]

    # list places
    if "list" in user_input or "places" in user_input:
        return "Here are the places:\n- " + "\n- ".join(PLACE_LIST)

    # fallback
    return "Sorry, I don't have info on that. Try asking: 'directions to library', 'where is ATM', etc."

# --------------------------
# GUI FUNCTIONS
# --------------------------

def send_message(event=None):
    user_text = user_entry.get().strip()
    if user_text == "":
        return

    chat_window.configure(state="normal")
    chat_window.insert(tk.END, f"You: {user_text}\n", "user")

    bot_reply = get_response(user_text)
    chat_window.insert(tk.END, f"Bot: {bot_reply}\n\n", "bot")

    chat_window.configure(state="disabled")
    chat_window.see(tk.END)
    user_entry.delete(0, tk.END)

def show_places():
    chat_window.configure(state="normal")
    chat_window.insert(tk.END, "Bot: Available places:\n- " + "\n- ".join(PLACE_LIST) + "\n\n", "bot")
    chat_window.configure(state="disabled")
    chat_window.see(tk.END)

# --------------------------
# GUI SETUP (Dark Theme)
# --------------------------

root = tk.Tk()
root.title("PESU Helper Bot")
root.geometry("500x600")
root.configure(bg="#1e1e1e")

# Style
style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", background="#333333", foreground="white", padding=10, relief="flat")
style.map("TButton", background=[("active", "#444444")])

# Chat window
chat_window = tk.Text(root, bg="#121212", fg="white", font=("Segoe UI", 11), bd=0, wrap="word")
chat_window.pack(padx=10, pady=10, fill="both", expand=True)
chat_window.tag_config("user", foreground="#4FC3F7")
chat_window.tag_config("bot", foreground="#A5D6A7")
chat_window.configure(state="disabled")

# Entry + Send button
bottom_frame = tk.Frame(root, bg="#1e1e1e")
bottom_frame.pack(fill="x", padx=10, pady=10)

user_entry = tk.Entry(bottom_frame, font=("Segoe UI", 12), bg="#2b2b2b", fg="white", insertbackground="white")
user_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

send_button = ttk.Button(bottom_frame, text="Send", command=send_message)
send_button.pack(side="right")

# Buttons bar
button_frame = tk.Frame(root, bg="#1e1e1e")
button_frame.pack(pady=5)

places_button = ttk.Button(button_frame, text="List Places", command=show_places)
places_button.pack(side="left", padx=5)

# Enter key binding
user_entry.bind("<Return>", send_message)

root.mainloop()
