import os
import time
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext
from datetime import datetime
import random

# ====================================================================
# --- FILES & DEFAULT RESPONSES ---
# ====================================================================

RESPONSES_FILE = "responses.txt"
HISTORY_FILE = "chat_history.txt"

DEFAULT_RESPONSES = {
    "stress": "It's okay to feel stressed sometimes. Take a moment to breathe deeply and ground yourself. 🌱",
    "exam": "Exams can be challenging, but you're capable of handling it. Take it one step at a time. ✨",
    "anxiety": "Anxiety can be tough, but you're not alone. Focus on small calming steps. 💚",
    "sad": "It's okay to feel sad sometimes. Be kind to yourself — you deserve care and rest. 💙",
    "hello": "Hey there! I'm glad you reached out. How are you feeling today? 🌼",
    "lonely": "Feeling lonely can be heavy. Remember you matter. 💫",
    "tired": "You must be feeling exhausted. Rest is important — it's okay to slow down. ☁",
    "bye": "Take care of yourself. You're doing your best, and that's enough. 🌷"
}

# Campus Data (Restored)
CAMPUS_PLACES = {
    "Golden Jubilee Block (GJBC)": {"short": "Main academic block near the food court.", "directions": "Head southeast from the main courtyard."},
    "Hornbill Coffee": {"short": "Coffee shop on the east side of the GJBC.", "directions": "Walk east from GJBC across the open area."},
    "Central Library": {"short": "Central library located northwest of GJBC.", "directions": "Walk northwest from GJBC across the open area."},
    "GJB Food Court": {"short": "Food court next to Golden Jubilee Block.", "directions": "Walk east-southeast from the GJBC main entrance."},
    "A Block": {"short": "Central academic building with lecture halls.", "directions": "Find via main paths from the courtyard."},
    "Boys Hostel": {"short": "Student accommodation (boys).", "directions": "Located on the eastern side of campus."},
    "Cricket Field": {"short": "Sports field on the north side.", "directions": "Go north from central campus."}
}

# Campus UI Colors (Restored)
CAMPUS_BG = "#0b1220"
CAMPUS_CARD = "#0f1724"
CAMPUS_TEXT = "#E6EEF6"
CAMPUS_ACCENT = "#06b6d4"
CAMPUS_BTN_BG = "#08323a"
CAMPUS_BTN_HOVER = "#0ea5a4"
CAMPUS_USER_COLOR = "#A5D6A7"
CAMPUS_BOT_COLOR = "#91E5F6"
CAMPUS_TIMESTAMP_COLOR = "#94a3b8"
CAMPUS_FONT_REG = ("Segoe UI", 10)

def ensure_responses_file(filename=RESPONSES_FILE):
    if not os.path.isfile(filename):
        with open(filename, "w", encoding="utf-8") as f:
            for k, v in DEFAULT_RESPONSES.items():
                f.write(f"{k}:{v}\n")

def load_responses(filename=RESPONSES_FILE):
    responses = {}
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                if ":" in line:
                    key, value = line.strip().split(":", 1)
                    key, value = key.lower().strip(), value.strip()
                    if key:
                        responses[key] = value
    except FileNotFoundError:
        pass
    return responses

def save_chat(user, bot, filename=HISTORY_FILE):
    with open(filename, "a", encoding="utf-8") as f:
        now = datetime.now().isoformat()
        f.write(f"{now}  User: {user}\n")
        f.write(f"{now}  Bot: {bot}\n\n")

def timestamp():
    return datetime.now().strftime("%H:%M")

# ====================================================================
# --- EMOTION-AWARE RESPONSE LOGIC (Mental Health) ---
# ====================================================================

POSITIVE_RESPONSES = {
    "good": ["I'm really glad to hear you're feeling good! 😊", "That's nice to hear — keep enjoying your day! 🌱", "Happy to hear that! ✨"],
    "great": ["That's wonderful! 💚", "Love that energy! 🌟"],
    "happy": ["That's beautiful! 😊", "Love to hear that you're feeling happy! 🌈"],
}

