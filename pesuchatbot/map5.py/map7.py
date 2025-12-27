"""
PESU GJBC Chatbot - Dark themed Tkinter GUI (single Python file)

- Put a map image named 'gjbc_map.png' in the same folder if you want the map displayed.
- Requires Pillow (optional) for image display: pip install pillow
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from difflib import get_close_matches
import os

# Try to import PIL for image support (optional)
try:
    from PIL import Image, ImageTk
    HAVE_PIL = True
except Exception:
    HAVE_PIL = False

# ---------- Configuration ----------
MAP_PATH = "gjbc_map.png"   # change filename if your map file has another name

# Dark theme colors
BG = "#0b1220"
CARD = "#0f1724"
TEXT = "#E6EEF6"
MUTED = "#9AA9B2"
ACCENT = "#06b6d4"
BTN = "#085f66"
BTN_HOVER = "#0ea5a4"

# ---------- Knowledge base: combined info from your inputs ----------
KB = {
    # GJBC crop POIs (from earlier)
    "golden jubilee block": {
        "label": "Golden Jubilee Block (GJBC)",
        "short": "Main academic block near the food court (southeast area of the crop).",
        "directions": "From the main courtyard, head southeast to reach GJBC. Food court and GJB basketball court are nearby."
    },
    "hornbill coffee": {
        "label": "Hornbill Coffee",
        "short": "Coffee shop on the east side of the GJBC crop.",
        "directions": "From GJBC, walk east across the open area; Hornbill Coffee is on the right."
    },
    "pesu gym": {
        "label": "PESU Gym",
        "short": "Gym near the north/top-center of the map.",
        "directions": "Head north from Golden Jubilee Block across the courtyard."
    },
    "central library": {
        "label": "PES University Central Library",
        "short": "Central library located northwest of GJBC.",
        "directions": "From GJBC walk northwest across the open area to reach the library building."
    },
    "mechanical block": {
        "label": "Mechanical (C) Block",
        "short": "Central landmark in the crop.",
        "directions": "From GJBC head slightly northwest to find the Mechanical block."
    },
    "badminton court": {
        "label": "PES Badminton Court",
        "short": "Badminton courts to the northeast of Mechanical block.",
        "directions": "From GJBC go northeast across the courtyard to reach badminton courts."
    },
    "basketball court": {
        "label": "PES GJB Basketball Court",
        "short": "Basketball court just below (south of) GJBC.",
        "directions": "From GJBC exit south to reach the basketball court."
    },
    "food court": {
        "label": "PESU GJB Food Court",
        "short": "Food court next to Golden Jubilee Block (east/southeast).",
        "directions": "From the GJBC main entrance, walk east/southeast to the food court."
    },
    "jv technosoft": {
        "label": "JV Technosoft Pvt",
        "short": "Tech office located southwest in the crop (temporarily closed as per listing).",
        "directions": "Located southwest of the Central Library area."
    },

    # Places from the stylized campus image you uploaded
    "front gate": {"label":"Front Gate","short":"Main entrance at the south side of campus.","directions":"Enter campus through front gate."},
    "scooter parking": {"label":"Scooter Parking","short":"Two-wheeler parking near front entrance.","directions":"Park scooters near the front gate area."},
    "car parking": {"label":"Car Parking","short":"Four-wheeler parking in the north zone.","directions":"Drive to the north-most parking lot."},
    "student lounge": {"label":"Student Lounge","short":"Relaxation zone near central campus.","directions":"Near A Block and central pathways."},
    "m block": {"label":"M Block","short":"Academic block in southern region.","directions":"Located near the south side, close to front gate."},
    "a block": {"label":"A Block","short":"Central academic building with lecture halls.","directions":"Central area - find via main paths from the courtyard."},
    "f block": {"label":"F Block","short":"Activity & events area; sports nearby.","directions":"Toward the northwest region of the campus image."},
    "tech park": {"label":"Tech Park","short":"Centre for industry partnerships and labs.","directions":"Near library and central academic blocks."},
    "library (campus)": {"label":"Library","short":"Central library (campus).","directions":"Near A Block and Tech Park."},
    "boys hostel": {"label":"Boys Hostel","short":"Boys accommodation in the east area.","directions":"Follow east-side pathways from central area."},
    "girls hostel": {"label":"Girls Hostel","short":"Girls accommodation in the west area.","directions":"Located near the western clusters of blocks."},
    "cricket field": {"label":"Cricket Field","short":"Large sports field on the north side.","directions":"Go north from central campus to reach the cricket field."},
    "event ground": {"label":"Event Ground","short":"Open space used for ceremonies/events.","directions":"Central open area near the student lounge."}
}

# Keep canonical names list for matching/display
PLACE_KEYS = list(KB.keys())

# ---------- Hotspot coordinates (percent relative to displayed image) ----------
# These are approximate and match earlier hot-spot positions for the crop.
HOTSPOTS = {
    "golden jubilee block": (74, 68),
    "hornbill coffee": (85, 60),
    "central library": (30, 18),
    "pesu gym": (46, 6),
    "mechanical block": (50, 38),
    "badminton court": (62, 28),
    "basketball court": (74, 80),
    "food court": (80, 72),
    "jv technosoft": (22, 76)
}

# ---------- Chat logic ----------
def find_best_match(query):
    """Return best matching KB key for a query (simple fuzzy using difflib)."""
    q = query.lower().strip()
    if not q:
        return None
    # direct substring preference
    for k in PLACE_KEYS:
        if k in q:
            return k
    # try close matches on keys and labels
    search_pool = PLACE_KEYS + [KB[k]['label'].lower() for k in PLACE_KEYS]
    matches = get_close_matches(q, search_pool, n=1, cutoff=0.5)
    if matches:
        m = matches[0]
        # find which key corresponds
        for k in PLACE_KEYS:
            if m == k or m == KB[k]['label'].lower():
                return k
    return None

def answer_text(query):
    k = find_best_match(query)
    if k:
        info = KB[k]
        return f"{info['label']}\n\n{info['short']}\n\nDirections: {info.get('directions','')}"
    # handle "from GJBC" style questions
    q = query.lower()
    if "from gjb" in q or "from gjbc" in q or "from golden" in q:
        # try to find destination
        for key in PLACE_KEYS:
            if key in q and key != "golden jubilee block":
                return KB[key].get('directions', KB[key]['short'])
        return "From GJBC, move to the main courtyard and follow the map landmarks: library (NW), gym (N), food court (E)."
    if "list" in q or "places" in q:
        return "Places we know:\n" + ", ".join([KB[k]['label'] for k in PLACE_KEYS])
    return "Sorry — I don't have a precise answer. Try 'Where is the library?' or click a place button."

# ---------- Tkinter UI ----------
class PESUApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PESU GJBC Assistant — Dark")
        self.configure(bg=BG)
        self.geometry("1100x700")
        self.minsize(900, 600)
        self._setup_styles()
        self._build_layout()
        self._load_map()
        self._draw_hotspots()

    def _setup_styles(self):
        style = ttk.Style(self)
        # Use default theme but override colors via widget options where possible
        style.configure("Card.TFrame", background=CARD)
        style.configure("TLabel", background=CARD, foreground=TEXT)
        style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"), background=BG, foreground=TEXT)
        style.configure("Small.TLabel", font=("Segoe UI", 10), background=CARD, foreground=MUTED)
        style.configure("Accent.TButton", background=ACCENT, foreground=BG)
        # we will still manually color many widgets for consistent dark look

    def _build_layout(self):
        # Top header
        header = ttk.Label(self, text="PESU GJBC Assistant", style="Header.TLabel")
        header.place(x=20, y=12)

        # Left frame: MAP
        self.left = ttk.Frame(self, style="Card.TFrame")
        self.left.place(x=20, y=60, width=640, height=520)
        # title
        lbl_map = tk.Label(self.left, text="Campus Map (GJBC area)", bg=CARD, fg=TEXT, font=("Segoe UI", 12, "bold"))
        lbl_map.pack(anchor="nw", pady=(8,0), padx=10)

        # Canvas for map
        self.canvas = tk.Canvas(self.left, bg="#081022", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)
        # bind click on canvas to show nearest hotspot if clicked
        self.canvas.bind("<Button-1>", self._on_map_click)

        # Right frame: Chat and list
        self.right = ttk.Frame(self, style="Card.TFrame")
        self.right.place(x=680, y=60, width=400, height=520)

        # Chat area (scrolled text)
        chat_label = tk.Label(self.right, text="Chat", bg=CARD, fg=TEXT, font=("Segoe UI", 12, "bold"))
        chat_label.pack(anchor="nw", pady=(8,0), padx=10)

        self.chatbox = scrolledtext.ScrolledText(self.right, wrap=tk.WORD, bg="#06101A", fg=TEXT,
                                                 insertbackground=TEXT, font=("Segoe UI", 11))
        self.chatbox.pack(fill="both", expand=False, padx=10, pady=(4,6), ipady=6)
        self.chatbox.configure(height=15)
        self.chatbox.insert(tk.END, "Bot: Hi — I'm the PESU GJBC assistant. Click markers or ask questions.\n\n")
        self.chatbox.configure(state=tk.DISABLED)

        # Input row
        input_frame = tk.Frame(self.right, bg=CARD)
        input_frame.pack(fill="x", padx=10, pady=6)
        self.entry = tk.Entry(input_frame, bg="#071525", fg=TEXT, insertbackground=TEXT, font=("Segoe UI", 11))
        self.entry.pack(side="left", fill="x", expand=True, padx=(0,8))
        self.entry.bind("<Return>", lambda e: self._on_send())

        send_btn = tk.Button(input_frame, text="Send", bg=BTN, fg=TEXT, relief=tk.FLAT, command=self._on_send)
        send_btn.pack(side="right")

        # Places quick list
        list_label = tk.Label(self.right, text="Places", bg=CARD, fg=TEXT, font=("Segoe UI", 12, "bold"))
        list_label.pack(anchor="nw", pady=(8,0), padx=10)
        self.places_frame = tk.Frame(self.right, bg=CARD)
        self.places_frame.pack(fill="both", expand=False, padx=10, pady=6)

        self._populate_places()

        # Footer / small help
        help_lbl = tk.Label(self, text="Tip: Click a marker on the map, or type 'list places' / 'where is library?'", bg=BG, fg=MUTED, font=("Segoe UI", 9))
        help_lbl.place(x=20, y=590)

    def _populate_places(self):
        # create vertical buttons (two columns)
        keys = list(KB.keys())
        # create two-column grid
        for w in self.places_frame.winfo_children():
            w.destroy()
        r = 0
        c = 0
        for i, k in enumerate(keys):
            text = KB[k]['label']
            b = tk.Button(self.places_frame, text=text, bg="#0b1b22", fg=TEXT, width=24, anchor="w",
                          command=lambda key=k: self._on_place_click(key))
            b.grid(row=r, column=c, padx=4, pady=4, sticky="w")
            c += 1
            if c > 1:
                c = 0
                r += 1

    def _load_map(self):
        # load image if available; else show placeholder rectangle
        self.map_img = None
        if HAVE_PIL and os.path.exists(MAP_PATH):
            try:
                im = Image.open(MAP_PATH)
                # Resize image to fit canvas size later dynamically; store original for drawing
                self.orig_image = im.copy()
                self._render_map_image(im)
            except Exception as e:
                print("Error loading map image:", e)
                self._draw_placeholder()
        else:
            self._draw_placeholder()
    def _draw_placeholder(self):
        self.canvas.delete("all")
        w = self.canvas.winfo_width() or 640
        h = self.canvas.winfo_height() or 420
        self.canvas.create_rectangle(0, 0, w, h, fill="#06101A", outline="")
        self.canvas.create_text(w//2, h//2, text="Map image not found.\nPlace 'gjbc_map.png' next to this script.", fill=MUTED, font=("Segoe UI", 12), justify="center")
        self.displayed_size = (w, h)

    def _draw_hotspots(self):
        # Draw markers according to HOTSPOTS (percentage positions)
        self.canvas.delete("hotspot")
        w, h = self.displayed_size
        # compute top-left of the displayed image on canvas so percent positions match image area
        # If we used a resized image centered, find its bounding box:
        # For simplicity, assume image centered in canvas; compute offset
        c_w = self.canvas.winfo_width() or w
        c_h = self.canvas.winfo_height() or h
        img_w, img_h = self.displayed_size
        offset_x = (c_w - img_w) // 2
        offset_y = (c_h - img_h) // 2

        for key, (px, py) in HOTSPOTS.items():
            x = offset_x + int(img_w * px / 100)
            y = offset_y + int(img_h * py / 100)
            # draw small circle with tag 'hotspot'
            r = 9
            oval = self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=ACCENT, outline="#081018", width=2, tags=("hotspot", key))
            # small label
            self.canvas.tag_bind(oval, "<Enter>", lambda e, k=key: self._show_tooltip(k, e.x, e.y))
            self.canvas.tag_bind(oval, "<Leave>", lambda e: self._hide_tooltip())
            self.canvas.tag_bind(oval, "<Button-1>", lambda e, k=key: self._on_place_click(k))

    def _on_map_click(self, event):
        # If user clicks, check nearest hotspot within threshold
        x, y = event.x, event.y
        closest = None
        min_d = 9999
        # compute positions as in _draw_hotspots
        c_w = self.canvas.winfo_width() or self.displayed_size[0]
        c_h = self.canvas.winfo_height() or self.displayed_size[1]
        img_w, img_h = self.displayed_size
        offset_x = (c_w - img_w) // 2
        offset_y = (c_h - img_h) // 2
        for key, (px, py) in HOTSPOTS.items():
            hx = offset_x + int(img_w * px / 100)
            hy = offset_y + int(img_h * py / 100)
            d = (hx - x) ** 2 + (hy - y) ** 2
            if d < min_d:
                min_d = d
                closest = key
        # threshold: within ~25px
        if min_d <= 25 ** 2 and closest:
            self._on_place_click(closest)

    def _on_place_click(self, key):
        info = KB.get(key)
        if not info:
            messagebox.showinfo("Info", "Place info not found.")
            return
        text = f"{info['label']}\n\n{info['short']}\n\nDirections: {info.get('directions','')}"
        self._append_chat("You", f"Where is {info['label']}?")
        self._append_chat("Bot", text)

    def _append_chat(self, who, text):
        self.chatbox.configure(state=tk.NORMAL)
        if who == "You":
            self.chatbox.insert(tk.END, f"You: {text}\n")
        else:
            self.chatbox.insert(tk.END, f"Bot: {text}\n\n")
        self.chatbox.see(tk.END)
        self.chatbox.configure(state=tk.DISABLED)

    def _on_send(self):
        q = self.entry.get().strip()
        if not q:
            return
        self._append_chat("You", q)
        self.entry.delete(0, tk.END)
        # answer
        ans = answer_text(q)
        self._append_chat("Bot", ans)

    def _show_tooltip(self, key, x, y):
        # simple tooltip display near cursor inside canvas
        info = KB.get(key)
        if not info:
            return
        self._hide_tooltip()
        text = info['label']
        self.tooltip = self.canvas.create_text(x + 12, y - 12, text=text, anchor="nw", fill=TEXT, font=("Segoe UI", 10, "bold"), tags="tooltip",
                                               justify="left")
    def _hide_tooltip(self):
        self.canvas.delete("tooltip")

    def run(self):
        # redraw hotspots after window layout established
        self.after(200, self._redraw_after_resize)
        self.mainloop()

    def _redraw_after_resize(self):
        # Re-render image to fit current canvas size (if PIL exists)
        if HAVE_PIL and os.path.exists(MAP_PATH):
            try:
                im = self.orig_image.copy()
                # compute canvas size
                c_w = self.canvas.winfo_width() or 640
                c_h = self.canvas.winfo_height() or 420
                im.thumbnail((c_w, c_h), Image.ANTIALIAS)
                self.map_img = ImageTk.PhotoImage(im)
                self.canvas.delete("all")
                self.canvas.create_image((self.canvas.winfo_width()//2, self.canvas.winfo_height()//2), image=self.map_img, anchor="center", tags=("map"))
                self.displayed_size = (im.width, im.height)
            except Exception:
                self._draw_placeholder()
        # redraw hotspots
        self._draw_hotspots()
        # schedule again to handle manual resize
        self.after(500, self._redraw_after_resize)


if __name__ == "__main__":
    app = PESUApp()
    app.run()