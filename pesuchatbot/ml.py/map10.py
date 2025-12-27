import tkinter as tk
from tkinter import ttk, scrolledtext
from datetime import datetime

# -------------------------
# DATA: places + descriptions
# -------------------------
PLACES = {
    "Golden Jubilee Block (GJBC)": {
        "short": "Main academic block near the food court (southeast area).",
        "directions": "From the main courtyard head southeast — food court and GJB basketball court nearby."
    },
    "Hornbill Coffee": {
        "short": "Coffee shop on the east side of the GJBC crop.",
        "directions": "From GJBC, walk east across the open area; Hornbill Coffee is on the right."
    },
    "PESU Gym": {
        "short": "Gym near the north/top-center of the crop.",
        "directions": "Head north from Golden Jubilee Block across the courtyard."
    },
    "Central Library": {
        "short": "Central library located northwest of GJBC.",
        "directions": "From GJBC walk northwest across the open area to reach the library building."
    },
    "Mechanical (C) Block": {
        "short": "Central landmark in the crop.",
        "directions": "From GJBC head slightly northwest to find the Mechanical block."
    },
    "Badminton Court": {
        "short": "Badminton courts to the northeast of Mechanical block.",
        "directions": "From GJBC go northeast across the courtyard to reach the badminton courts."
    },
    "Basketball Court": {
        "short": "Basketball court just south of GJBC.",
        "directions": "From GJBC exit south to reach the basketball court."
    },
    "GJB Food Court": {
        "short": "Food court next to Golden Jubilee Block (east/southeast).",
        "directions": "From the GJBC main entrance, walk east-southeast to the food court."
    },
    "JV Technosoft": {
        "short": "Tech office located southwest in the crop.",
        "directions": "Located southwest of the Central Library area."
    },
    # additional campus places from your later image
    "Front Gate": {
        "short": "Main entrance of PES RR campus (south).",
        "directions": "Enter from front gate and follow the main road into campus."
    },
    "Scooter Parking": {
        "short": "Two-wheeler parking area near the front entrance.",
        "directions": "Park scooters near the front gate area."
    },
    "Car Parking": {
        "short": "Four-wheeler parking area in the north zone.",
        "directions": "Drive to the north-most parking lot."
    },
    "Student Lounge": {
        "short": "Relaxation and hangout zone near the center of the campus.",
        "directions": "Near A Block and central pathways."
    },
    "M Block": {
        "short": "Academic block located near the southern region.",
        "directions": "Located near the south side, close to front gate."
    },
    "A Block": {
        "short": "Central academic building with lecture halls.",
        "directions": "Central area — find via main paths from the courtyard."
    },
    "F Block": {
        "short": "Activity & events area; sports nearby.",
        "directions": "Toward the northwest region of the campus."
    },
    "Tech Park": {
        "short": "Startup incubators & tech offices near central campus.",
        "directions": "Close to library and central academic blocks."
    },
    "Boys Hostel": {
        "short": "Student accommodation (boys).",
        "directions": "Located on the eastern side of campus."
    },
    "Girls Hostel": {
        "short": "Student accommodation (girls).",
        "directions": "Located near the central-west area of campus."
    },
    "Cricket Field": {
        "short": "Sports field on the north side.",
        "directions": "Go north from central campus to reach the cricket field."
    },
    "Event Ground": {
        "short": "Open ground used for ceremonies and events.",
        "directions": "Central open area near the student lounge."
    }
}

# -------------------------
# UI colors & constants
# -------------------------
BG = "#0b1220"
CARD = "#0f1724"
TEXT = "#E6EEF6"
MUTED = "#9AA9B2"
ACCENT = "#06b6d4"
BTN_BG = "#08323a"
BTN_HOVER = "#0ea5a4"
USER_COLOR = "#A5D6A7"
BOT_COLOR = "#91E5F6"
TIMESTAMP_COLOR = "#94a3b8"
FONT_REG = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 11, "bold")

# -------------------------
# Helper functions
# -------------------------
def timestamp():
    return datetime.now().strftime("%H:%M")