NEGATIVE_RESPONSES = {
    "stress": ["It's okay to feel stressed. Take a deep breath and give yourself a moment to relax. 🌱", "Stress can feel heavy. Remember to be kind to yourself. 💛"],
    "tired": ["You must be feeling exhausted. Rest is important — it's okay to slow down. ☁", "Feeling tired is natural after a busy day. Take care of yourself. 🌿"],
    "anxiety": ["Anxiety can be overwhelming, but you're not alone. Focus on small calming steps and breathe deeply. 💚", "I understand anxiety can be tough. Be gentle with yourself. 💛"],
    "sad": ["I'm sorry you're feeling sad. It's okay to take time for yourself. 💙", "Your feelings matter — treat yourself with care."],
}

NEUTRAL_RESPONSES = {
    "hello": "Hey there! I'm glad you reached out. 🌼",
    "hi": "Hi! It's nice to hear from you. 💚",
    "thanks": "You're welcome 🤍",
    "bye": "Take care of yourself. You matter 🌷"
}

REFLECTIVE_FALLBACKS = [
    "I hear you. Would you like to tell me a little more? 💛",
    "That sounds important… I'm here to listen. 🌿",
    "I want to understand better — can you tell me more about that?",
    "You're not alone. Take your time, I'm here. 💚"
]

def get_response(user_input, file_responses):
    text = user_input.lower()

    for key, replies in POSITIVE_RESPONSES.items():
        if key in text:
            return random.choice(replies)

    for key, replies in NEGATIVE_RESPONSES.items():
        if key in text:
            return random.choice(replies)

    for key, reply in NEUTRAL_RESPONSES.items():
        if key in text:
            return reply

    for key, reply in file_responses.items():
        if key in text:
            return reply

    return random.choice(REFLECTIVE_FALLBACKS)

# ====================================================================
# --- COMBINED CHATBOT APPLICATION ---
# ====================================================================

