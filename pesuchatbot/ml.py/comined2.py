import os
import time
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext
from datetime import datetime
import random

# ---------------------- FILES & DEFAULT RESPONSES ---------------------- #

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

# ---------------------- EMOTION-AWARE RESPONSE LOGIC ---------------------- #

POSITIVE_RESPONSES = {
    "good": [
        "I'm really glad to hear you're feeling good! 😊",
        "That's nice to hear — keep enjoying your day! 🌱",
        "Happy to hear that! ✨"
    ],
    "fine": [
        "Good to know you're feeling fine. 🌼",
        "That sounds okay! Keep taking care of yourself. 💚"
    ],
    "great": [
        "That's wonderful! 💚",
        "Love that energy! 🌟"
    ],
    "okay": [
        "Alright! Remember to take care of yourself. 🌱",
        "Okay is good — keep going at your own pace. 💛"
    ],
    "alright": [
        "Good to know you're feeling alright. 🌼",
        "Alright — keep taking care of yourself. 💚"
    ],
    "better": [
        "I'm glad you're feeling better. ✨",
        "Nice to hear you're doing better — keep it up! 💛"
    ],
    "happy": [
        "That's beautiful! 😊",
        "Love to hear that you're feeling happy! 🌈"
    ],
}

NEGATIVE_RESPONSES = {
    "stress": [
        "It's okay to feel stressed. Take a deep breath and give yourself a moment to relax. 🌱",
        "Stress can feel heavy. Remember to be kind to yourself. 💛"
    ],
    "tired": [
        "You must be feeling exhausted. Rest is important — it's okay to slow down. ☁",
        "Feeling tired is natural after a busy day. Take care of yourself. 🌿"
    ],
    "anxiety": [
        "Anxiety can be overwhelming, but you're not alone. Focus on small calming steps and breathe deeply. 💚",
        "I understand anxiety can be tough. Be gentle with yourself. 💛"
    ],
    "lonely": [
        "Feeling lonely can be heavy. Remember you matter. 💛",
        "You are not alone — your feelings are valid. 💙"
    ],
    "exam": [
        "Exams can feel intense, but you're capable. Take one step at a time. 📘",
        "It's normal to feel pressure during exams. Doing your best is enough. 🌟"
    ],
    "sad": [
        "I'm sorry you're feeling sad. It's okay to take time for yourself. 💙",
        "Your feelings matter — treat yourself with care."
    ],
    "overwhelmed": [
        "That sounds like a lot to carry. Remember to breathe and take it slowly. 🌿",
        "You are doing your best, and it's okay to slow down."
    ],
    "confused": [
        "Feeling confused is natural sometimes. Give yourself patience. 💛",
        "It's okay to feel uncertain. Step by step is enough."
    ],
    "angry": [
        "It's okay to feel angry — your feelings are valid. 🔥",
        "Anger is natural. Care for yourself while experiencing it."
    ],
}

