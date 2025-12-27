import os
import wx
import wx.lib.scrolledpanel as scrolled
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

CAMPUS_PLACES = {
    "Golden Jubilee Block (GJBC)": {"short": "Main academic block near the food court.", "directions": "Head southeast from the main courtyard."},
    "Hornbill Coffee": {"short": "Coffee shop on the east side of the GJBC.", "directions": "Walk east from GJBC across the open area."},
    "Central Library": {"short": "Central library located northwest of GJBC.", "directions": "Walk northwest from GJBC across the open area."},
    "GJB Food Court": {"short": "Food court next to Golden Jubilee Block.", "directions": "Walk east-southeast from the GJBC main entrance."},
    "A Block": {"short": "Central academic building with lecture halls.", "directions": "Find via main paths from the courtyard."},
    "Boys Hostel": {"short": "Student accommodation (boys).", "directions": "Located on the eastern side of campus."},
    "Cricket Field": {"short": "Sports field on the north side.", "directions": "Go north from central campus."}
}

POSITIVE_RESPONSES = {
    "good": ["I'm really glad to hear you're feeling good! 😊", "That's nice to hear — keep enjoying your day! 🌱"],
    "great": ["That's wonderful! 💚", "Love that energy! 🌟"],
    "happy": ["That's beautiful! 😊", "Love to hear that you're feeling happy! 🌈"],
}

NEGATIVE_RESPONSES = {
    "stress": ["It's okay to feel stressed. Take a deep breath and give yourself a moment to relax. 🌱"],
    "tired": ["You must be feeling exhausted. Rest is important — it's okay to slow down. ☁"],
    "anxiety": ["Anxiety can be overwhelming, but you're not alone. Focus on small calming steps and breathe deeply. 💚"],
    "sad": ["I'm sorry you're feeling sad. It's okay to take time for yourself. 💙"],
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
    "You're not alone. Take your time, I'm here. 💚"
]

ANALYSIS_QUESTIONS = [
    "What shall I call you?",
    "Who do you believe you are:\nA) The body\nB) The mind\nC) The emotions\nD) The awareness\n\nChoose A, B, C, or D: ",
    "Now tell me in one word what you feel your true nature is. Examples: peace, void, happiness, energy, silence: ",
    "How does this void feel to you:\nA) Peaceful nothingness\nB) Powerful silence\nC) Spacious awareness\nD) Presence without identity\nE) All of the above\n\nChoose A, B, C, D, or E: "
]

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
        f.write(f"{now} User: {user}\n{now} Bot: {bot}\n\n")

