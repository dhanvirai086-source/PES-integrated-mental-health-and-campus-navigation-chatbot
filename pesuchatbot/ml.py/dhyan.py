import os
import tkinter as tk
from tkinter import ttk
from datetime import datetime
import random

# ---------------------- FILES & DEFAULT RESPONSES ---------------------- #

RESPONSES_FILE = "responses.txt"
HISTORY_FILE = "chat_history.txt"

DEFAULT_RESPONSES = {
    "stress": "It's okay to feel stressed sometimes. Take a moment to breathe deeply and ground yourself. 🌱",
    "exam": "Exams can be challenging, but you’re capable of handling it. Take it one step at a time. ✨",
    "anxiety": "Anxiety can be tough, but you’re not alone. Focus on small calming steps. 💚",
    "sad": "It’s okay to feel sad sometimes. Be kind to yourself — you deserve care and rest. 💙",
    "hello": "Hey there! I’m glad you reached out. How are you feeling today? 🌼",
    "lonely": "Feeling lonely can be heavy. Remember you matter. 💫",
    "tired": "You must be feeling exhausted. Rest is important — it’s okay to slow down. ☁️",
    "bye": "Take care of yourself. You’re doing your best, and that’s enough. 🌷"
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
        "That’s nice to hear — keep enjoying your day! 🌱",
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
        "I’m glad you're feeling better. ✨",
        "Nice to hear you’re doing better — keep it up! 💛"
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
        "You must be feeling exhausted. Rest is important — it’s okay to slow down. ☁️",
        "Feeling tired is natural after a busy day. Take care of yourself. 🌿"
    ],
    "anxiety": [
        "Anxiety can be overwhelming, but you’re not alone. Focus on small calming steps and breathe deeply. 💚",
        "I understand anxiety can be tough. Be gentle with yourself. 💛"
    ],
    "lonely": [
        "Feeling lonely can be heavy. Remember you matter. 💛",
        "You are not alone — your feelings are valid. 💙"
    ],
    "exam": [
        "Exams can feel intense, but you’re capable. Take one step at a time. 📘",
        "It’s normal to feel pressure during exams. Doing your best is enough. 🌟"
    ],
    "sad": [
        "I’m sorry you’re feeling sad. It’s okay to take time for yourself. 💙",
        "Your feelings matter — treat yourself with care."
    ],
    "overwhelmed": [
        "That sounds like a lot to carry. Remember to breathe and take it slowly. 🌿",
        "You are doing your best, and it’s okay to slow down."
    ],
    "confused": [
        "Feeling confused is natural sometimes. Give yourself patience. 💛",
        "It’s okay to feel uncertain. Step by step is enough."
    ],
    "angry": [
        "It’s okay to feel angry — your feelings are valid. 🔥",
        "Anger is natural. Care for yourself while experiencing it."
    ],
}

NEUTRAL_RESPONSES = {
    "hello": "Hey there! I’m glad you reached out. 🌼",
    "hi": "Hi! It’s nice to hear from you. 💚",
    "hey": "Hey! I'm here with you. 🌼",
    "thanks": "You're welcome 🤍",
    "thank you": "You’re welcome 🌱",
    "bye": "Take care of yourself. You matter 🌷"
}

REFLECTIVE_FALLBACKS = [
    "I hear you. Would you like to tell me a little more? 💛",
    "That sounds important… I’m here to listen. 🌿",
    "I want to understand better — can you tell me more about that?",
    "You’re not alone. Take your time, I’m here. 💚"
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

# ---------------------- GUI ---------------------- #

class ModernChatbot(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🌿 PESU Support — Mental Health Companion")
        self.geometry("620x700")
        self.configure(bg="#f0f4f7")

        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        ensure_responses_file()
        self.responses = load_responses()

        self._build_ui()
        self._insert_bot_message("Hello! I’m your PESU Support companion 🌼 How are you feeling today?")

    def _build_ui(self):
        self.top_frame = tk.Frame(self, bg="#d6eaf8", height=70)
        self.top_frame.pack(fill=tk.X)
        self.title_lbl = tk.Label(
            self.top_frame,
            text="🌱 PESU Support — I'm here to listen",
            font=("Segoe UI Semibold", 14, "bold"),
            fg="#1b4f72",
            bg="#d6eaf8",
            pady=20
        )
        self.title_lbl.pack()

        self.chat_frame = tk.Frame(self, bg=self["bg"])
        self.chat_frame.pack(padx=20, pady=(10, 0), fill=tk.BOTH, expand=True)

        self.chat_canvas = tk.Canvas(self.chat_frame, bg=self["bg"], highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.chat_frame, orient="vertical", command=self.chat_canvas.yview)
        self.inner_frame = tk.Frame(self.chat_canvas, bg=self["bg"])

        self.inner_frame.bind("<Configure>", lambda e: self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all")))
        self.chat_canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        self.chat_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.chat_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.input_frame = tk.Frame(self, bg="#f0f4f7")
        self.input_frame.pack(fill=tk.X, padx=20, pady=10)

        self.user_input = tk.Entry(
            self.input_frame,
            font=("Segoe UI", 12),
            bg="white",
            fg="#154360",
            relief="flat"
        )
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=10, padx=(0, 10))
        self.user_input.bind("<Return>", self._on_send)

        self.send_btn = tk.Button(
            self.input_frame,
            text="Send ➤",
            command=self._on_send,
            font=("Segoe UI", 11, "bold"),
            bg="#5dade2",
            fg="white",
            activebackground="#3498db",
            activeforeground="white",
            relief="flat",
            width=10
        )
        self.send_btn.pack(side=tk.RIGHT)

    def _insert_user_message(self, msg):
        frame = tk.Frame(self.inner_frame, bg=self["bg"])
        bubble = tk.Label(
            frame,
            text=msg,
            wraplength=380,
            justify="left",
            font=("Segoe UI", 11),
            bg="#aed6f1",
            fg="#154360",
            padx=10, pady=8,
            anchor="w",
            bd=0,
            relief="flat"
        )
        bubble.pack(anchor="e", padx=10, pady=4)
        frame.pack(anchor="e", fill=tk.X)

    def _insert_bot_message(self, msg):
        frame = tk.Frame(self.inner_frame, bg=self["bg"])
        bubble = tk.Label(
            frame,
            text=msg,
            wraplength=380,
            justify="left",
            font=("Segoe UI", 11),
            bg="#d6eaf8",
            fg="#1b2631",
            padx=10, pady=8,
            anchor="w",
            bd=0,
            relief="flat"
        )
        bubble.pack(anchor="w", padx=10, pady=4)
        frame.pack(anchor="w", fill=tk.X)
        self.chat_canvas.update_idletasks()
        self.chat_canvas.yview_moveto(1.0)

    def _on_send(self, event=None):
        user_msg = self.user_input.get().strip()
        if not user_msg:
            return
        self._insert_user_message(user_msg)
        self.user_input.delete(0, tk.END)

        bot_reply = get_response(user_msg, self.responses)
        self.after(300, lambda: self._insert_bot_message(bot_reply))
        save_chat(user_msg, bot_reply)

# ---------------------- RUN ---------------------- #

if __name__ == "__main__":
    app = ModernChatbot()
    app.mainloop()