# -------------------------
# Tkinter App
# -------------------------
class PESUChatApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PESU GJBC Assistant")
        self.configure(bg=BG)
        self.geometry("1000x650")
        self.minsize(900, 600)
        self._create_widgets()
        self._place_widgets()
        self._bind_events()

    def _create_widgets(self):
        # Left panel: Places list (scrollable)
        self.left_card = tk.Frame(self, bg=CARD, bd=0)
        self.left_title = tk.Label(self.left_card, text="Places", bg=CARD, fg=TEXT, font=FONT_BOLD)

        # canvas + scrollbar to host buttons grid
        self.places_canvas = tk.Canvas(self.left_card, bg=CARD, highlightthickness=0)
        self.places_frame = tk.Frame(self.places_canvas, bg=CARD)
        self.places_vscroll = ttk.Scrollbar(self.left_card, orient="vertical", command=self.places_canvas.yview)
        self.places_canvas.configure(yscrollcommand=self.places_vscroll.set)

        # Center panel: Chat
        self.center_card = tk.Frame(self, bg=CARD)
        self.center_title = tk.Label(self.center_card, text="Chat", bg=CARD, fg=TEXT, font=FONT_BOLD)
        self.chatbox = scrolledtext.ScrolledText(self.center_card, wrap=tk.WORD, bg="#071821", fg=TEXT,
                                                font=FONT_REG, bd=0, padx=8, pady=8)
        self.chatbox.tag_config("user", foreground=USER_COLOR, font=FONT_REG)
        self.chatbox.tag_config("bot", foreground=BOT_COLOR, font=FONT_REG)
        self.chatbox.tag_config("meta", foreground=TIMESTAMP_COLOR, font=("Segoe UI", 8))
        self.chatbox.insert(tk.END, "Bot: Hi — I'm the PESU GJBC assistant. Click a place or type a question.\n\n", "bot")
        self.chatbox.configure(state=tk.DISABLED)

        # input
        self.input_frame = tk.Frame(self.center_card, bg=CARD)
        self.user_entry = tk.Entry(self.input_frame, bg="#071a1d", fg=TEXT, insertbackground=TEXT, font=FONT_REG)
        self.send_btn = tk.Button(self.input_frame, text="Send", bg=ACCENT, fg=BG, font=FONT_BOLD, activebackground=BTN_HOVER, command=self._on_send)

        # Right panel: Quick actions & About
        self.right_card = tk.Frame(self, bg=CARD)
        self.right_title = tk.Label(self.right_card, text="Quick Actions", bg=CARD, fg=TEXT, font=FONT_BOLD)
        self.show_list_btn = tk.Button(self.right_card, text="Show Places List", bg=BTN_BG, fg=TEXT, command=self._populate_places_display)
        self.clear_btn = tk.Button(self.right_card, text="Clear Chat", bg=BTN_BG, fg=TEXT, command=self._clear_chat)
        self.about_label = tk.Label(self.right_card, text="This local assistant contains GJBC + PESU RR campus info.\nClick a place to view short description and directions.", bg=CARD, fg=MUTED, justify="left", wraplength=260)

        # Prepare buttons grid inside places_frame
        self.place_buttons = []  # store (btn, key)

    def _place_widgets(self):
        # layout left
        self.left_card.place(x=12, y=12, width=300, height=620)
        self.left_title.pack(anchor="nw", padx=12, pady=(10,4))
        self.places_canvas.pack(side="left", fill="both", expand=True, padx=(12,0), pady=8)
        self.places_vscroll.pack(side="right", fill="y", padx=(0,12), pady=8)
        # add frame to canvas
        self.places_canvas.create_window((0, 0), window=self.places_frame, anchor="nw")
        self.places_frame.bind("<Configure>", lambda e: self.places_canvas.configure(scrollregion=self.places_canvas.bbox("all")))

        # layout center
        self.center_card.place(x=330, y=12, width=480, height=620)
        self.center_title.pack(anchor="nw", padx=12, pady=(10,4))
        self.chatbox.pack(fill="both", expand=True, padx=12, pady=(0,8))
        self.input_frame.pack(fill="x", padx=12, pady=8)
        self.user_entry.pack(side="left", fill="x", expand=True, padx=(0,8))
        self.send_btn.pack(side="right")

        # layout right
        self.right_card.place(x=825, y=12, width=155, height=620)
        self.right_title.pack(anchor="nw", padx=12, pady=(10,8))
        self.show_list_btn.pack(fill="x", padx=12, pady=(0,8))
        self.clear_btn.pack(fill="x", padx=12, pady=(0,8))
        self.about_label.pack(anchor="nw", padx=12, pady=(12,0))

        # finally populate place buttons
        self._populate_places()

    def _bind_events(self):
        # scrolling with mousewheel on canvas
        def _on_mousewheel(event):
            self.places_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        # different OS events
        self.places_canvas.bind_all("<MouseWheel>", _on_mousewheel)   # Windows
        self.places_canvas.bind_all("<Button-4>", lambda e: self.places_canvas.yview_scroll(-1, "units"))  # Linux
        self.places_canvas.bind_all("<Button-5>", lambda e: self.places_canvas.yview_scroll(1, "units"))

        # Enter to send
        self.user_entry.bind("<Return>", lambda e: self._on_send())

    # -------------------------
    # Places handling
    # -------------------------
    def _populate_places(self):
        # Remove old buttons
        for child in self.places_frame.winfo_children():
            child.destroy()
        self.place_buttons.clear()

        keys = list(PLACES.keys())
        # two-column grid
        cols = 1  # 1 column in left panel for bigger buttons (makes it prettier)
        for i, key in enumerate(keys):
            b = tk.Button(self.places_frame, text=key, width=32, anchor="w",
                          bg=BTN_BG, fg=TEXT, relief="flat", padx=8,
                          command=lambda k=key: self._on_place_click(k))
            b.grid(row=i, column=0, padx=6, pady=6, sticky="w")
            # hover effects
            b.bind("<Enter>", lambda e, w=b: w.configure(bg=BTN_HOVER))
            b.bind("<Leave>", lambda e, w=b: w.configure(bg=BTN_BG))
            self.place_buttons.append((b, key))

    def _populate_places_display(self):
        # show places list in chat
        text = "Bot: Available places:\n" + "\n".join(f"- {k}" for k in PLACES.keys())
        self._append_bot(text)

    def _on_place_click(self, key):
        info = PLACES.get(key, {})
        text = f"{key}\n\n{info.get('short','No short info')}\n\nDirections: {info.get('directions','No directions available')}"
        self._append_user(f"Where is {key}?")
        self._append_bot(text)

    # -------------------------
    # Chat functions
    # -------------------------
    def _on_send(self):
        q = self.user_entry.get().strip()
        if not q:
            return
        # display user message
        self._append_user(q)
        self.user_entry.delete(0, tk.END)
        # generate simple response
        resp = self._generate_response(q)
        self._append_bot(resp)

    def _generate_response(self, q):
        q_l = q.lower()
        # check for place mention
        for key in PLACES.keys():
            if key.lower() in q_l or any(word in q_l for word in key.lower().split()):
                info = PLACES[key]
                return f"{key}\n\n{info.get('short','')}\n\nDirections: {info.get('directions','')}"
        # list places
        if "list" in q_l or "places" in q_l:
            return "Places:\n" + "\n".join(f"- {k}" for k in PLACES.keys())
        # common shortcuts
        if "gjbc" in q_l or "golden" in q_l:
            info = PLACES.get("Golden Jubilee Block (GJBC)")
            return f"{info['label'] if 'label' in info else 'Golden Jubilee Block (GJBC)'}\n\n{info['short']}\n\nDirections: {info['directions']}"
        # fallback
        return "Sorry — I don't have an exact answer. Try clicking a place button or ask 'List places'."

    def _append_user(self, text):
        self.chatbox.configure(state=tk.NORMAL)
        self.chatbox.insert(tk.END, f"You: {text}\n", "user")
        self.chatbox.insert(tk.END, f"{timestamp()}\n\n", "meta")
        self.chatbox.configure(state=tk.DISABLED)
        self.chatbox.yview_moveto(1.0)

    def _append_bot(self, text):
        self.chatbox.configure(state=tk.NORMAL)
        # preserve newlines, prefix
        prefix = "Bot: "
        for line in text.splitlines():
            self.chatbox.insert(tk.END, f"{prefix if line == text.splitlines()[0] else '    '}{line}\n", "bot")
        self.chatbox.insert(tk.END, f"{timestamp()}\n\n", "meta")
        self.chatbox.configure(state=tk.DISABLED)
        self.chatbox.yview_moveto(1.0)

    def _clear_chat(self):
        self.chatbox.configure(state=tk.NORMAL)
        self.chatbox.delete("1.0", tk.END)
        self.chatbox.insert(tk.END, "Bot: Hi — I'm the PESU GJBC assistant. Click a place or type a question.\n\n", "bot")
        self.chatbox.configure(state=tk.DISABLED)

# -------------------------
# Run app
# -------------------------
if __name__ == "__main__":
    app = PESUChatApp()
    app.mainloop()
