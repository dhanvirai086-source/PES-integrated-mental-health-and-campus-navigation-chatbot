import tkinter as tk
from tkinter import scrolledtext

# -----------------------
# PES University Data
# -----------------------

places = {
    "Front Gate": "Main entrance of PESU RR campus.",
    "Scooter Parking": "Scooter parking is located near the A-block entrance.",
    "Student Lounge": "Chill spot near A block for students.",
    "Hostel": "The boys and girls hostels are located near the back gate.",
    "MRD Block": "Admin block where documents are handled.",
    "A Block": "Contains lecture halls, labs and classrooms.",
    "F Block": "Sports, clubs, hackathons and activity areas.",
    "G Block": "Departments such as CSE, labs and classrooms.",
    "H Block": "Library and higher education classrooms.",
    "Eco Park": "Large green area near the parking zone.",
    "PESU Food Court": "Main food court beside the sports area.",
    "ViewPoint Café": "Coffee and snacks area near the PESU dome.",
    "PESU Dome": "E-sports events, gatherings, ceremonies.",
    "Parking Lot": "Main car parking area at the top of campus.",
    "Cricket Field": "Near F-block.",
    "Basketball Court": "Behind Student Lounge.",
    "Tech Park": "Advanced engineering labs."
}

directions = {
    ("Front Gate", "A Block"): "Enter from front gate → go straight 200m → A Block is on your right.",
    ("Front Gate", "Eco Park"): "Enter campus → take first left → Eco park is straight ahead.",
    ("A Block", "G Block"): "From A Block → walk towards Student Lounge → continue straight → G Block is on your right.",
    ("G Block", "Food Court"): "From G Block → walk straight → Food Court beside basketball court.",
    ("Hostel", "A Block"): "From hostel → walk to central road → A Block is on your left.",
}

# -----------------------
# Chatbot Logic
# -----------------------

def get_response(user_input):
    user_input = user_input.lower()

    # place lookup
    for place in places:
        if place.lower() in user_input:
            return places[place]

    # direction lookup
    for (start, end) in directions:
        if start.lower() in user_input and end.lower() in user_input:
            return directions[(start, end)]

    return "I’m not sure about that. Try asking about a place or directions!"

# -----------------------
# GUI FUNCTIONS
# -----------------------

def send_message():
    msg = user_entry.get()
    if msg.strip() == "":
        return

    chat_window.insert(tk.END, "You: " + msg + "\n")
    user_entry.delete(0, tk.END)

    reply = get_response(msg)
    chat_window.insert(tk.END, "Bot: " + reply + "\n\n")


def insert_place(place_name):
    chat_window.insert(tk.END, f"You selected: {place_name}\n")
    chat_window.insert(tk.END, f"Bot: {places[place_name]}\n\n")


# -----------------------
# GUI SETUP
# -----------------------

root = tk.Tk()
root.title("PESU Campus Chatbot")
root.geometry("600x650")
root.configure(bg="#E8F0FE")

title = tk.Label(root, text="PESU Campus Chatbot", font=("Arial", 20, "bold"), bg="#E8F0FE")
title.pack(pady=10)

chat_window = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=20, font=("Arial", 12))
chat_window.pack(pady=10)

frame = tk.Frame(root, bg="#E8F0FE")
frame.pack()

user_entry = tk.Entry(frame, width=40, font=("Arial", 14))
user_entry.grid(row=0, column=0, padx=10, pady=10)

send_btn = tk.Button(frame, text="Send", font=("Arial", 12, "bold"), command=send_message)
send_btn.grid(row=0, column=1)

# -----------------------
# Places Buttons
# -----------------------

btn_frame = tk.LabelFrame(root, text="Campus Places", font=("Arial", 12, "bold"), padx=10, pady=10)
btn_frame.pack(pady=10)

row = 0
col = 0

for place in list(places.keys())[:10]:  # you can increase number of buttons later
    b = tk.Button(btn_frame, text=place, width=22, command=lambda p=place: insert_place(p))
    b.grid(row=row, column=col, padx=5, pady=5)
    col += 1
    if col == 2:
        col = 0
        row += 1

root.mainloop()