def timestamp():
    return datetime.now().strftime("%H:%M")

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
class CombinedChatbot(wx.Frame):
    def __init__(self):
        super()._init_(None, title="🚀 PESU Integrated Support System", size=(850, 750))
        self.SetBackgroundColour(wx.Colour(10, 15, 36))
        ensure_responses_file()
        self.responses = load_responses()
        
        # Analysis state
        self.analysis_stage = 0
        self.analysis_data = {}
        
        self._build_ui()
        self.Centre()

    def _build_ui(self):
        main_panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Header
        header_panel = wx.Panel(main_panel)
        header_panel.SetBackgroundColour(wx.Colour(28, 36, 64))
        header_sizer = wx.BoxSizer(wx.VERTICAL)
        header_label = wx.StaticText(header_panel, label="🚀 PESU Support Center 🌙")
        header_font = wx.Font(22, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        header_label.SetFont(header_font)
        header_label.SetForegroundColour(wx.Colour(143, 170, 255))
        header_sizer.Add(header_label, 0, wx.ALL | wx.CENTER, 10)
        header_panel.SetSizer(header_sizer)
        main_sizer.Add(header_panel, 0, wx.EXPAND | wx.ALL, 15)

        # Notebook
        self.notebook = wx.Notebook(main_panel)

        # Tab 1: Campus Assistant
        self.campus_panel = wx.Panel(self.notebook)
        self.campus_panel.SetBackgroundColour(wx.Colour(11, 18, 32))
        self.notebook.AddPage(self.campus_panel, "🗺️ Campus Assistant")
        self._build_campus_tab()

        # Tab 2: Unified Wellness & Analysis
        self.wellness_panel = wx.Panel(self.notebook)
        self.wellness_panel.SetBackgroundColour(wx.Colour(240, 244, 247))
        self.notebook.AddPage(self.wellness_panel, "💚 Wellness & Inner Journey")
        self._build_wellness_tab()

        main_sizer.Add(self.notebook, 1, wx.EXPAND | wx.ALL, 15)
        main_panel.SetSizer(main_sizer)

    # ==================================================================== 
    # --- TAB 1: CAMPUS ASSISTANT (UNCHANGED) ---
    # ==================================================================== 
    def _build_campus_tab(self):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # Left Panel: Places List
        left_panel = wx.Panel(self.campus_panel)
        left_panel.SetBackgroundColour(wx.Colour(15, 23, 36))
        left_sizer = wx.BoxSizer(wx.VERTICAL)
        places_label = wx.StaticText(left_panel, label="Places")
        places_label.SetForegroundColour(wx.Colour(230, 238, 246))
        left_sizer.Add(places_label, 0, wx.ALL, 10)
        
        self.places_scroll = scrolled.ScrolledPanel(left_panel, size=(250, -1))
        self.places_scroll.SetBackgroundColour(wx.Colour(15, 23, 36))
        places_scroll_sizer = wx.BoxSizer(wx.VERTICAL)
        
        for place_name in CAMPUS_PLACES.keys():
            btn = wx.Button(self.places_scroll, label=place_name, size=(230, -1))
            btn.SetBackgroundColour(wx.Colour(8, 50, 58))
            btn.SetForegroundColour(wx.Colour(230, 238, 246))
            btn.Bind(wx.EVT_BUTTON, lambda evt, name=place_name: self._on_campus_place_click(name))
            places_scroll_sizer.Add(btn, 0, wx.ALL, 6)
        
        self.places_scroll.SetSizer(places_scroll_sizer)
        self.places_scroll.SetupScrolling()
        left_sizer.Add(self.places_scroll, 1, wx.EXPAND | wx.ALL, 5)
        left_panel.SetSizer(left_sizer)
        sizer.Add(left_panel, 0, wx.EXPAND | wx.ALL, 10)
        
        # Center Panel: Chat
        center_panel = wx.Panel(self.campus_panel)
        center_panel.SetBackgroundColour(wx.Colour(15, 23, 36))
        center_sizer = wx.BoxSizer(wx.VERTICAL)
        chat_label = wx.StaticText(center_panel, label="Campus Chat")
        chat_label.SetForegroundColour(wx.Colour(230, 238, 246))
        center_sizer.Add(chat_label, 0, wx.ALL, 10)
        
        self.campus_chatbox = wx.TextCtrl(center_panel, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2)
        self.campus_chatbox.SetBackgroundColour(wx.Colour(7, 24, 33))
        self.campus_chatbox.SetForegroundColour(wx.Colour(230, 238, 246))
        self.campus_chatbox.AppendText("Bot: Hi — I'm the PESU Campus assistant. Click a place or type a question.\n\n")
        center_sizer.Add(self.campus_chatbox, 1, wx.EXPAND | wx.ALL, 10)
        
        # Input
        input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.campus_input = wx.TextCtrl(center_panel, style=wx.TE_PROCESS_ENTER)
        self.campus_input.SetBackgroundColour(wx.Colour(7, 26, 29))
        self.campus_input.SetForegroundColour(wx.Colour(230, 238, 246))
        self.campus_input.Bind(wx.EVT_TEXT_ENTER, lambda evt: self._on_campus_send())
        input_sizer.Add(self.campus_input, 1, wx.ALL, 5)
        
        send_btn = wx.Button(center_panel, label="Send")
        send_btn.SetBackgroundColour(wx.Colour(6, 182, 212))
        send_btn.SetForegroundColour(wx.Colour(11, 18, 32))
        send_btn.Bind(wx.EVT_BUTTON, lambda evt: self._on_campus_send())
        input_sizer.Add(send_btn, 0, wx.ALL, 5)
        
        center_sizer.Add(input_sizer, 0, wx.EXPAND)
        center_panel.SetSizer(center_sizer)
        sizer.Add(center_panel, 1, wx.EXPAND | wx.ALL, 10)
        
        self.campus_panel.SetSizer(sizer)

    def _on_campus_place_click(self, key):
        info = CAMPUS_PLACES.get(key, {})
        text = f"{key}\n\n{info.get('short','No short info')}\n\nDirections: {info.get('directions','No directions available')}"
        self._append_campus_user(f"Where is {key}?")
        self._append_campus_bot(text)

    def _on_campus_send(self):
        q = self.campus_input.GetValue().strip()
        if not q:
            return
        self._append_campus_user(q)
        self.campus_input.Clear()
        resp = self._generate_campus_response(q)
        self._append_campus_bot(resp)

    def _generate_campus_response(self, q):
        q_l = q.lower()
        for key in CAMPUS_PLACES.keys():
            if key.lower() == q_l or key.lower() in q_l or any(word in q_l.split() for word in key.lower().split()):
                info = CAMPUS_PLACES[key]
                return f"{key}\n\n{info.get('short','')}\n\nDirections: {info.get('directions','')}"
        if "list" in q_l or "places" in q_l:
            return "Places:\n" + "\n".join(f"- {k}" for k in CAMPUS_PLACES.keys())
        if "gjbc" in q_l or "golden" in q_l:
            key = "Golden Jubilee Block (GJBC)"
            info = CAMPUS_PLACES.get(key)
            if info:
                return f"{key}\n\n{info['short']}\n\nDirections: {info['directions']}"
        return "Sorry — I don't have an exact answer. Try clicking a place button or asking for a list."

    def _append_campus_user(self, text):
        self.campus_chatbox.SetDefaultStyle(wx.TextAttr(wx.Colour(165, 214, 167)))
        self.campus_chatbox.AppendText(f"You: {text}\n")
        self.campus_chatbox.SetDefaultStyle(wx.TextAttr(wx.Colour(148, 163, 184)))
        self.campus_chatbox.AppendText(f"{timestamp()}\n\n")

    def _append_campus_bot(self, text):
        self.campus_chatbox.SetDefaultStyle(wx.TextAttr(wx.Colour(145, 229, 246)))
        lines = text.splitlines()
        for i, line in enumerate(lines):
            prefix = "Bot: " if i == 0 else "     "
            self.campus_chatbox.AppendText(f"{prefix}{line}\n")
        self.campus_chatbox.SetDefaultStyle(wx.TextAttr(wx.Colour(148, 163, 184)))
        self.campus_chatbox.AppendText(f"{timestamp()}\n\n")

    # ==================================================================== 
    # --- TAB 2: UNIFIED WELLNESS & INNER JOURNEY ---
    # ==================================================================== 
    def _build_wellness_tab(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Mode selector
        mode_panel = wx.Panel(self.wellness_panel)
        mode_panel.SetBackgroundColour(wx.Colour(230, 240, 250))
        mode_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.mode_support = wx.Button(mode_panel, label="💚 Mental Health Support")
        self.mode_support.SetBackgroundColour(wx.Colour(93, 173, 226))
        self.mode_support.SetForegroundColour(wx.Colour(255, 255, 255))
        self.mode_support.Bind(wx.EVT_BUTTON, lambda evt: self._switch_mode("support"))
        
        self.mode_analysis = wx.Button(mode_panel, label="🧘 Inner Journey")
        self.mode_analysis.SetBackgroundColour(wx.Colour(155, 155, 155))
        self.mode_analysis.SetForegroundColour(wx.Colour(255, 255, 255))
        self.mode_analysis.Bind(wx.EVT_BUTTON, lambda evt: self._switch_mode("analysis"))
        
        mode_sizer.Add(self.mode_support, 1, wx.ALL, 5)
        mode_sizer.Add(self.mode_analysis, 1, wx.ALL, 5)
        mode_panel.SetSizer(mode_sizer)
        sizer.Add(mode_panel, 0, wx.EXPAND | wx.ALL, 10)
        
        # Chat display
        self.wellness_scroll = scrolled.ScrolledPanel(self.wellness_panel)
        self.wellness_scroll.SetBackgroundColour(wx.Colour(240, 244, 247))
        self.wellness_scroll_sizer = wx.BoxSizer(wx.VERTICAL)
        self.wellness_scroll.SetSizer(self.wellness_scroll_sizer)
        sizer.Add(self.wellness_scroll, 1, wx.EXPAND | wx.ALL, 15)
        
        # Input area
        input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.wellness_input = wx.TextCtrl(self.wellness_panel, style=wx.TE_PROCESS_ENTER)
        self.wellness_input.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.wellness_input.SetForegroundColour(wx.Colour(21, 67, 96))
        self.wellness_input.Bind(wx.EVT_TEXT_ENTER, lambda evt: self._on_wellness_send())
        input_sizer.Add(self.wellness_input, 1, wx.ALL, 5)
        
        self.wellness_btn = wx.Button(self.wellness_panel, label="Send ➤")
        self.wellness_btn.SetBackgroundColour(wx.Colour(93, 173, 226))
        self.wellness_btn.SetForegroundColour(wx.Colour(255, 255, 255))
        self.wellness_btn.Bind(wx.EVT_BUTTON, lambda evt: self._on_wellness_send())
        input_sizer.Add(self.wellness_btn, 0, wx.ALL, 5)
        
        sizer.Add(input_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 15)
        self.wellness_panel.SetSizer(sizer)
        
        # Default mode
        self.current_mode = "support"
        self._insert_wellness_message("Hello! I'm your PESU Wellness companion 🌼 How are you feeling today?", False)

    def _switch_mode(self, mode):
        self.current_mode = mode
        self.wellness_scroll_sizer.Clear(True)
        
        if mode == "support":
            self.mode_support.SetBackgroundColour(wx.Colour(93, 173, 226))
            self.mode_analysis.SetBackgroundColour(wx.Colour(155, 155, 155))
            self.wellness_btn.SetLabel("Send ➤")
            self._insert_wellness_message("Mental Health Support Mode 💚\nHow are you feeling today?", False)
        else:
            self.mode_support.SetBackgroundColour(wx.Colour(155, 155, 155))
            self.mode_analysis.SetBackgroundColour(wx.Colour(93, 173, 226))
            self.wellness_btn.SetLabel("Start Journey")
            self.analysis_stage = 0
            self.analysis_data = {}
            self._insert_wellness_message("Inner Journey Program 🧘\nClick 'Start Journey' to begin exploring awareness and consciousness.", False)

    def _insert_wellness_message(self, msg, is_user=True):
        bubble = wx.StaticText(self.wellness_scroll, label=msg)
        bubble.Wrap(450)
        
        if is_user:
            bubble.SetBackgroundColour(wx.Colour(174, 214, 241))
            bubble.SetForegroundColour(wx.Colour(21, 67, 96))
            self.wellness_scroll_sizer.Add(bubble, 0, wx.ALIGN_RIGHT | wx.ALL, 10)
        else:
            bubble.SetBackgroundColour(wx.Colour(214, 234, 248))
            bubble.SetForegroundColour(wx.Colour(27, 38, 49))
            self.wellness_scroll_sizer.Add(bubble, 0, wx.ALIGN_LEFT | wx.ALL, 10)
        
        self.wellness_scroll.SetupScrolling(scrollToTop=False)
        self.wellness_scroll.Layout()

    def _on_wellness_send(self):
        if self.current_mode == "support":
            self._handle_support_mode()
        else:
            self._handle_analysis_mode()

    def _handle_support_mode(self):
        user_msg = self.wellness_input.GetValue().strip()
        if not user_msg:
            return
        
        self._insert_wellness_message(user_msg, True)
        self.wellness_input.Clear()
        
        bot_reply = get_response(user_msg, self.responses)
        wx.CallLater(300, lambda: self._insert_wellness_message(bot_reply, False))
        save_chat(user_msg, bot_reply)

    def _handle_analysis_mode(self):
        user_input = self.wellness_input.GetValue().strip()
        
        if self.analysis_stage == 0 and self.wellness_btn.GetLabel() == "Start Journey":
            self.wellness_btn.SetLabel("Submit")
            self._insert_wellness_message("Welcome to the Inner Journey. Let's begin...", False)
            wx.CallLater(500, self._next_analysis_question)
            return
        
        if not user_input:
            return
        
        self._insert_wellness_message(user_input, True)
        self.wellness_input.Clear()
        
        # Store answer
        if self.analysis_stage == 0:
            self.analysis_data['name'] = user_input
        elif self.analysis_stage == 1:
            self.analysis_data['who'] = user_input
        elif self.analysis_stage == 2:
            self.analysis_data['nature'] = user_input
        elif self.analysis_stage == 3:
            self.analysis_data['void'] = user_input
        
        self.analysis_stage += 1
        
        if self.analysis_stage < len(ANALYSIS_QUESTIONS):
            wx.CallLater(500, self._next_analysis_question)
        else:
            wx.CallLater(500, self._show_analysis_summary)

    def _next_analysis_question(self):
        if self.analysis_stage < len(ANALYSIS_QUESTIONS):
            question = ANALYSIS_QUESTIONS[self.analysis_stage]
            self._insert_wellness_message(f"[{self.analysis_stage+1}] {question}", False)

    def _show_analysis_summary(self):
        name = self.analysis_data.get('name', 'Traveller')
        who = self.analysis_data.get('who', 'not given')
        nature = self.analysis_data.get('nature', 'undefined')
        
        summary = f"""Analysis Complete for {name}

Your Exploration:
- Primary belief of self: {who.upper()}
- True nature: {nature.upper()}

"""
        if who.lower() == 'd' or 'awareness' in who.lower():
            summary += "This aligns with pure awareness. 🌙\n"
        
        summary += "\nThank you for this inner journey, traveller of consciousness."
        
        self._insert_wellness_message(summary, False)
        self.wellness_btn.SetLabel("Start Journey")
        self.analysis_stage = 0
        self.analysis_data = {}

# ---------------------- RUN ----------------------
if __name__ == "_main_":
    app = wx.App()
    frame = CombinedChatbot()
    frame.Show()
    app.MainLoop()