NEUTRAL_RESPONSES = {
    "hello": "Hey there! I'm glad you reached out. 🌼",
    "hi": "Hi! It's nice to hear from you. 💚",
    "hey": "Hey! I'm here with you. 🌼",
    "thanks": "You're welcome 🤍",
    "thank you": "You're welcome 🌱",
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

# ---------------------- COMBINED CHATBOT APPLICATION ---------------------- #

class CombinedChatbot(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🌿 PESU Support — Personal Analysis & Mental Health")
        self.geometry("850x750")
        self.configure(bg="#0a0f24")

        ensure_responses_file()
        self.responses = load_responses()

        self._build_ui()

    def _build_ui(self):
        # Main header
        header_frame = tk.Frame(self, bg="#1c2440", highlightbackground="#4c6eff",
                               highlightthickness=3)
        header_frame.pack(fill=tk.X, padx=15, pady=15)
        
        header_label = tk.Label(
            header_frame,
            text="🌙 PESU Support Center 🌙",
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

        # Tab 1: Personal Analysis
        self.analysis_frame = tk.Frame(self.notebook, bg="#1c2440")
        self.notebook.add(self.analysis_frame, text="🧘 Personal Analysis")
        self._build_analysis_tab()

        # Tab 2: Mental Health Support
        self.support_frame = tk.Frame(self.notebook, bg="#f0f4f7")
        self.notebook.add(self.support_frame, text="💚 Mental Health Support")
        self._build_support_tab()

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
            text="Submit",
            font=("Consolas", 12, "bold"),
            bg="#4458ff",
            fg="white",
            activebackground="#5a6dff",
            cursor="hand2",
            relief="flat",
            width=12
        )
        self.analysis_submit.pack(side=tk.RIGHT)

        # Start analysis program in thread
        self.user_input_value = None
        threading.Thread(target=self._run_analysis_program, daemon=True).start()

    def _build_support_tab(self):
        # Mental Health Support GUI
        chat_frame = tk.Frame(self.support_frame, bg="#f0f4f7")
        chat_frame.pack(padx=15, pady=15, fill=tk.BOTH, expand=True)

        self.support_canvas = tk.Canvas(chat_frame, bg="#f0f4f7", highlightthickness=0)
        self.support_scrollbar = ttk.Scrollbar(chat_frame, orient="vertical",
                                              command=self.support_canvas.yview)
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

    # ---------------------- PERSONAL ANALYSIS FUNCTIONS ---------------------- #

    def _analysis_print(self, text):
        self.analysis_text.config(state="normal")
        self.analysis_text.insert(tk.END, text)
        self.analysis_text.see(tk.END)
        self.analysis_text.config(state="disabled")
        self.update()

    def _slow_print(self, text, delay=0.04):
        for char in text:
            self._analysis_print(char)
            time.sleep(delay)
        self._analysis_print("\n")

    def _ask(self, question):
        self._slow_print(question)
        return self._get_analysis_input()

    def _get_analysis_input(self):
        self.user_input_value = None

        def submit():
            self.user_input_value = self.analysis_input.get()
            self.analysis_input.delete(0, tk.END)

        self.analysis_submit.config(command=submit)

        while self.user_input_value is None:
            self.update()
            time.sleep(0.05)

        return self.user_input_value

    def _run_analysis_program(self):
        self._slow_print("\nWelcome to the Inner Journey Program.")
        self._slow_print("A space to explore awareness, existence, surrender, and the void.\n")
        self._slow_print("Let's begin...\n")

        name = self._ask("Before we start, what shall I call you? ")

        self._slow_print(f"\nHello {name}. Let us explore the deeper layers of your existence.\n")

        q1 = self._ask(
            "Who do you believe you are:\n"
            "A) The body\n"
            "B) The mind\n"
            "C) The emotions\n"
            "D) The awareness\n\n"
            "Clue: Your answer must be permanent, everlasting, stable and constant.\n"
            "Choose A, B, C, or D: "
        )

        if q1.lower() == "d":
            self._slow_print("\nYou chose Awareness — the observer behind all experience.")
        else:
            self._slow_print("\nInteresting perspective. Let's go deeper.")

        self._slow_print("\nNow tell me in one word what you feel your true nature is.")
        nature = self._ask("Examples: peace, void, happiness, energy, silence: ")

        self._slow_print(f"\nYou feel your true nature is: {nature.upper()}. Beautiful.\n")

        self._slow_print("Here is a deeper reflection...")
        time.sleep(1.5)

        self._slow_print("\nIf you surrender everything — identity, thoughts, fears —")
        self._slow_print("what remains is often described as the VOID.")
        self._slow_print("But this void is not empty... it is full of infinite potential.\n")

        q2 = self._ask(
            "How does this void feel to you:\n"
            "A) Peaceful nothingness\n"
            "B) Powerful silence\n"
            "C) Spacious awareness\n"
            "D) Presence without identity\n"
            "E) All of the above\n\n"
            "Choose A, B, C, D, or E: "
        )

        self._slow_print("\nA profound choice.")

        self._slow_print("\n\nFinal Reflection:")
        self._slow_print("-----------------------------------------------")
        self._slow_print(f"{name}, you have explored:")
        self._slow_print(f" • Your identity as {nature}")
        self._slow_print(" • The awareness behind your thoughts")
        self._slow_print(" • The surrender into the void")
        self._slow_print("-----------------------------------------------")

        self._slow_print("\nRemember:")
        self._slow_print("The one who is watching all of this unfold...")
        self._slow_print("is not the mind, not the body, but pure awareness.\n")

        self._slow_print("Thank you for taking this inner journey.\n")
        self._slow_print("Goodbye, traveller of consciousness. 🌙\n")

    # ---------------------- MENTAL HEALTH SUPPORT FUNCTIONS ---------------------- #

    def _insert_support_message(self, msg, is_user=True):
        frame = tk.Frame(self.support_inner, bg="#f0f4f7")
        
        if is_user:
            bubble = tk.Label(
                frame,
                text=msg,
                wraplength=450,
                justify="left",
                font=("Segoe UI", 11),
                bg="#aed6f1",
                fg="#154360",
                padx=12,
                pady=10,
                anchor="w",
                bd=0,
                relief="flat"
            )
            bubble.pack(anchor="e", padx=10, pady=4)
            frame.pack(anchor="e", fill=tk.X)
        else:
            bubble = tk.Label(
                frame,
                text=msg,
                wraplength=450,
                justify="left",
                font=("Segoe UI", 11),
                bg="#d6eaf8",
                fg="#1b2631",
                padx=12,
                pady=10,
                anchor="w",
                bd=0,
                relief="flat"
            )
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
        self.after(300, lambda: self._insert_support_message(bot_reply, is_user=False))
        save_chat(user_msg, bot_reply)

# ---------------------- RUN ---------------------- #

if __name__ == "__main__":
    app = CombinedChatbot()
    app.mainloop()