class CombinedChatbot(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🚀 PESU Integrated Support System")
        self.geometry("850x750")
        self.configure(bg="#0a0f24")

        ensure_responses_file()
        self.responses = load_responses()
        self.campus_places = CAMPUS_PLACES

        # Analysis state management for simplified flow
        self.analysis_stage = 0
        self.analysis_data = {}
        self.analysis_questions = [
            "what shall I call you?",
            "Who do you believe you are:\nA) The body\nB) The mind\nC) The emotions\nD) The awareness\n\nChoose A, B, C, or D: ",
            "Now tell me in one word what you feel your true nature is. Examples: peace, void, happiness, energy, silence: ",
            "How does this void feel to you:\nA) Peaceful nothingness\nB) Powerful silence\nC) Spacious awareness\nD) Presence without identity\nE) All of the above\n\nChoose A, B, C, D, or E: "
        ]
        self.analysis_output_delay = 50 # millisecond delay for slow print effect

        self._build_ui()

    def _build_ui(self):
        # Main header
        header_frame = tk.Frame(self, bg="#1c2440", highlightbackground="#4c6eff", highlightthickness=3)
        header_frame.pack(fill=tk.X, padx=15, pady=15)
        
        header_label = tk.Label(
            header_frame,
            text="🚀 PESU Support Center 🌙",
            font=("Georgia", 22, "bold"),
            fg="#8faaff",
            bg="#1c2440",
            pady=10
        )
        header_label.pack()

        # Notebook (tabs)
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background='#0a0f24', borderwidth=0)
        style.configure('TNotebook.Tab', background='#1c2440', foreground='#8faaff',
                        padding=[20, 10], font=('Segoe UI', 11, 'bold'))
        style.map('TNotebook.Tab', background=[('selected', '#4c6eff')],
                  foreground=[('selected', 'white')])

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both', padx=15, pady=(0, 15))

        # Tab 1: Campus Assistant
        self.campus_frame = tk.Frame(self.notebook, bg=CAMPUS_BG)
        self.notebook.add(self.campus_frame, text="🗺️ Campus Assistant")
        self._build_campus_tab()

        # Tab 2: Personal Analysis
        self.analysis_frame = tk.Frame(self.notebook, bg="#1c2440")
        self.notebook.add(self.analysis_frame, text="🧘 Personal Analysis")
        self._build_analysis_tab()

        # Tab 3: Mental Health Support
        self.support_frame = tk.Frame(self.notebook, bg="#f0f4f7")
        self.notebook.add(self.support_frame, text="💚 Mental Health Support")
        self._build_support_tab()

    # ====================================================================
    # --- TAB 1: CAMPUS ASSISTANT FUNCTIONS (UNCHANGED) ---
    # ====================================================================

    def _build_campus_tab(self):
        # UI structure similar to the previous simple version
        main_frame = tk.Frame(self.campus_frame, bg=CAMPUS_BG)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        # Left Panel: Places List
        self.campus_left_card = tk.Frame(main_frame, bg=CAMPUS_CARD, bd=0)
        self.campus_left_card.grid(row=0, column=0, padx=(0, 12), sticky="nswe")
        
        tk.Label(self.campus_left_card, text="Places", bg=CAMPUS_CARD, fg=CAMPUS_TEXT, font=("Segoe UI", 11, "bold")).pack(anchor="nw", padx=12, pady=(10,4))

        self.campus_places_canvas = tk.Canvas(self.campus_left_card, bg=CAMPUS_CARD, highlightthickness=0)
        self.campus_places_frame = tk.Frame(self.campus_places_canvas, bg=CAMPUS_CARD)
        self.campus_places_vscroll = ttk.Scrollbar(self.campus_left_card, orient="vertical", command=self.campus_places_canvas.yview)
        
        self.campus_places_canvas.configure(yscrollcommand=self.campus_places_vscroll.set)
        self.campus_places_canvas.pack(side="left", fill="both", expand=True, padx=(12,0), pady=8)
        self.campus_places_vscroll.pack(side="right", fill="y", padx=(0,12), pady=8)
        self.campus_places_canvas.create_window((0, 0), window=self.campus_places_frame, anchor="nw")
        
        self.campus_places_frame.bind("<Configure>", lambda e: self.campus_places_canvas.configure(scrollregion=self.campus_places_canvas.bbox("all")))
        self._populate_campus_places()
        
        # Center Panel: Chat
        self.campus_center_card = tk.Frame(main_frame, bg=CAMPUS_CARD)
        self.campus_center_card.grid(row=0, column=1, sticky="nswe")
        
        tk.Label(self.campus_center_card, text="Campus Chat", bg=CAMPUS_CARD, fg=CAMPUS_TEXT, font=("Segoe UI", 11, "bold")).pack(anchor="nw", padx=12, pady=(10,4))
        
        self.campus_chatbox = scrolledtext.ScrolledText(self.campus_center_card, wrap=tk.WORD, bg="#071821", fg=CAMPUS_TEXT,
                                                        font=CAMPUS_FONT_REG, bd=0, padx=8, pady=8)
        self.campus_chatbox.tag_config("user", foreground=CAMPUS_USER_COLOR, font=CAMPUS_FONT_REG)
        self.campus_chatbox.tag_config("bot", foreground=CAMPUS_BOT_COLOR, font=CAMPUS_FONT_REG)
        self.campus_chatbox.tag_config("meta", foreground=CAMPUS_TIMESTAMP_COLOR, font=("Segoe UI", 8))
        self.campus_chatbox.insert(tk.END, "Bot: Hi — I'm the PESU Campus assistant. Click a place or type a question.\n\n", "bot")
        self.campus_chatbox.configure(state=tk.DISABLED)
        self.campus_chatbox.pack(fill="both", expand=True, padx=12, pady=(0,8))

        # Input
        campus_input_frame = tk.Frame(self.campus_center_card, bg=CAMPUS_CARD)
        campus_input_frame.pack(fill="x", padx=12, pady=8)
        self.campus_user_entry = tk.Entry(campus_input_frame, bg="#071a1d", fg=CAMPUS_TEXT, insertbackground=CAMPUS_TEXT, font=CAMPUS_FONT_REG)
        self.campus_user_entry.pack(side="left", fill="x", expand=True, padx=(0,8))
        tk.Button(campus_input_frame, text="Send", bg=CAMPUS_ACCENT, fg=CAMPUS_BG, font=("Segoe UI", 11, "bold"), activebackground=CAMPUS_BTN_HOVER, command=self._on_campus_send).pack(side="right")
        self.campus_user_entry.bind("<Return>", lambda e: self._on_campus_send())

        # Configure weights for resizing
        main_frame.grid_columnconfigure(0, weight=30)
        main_frame.grid_columnconfigure(1, weight=70)
        main_frame.grid_rowconfigure(0, weight=1)

    def _populate_campus_places(self):
        for child in self.campus_places_frame.winfo_children():
            child.destroy()
        keys = list(self.campus_places.keys())
        for i, key in enumerate(keys):
            b = tk.Button(self.campus_places_frame, text=key, width=32, anchor="w",
                          bg=CAMPUS_BTN_BG, fg=CAMPUS_TEXT, relief="flat", padx=8,
                          command=lambda k=key: self._on_campus_place_click(k))
            b.grid(row=i, column=0, padx=6, pady=6, sticky="w")
            b.bind("<Enter>", lambda e, w=b: w.configure(bg=CAMPUS_BTN_HOVER))
            b.bind("<Leave>", lambda e, w=b: w.configure(bg=CAMPUS_BTN_BG))
            
    def _on_campus_place_click(self, key):
        info = self.campus_places.get(key, {})
        text = f"{key}\n\n{info.get('short','No short info')}\n\nDirections: {info.get('directions','No directions available')}"
        self._append_campus_user(f"Where is {key}?")
        self._append_campus_bot(text)

    def _on_campus_send(self):
        q = self.campus_user_entry.get().strip()
        if not q: return
        self._append_campus_user(q)
        self.campus_user_entry.delete(0, tk.END)
        resp = self._generate_campus_response(q)
        self._append_campus_bot(resp)

    def _generate_campus_response(self, q):
        q_l = q.lower()
        for key in self.campus_places.keys():
            if key.lower() == q_l or key.lower() in q_l or any(word in q_l.split() for word in key.lower().split()):
                info = self.campus_places[key]
                return f"{key}\n\n{info.get('short','')}\n\nDirections: {info.get('directions','')}"
        
        if "list" in q_l or "places" in q_l:
            return "Places:\n" + "\n".join(f"- {k}" for k in self.campus_places.keys())
        
        if "gjbc" in q_l or "golden" in q_l:
            key = "Golden Jubilee Block (GJBC)"
            info = self.campus_places.get(key)
            if info: return f"{key}\n\n{info['short']}\n\nDirections: {info['directions']}"
            
        return "Sorry — I don't have an exact answer. Try clicking a place button or asking for a list."

    def _append_campus_user(self, text):
        self.campus_chatbox.configure(state=tk.NORMAL)
        self.campus_chatbox.insert(tk.END, f"You: {text}\n", "user")
        self.campus_chatbox.insert(tk.END, f"{timestamp()}\n\n", "meta")
        self.campus_chatbox.configure(state=tk.DISABLED)
        self.campus_chatbox.yview_moveto(1.0)

    def _append_campus_bot(self, text):
        self.campus_chatbox.configure(state=tk.NORMAL)
        prefix = "Bot: "
        lines = text.splitlines()
        for i, line in enumerate(lines):
            p = prefix if i == 0 else ' ' * len(prefix) 
            self.campus_chatbox.insert(tk.END, f"{p}{line}\n", "bot")
        self.campus_chatbox.insert(tk.END, f"{timestamp()}\n\n", "meta")
        self.campus_chatbox.configure(state=tk.DISABLED)
        self.campus_chatbox.yview_moveto(1.0)
    
    # ====================================================================
    # --- TAB 2: PERSONAL ANALYSIS FUNCTIONS (SIMPLIFIED/SYNCHRONOUS) ---
    # ====================================================================

    def _build_analysis_tab(self):
        # Personal Analysis GUI
        self.analysis_text = scrolledtext.ScrolledText(
            self.analysis_frame,
            wrap=tk.WORD,
            font=("Consolas", 12),
            bg="#0f162f",
            fg="#e6e9ff",
            insertbackground="white",
            relief="flat",
            borderwidth=0
        )
        self.analysis_text.pack(expand=True, fill="both", padx=15, pady=15)
        self.analysis_text.config(state="disabled")

        input_frame = tk.Frame(self.analysis_frame, bg="#1c2440")
        input_frame.pack(fill="x", padx=15, pady=(0, 15))

        self.analysis_input = tk.Entry(
            input_frame,
            font=("Consolas", 13),
            bg="#141f3c",
            fg="white",
            insertbackground="white",
            relief="flat"
        )
        self.analysis_input.pack(side=tk.LEFT, fill="x", expand=True, padx=(0, 10), ipady=8)

        self.analysis_submit = tk.Button(
            input_frame,
            text="Start", # Changed initial text to Start
            font=("Consolas", 12, "bold"),
            bg="#4458ff",
            fg="white",
            activebackground="#5a6dff",
            cursor="hand2",
            relief="flat",
            width=12,
            command=self._start_analysis # New starting command
        )
        self.analysis_submit.pack(side=tk.RIGHT)
        
        # Initial display
        self._analysis_print("\nWelcome to the Inner Journey Program. Click 'Start' to begin...")

    def _start_analysis(self):
        # Reset state and start the process
        self.analysis_stage = 0
        self.analysis_data = {}
        self.analysis_text.config(state="normal")
        self.analysis_text.delete(1.0, tk.END)
        self.analysis_text.config(state="disabled")
        self._analysis_print("\nWelcome to the Inner Journey Program.")
        self._analysis_print("A space to explore awareness, existence, surrender, and the void.\n")
        self._analysis_print("Let's begin...\n")
        
        self.analysis_submit.config(text="Submit", command=self._process_analysis_input)
        self.after(500, self._next_analysis_step) # Use after for sequential flow

    def _analysis_print(self, text, user=False):
        self.analysis_text.config(state="normal")
        if user:
            self.analysis_text.insert(tk.END, text + "\n", ("user" if user else "bot"))
        else:
            self.analysis_text.insert(tk.END, text + "\n")
        self.analysis_text.see(tk.END)
        self.analysis_text.config(state="disabled")

    def _next_analysis_step(self):
        if self.analysis_stage < len(self.analysis_questions):
            question = self.analysis_questions[self.analysis_stage]
            self._analysis_print(f"[{self.analysis_stage+1}] {question}")
        else:
            self._final_analysis_summary()

    def _process_analysis_input(self):
        user_input = self.analysis_input.get().strip()
        if not user_input:
            self._analysis_print("Please enter a response.", user=False)
            return
            
        self.analysis_input.delete(0, tk.END)
        
        # Display user input
        self._analysis_print(f"> {user_input}", user=True) 

        # Store response
        if self.analysis_stage == 0:
            self.analysis_data['name'] = user_input
        elif self.analysis_stage == 1:
            self.analysis_data['who'] = user_input
        elif self.analysis_stage == 2:
            self.analysis_data['nature'] = user_input
        elif self.analysis_stage == 3:
            self.analysis_data['void'] = user_input
            
        self.analysis_stage += 1
        self._next_analysis_step()


    def _final_analysis_summary(self):
        name = self.analysis_data.get('name', 'Traveller')
        who = self.analysis_data.get('who', 'not given')
        nature = self.analysis_data.get('nature', 'undefined')

        self._analysis_print("\nAnalysis Complete.")
        self._analysis_print("-----------------------------------------------")
        self._analysis_print(f"{name}, you have explored:")
        self._analysis_print(f" • Your primary belief of self is: {who.upper()}")
        self._analysis_print(f" • You feel your true nature is: {nature.upper()}")
        
        if who.lower() == 'd' or who.lower() == 'awareness':
             self._analysis_print("This aligns with the concept of pure awareness.")

        self._analysis_print("-----------------------------------------------")

        self._analysis_print("\nThank you for taking this inner journey.")
        self._analysis_print("Goodbye, traveller of consciousness. 🌙\n")
        
        self.analysis_submit.config(text="Start", command=self._start_analysis)
    

    # ====================================================================
    # --- TAB 3: MENTAL HEALTH SUPPORT FUNCTIONS (UNCHANGED) ---
    # ====================================================================

    def _build_support_tab(self):
        # Mental Health Support GUI
        chat_frame = tk.Frame(self.support_frame, bg="#f0f4f7")
        chat_frame.pack(padx=15, pady=15, fill=tk.BOTH, expand=True)

        self.support_canvas = tk.Canvas(chat_frame, bg="#f0f4f7", highlightthickness=0)
        self.support_scrollbar = ttk.Scrollbar(chat_frame, orient="vertical", command=self.support_canvas.yview)
        # support_inner holds the chat bubbles
        self.support_inner = tk.Frame(self.support_canvas, bg="#f0f4f7")

        self.support_inner.bind(
            "<Configure>",
            lambda e: self.support_canvas.configure(scrollregion=self.support_canvas.bbox("all"))
        )
        self.support_canvas.create_window((0, 0), window=self.support_inner, anchor="nw")
        self.support_canvas.configure(yscrollcommand=self.support_scrollbar.set)

        self.support_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.support_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Input area
        input_frame = tk.Frame(self.support_frame, bg="#f0f4f7")
        input_frame.pack(fill=tk.X, padx=15, pady=(0, 15))

        self.support_input = tk.Entry(
            input_frame,
            font=("Segoe UI", 12),
            bg="white",
            fg="#154360",
            relief="flat"
        )
        self.support_input.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=10, padx=(0, 10))
        self.support_input.bind("<Return>", self._on_support_send)

        self.support_btn = tk.Button(
            input_frame,
            text="Send ➤",
            command=self._on_support_send,
            font=("Segoe UI", 11, "bold"),
            bg="#5dade2",
            fg="white",
            activebackground="#3498db",
            activeforeground="white",
            relief="flat",
            width=10
        )
        self.support_btn.pack(side=tk.RIGHT)

        # Welcome message
        self._insert_support_message(
            "Hello! I'm your PESU Support companion 🌼 How are you feeling today?",
            is_user=False
        )

    def _insert_support_message(self, msg, is_user=True):
        # This creates the unique chat bubble appearance
        frame = tk.Frame(self.support_inner, bg="#f0f4f7")
        
        if is_user:
            bubble = tk.Label(frame, text=msg, wraplength=450, justify="left", font=("Segoe UI", 11), 
                              bg="#aed6f1", fg="#154360", padx=12, pady=10, anchor="w", bd=0, relief="flat")
            bubble.pack(anchor="e", padx=10, pady=4)
            frame.pack(anchor="e", fill=tk.X)
        else:
            bubble = tk.Label(frame, text=msg, wraplength=450, justify="left", font=("Segoe UI", 11), 
                              bg="#d6eaf8", fg="#1b2631", padx=12, pady=10, anchor="w", bd=0, relief="flat")
            bubble.pack(anchor="w", padx=10, pady=4)
            frame.pack(anchor="w", fill=tk.X)

        self.support_canvas.update_idletasks()
        self.support_canvas.yview_moveto(1.0)

    def _on_support_send(self, event=None):
        user_msg = self.support_input.get().strip()
        if not user_msg:
            return

        self._insert_support_message(user_msg, is_user=True)
        self.support_input.delete(0, tk.END)

        bot_reply = get_response(user_msg, self.responses)
        
        # Delay the bot response slightly for a natural chat feel
        self.after(300, lambda: self._insert_support_message(bot_reply, is_user=False))
        save_chat(user_msg, bot_reply)

# ---------------------- RUN ---------------------- #

if __name__ == "__main__":
    app = CombinedChatbot()
    app.mainloop()


    