from flask import Flask, request, jsonify, render_template_string, send_file, abort
import os, re, datetime

# optional fuzzy library
try:
    from rapidfuzz import process, fuzz
    HAVE_RAPIDFUZZ = True
except Exception:
    HAVE_RAPIDFUZZ = False

app = Flask(__name__)

# --- MAP PATH ---
# Current session image path (change to local filename like "gjbc_map.png" if you placed the image next to app.py)
MAP_PATH = "/mnt/data/8b3b1ee7-3924-47bd-b940-050213295fd9.png"

# --- Knowledge base ---
KB = {
    "golden jubilee block": {
        "short": "Golden Jubilee Block (GJBC) — main academic block in the southeast of the crop.",
        "directions_from_gjbc": "You're at GJBC. Use the main entrance to find nearby POIs: food court (E), basketball (S)."
    },
    "hornbill coffee": {
        "short": "Hornbill Coffee — east side near the food court.",
        "directions_from_gjbc": "From GJBC, walk east toward the food court and Hornbill Coffee."
    },
    "central library": {
        "short": "Central Library — northwest of the GJBC block.",
        "directions_from_gjbc": "Walk northwest across the courtyard to reach the library building."
    },
    "pesu gym": {
        "short": "PESU Gym — north / top-center on the crop.",
        "directions_from_gjbc": "Head north from GJBC across the courtyard to reach the gym."
    },
    "mechanical block": {
        "short": "Mechanical (C) Block — central landmark in the map.",
        "directions_from_gjbc": "From GJBC go slightly northwest to locate the Mechanical block."
    },
    "badminton court": {
        "short": "Badminton Court — northeast of Mechanical block.",
        "directions_from_gjbc": "From GJBC walk northeast across the open area to reach the badminton courts."
    },
    "basketball court": {
        "short": "Basketball Court — just south of GJBC.",
        "directions_from_gjbc": "Exit GJBC and walk south a short distance to find the basketball court."
    },
    "food court": {
        "short": "GJB Food Court — east/southeast of GJBC, near Hornbill Coffee.",
        "directions_from_gjbc": "From the main GJBC entrance, walk east-southeast to find the food court."
    }
}

# Hotspots (percent positions relative to the displayed image)
HOTSPOTS = [
    {"id": "golden jubilee block", "left": 74, "top": 68},
    {"id": "hornbill coffee", "left": 85, "top": 60},
    {"id": "central library", "left": 30, "top": 18},
    {"id": "pesu gym", "left": 46, "top": 6},
    {"id": "mechanical block", "left": 50, "top": 38},
    {"id": "badminton court", "left": 62, "top": 28},
    {"id": "basketball court", "left": 74, "top": 80},
    {"id": "food court", "left": 80, "top": 72}
]

# ---------------- helpers ----------------
def normalize(text):
    t = text.lower().strip()
    t = re.sub(r"[^\w\s]", " ", t)
    t = re.sub(r"\s+", " ", t)
    return t

def fuzzy_match(query):
    nq = normalize(query)
    keys = list(KB.keys())
    if HAVE_RAPIDFUZZ:
        match = process.extractOne(nq, keys, scorer=fuzz.token_sort_ratio)
        if match:
            best_key, score, _ = match
            return best_key, score
        return None, 0
    else:
        # fallback: exact substring or simple word overlap
        for k in keys:
            if all(tok in nq for tok in k.split()):
                return k, 100
        best = None
        best_score = 0
        for k in keys:
            common = sum(1 for w in k.split() if w in nq)
            if common > best_score:
                best_score = common
                best = k
        if best:
            return best, best_score * 25
        return None, 0

def answer_question(q):
    nq = normalize(q)
    # Map request
    if "map" in nq or "show map" in nq or nq.strip() == "map":
        return {"type":"map", "answer":"Displaying the campus map."}
    # direct keys
    for k in KB:
        if k in nq:
            return {"type":"kb", "key":k, "answer":KB[k]["short"], "details":KB[k].get("directions_from_gjbc","")}
    # fuzzy try
    best_key, score = fuzzy_match(q)
    if best_key and score >= 50:
        return {"type":"kb", "key":best_key, "answer":KB[best_key]["short"], "details":KB[best_key].get("directions_from_gjbc",""), "score":score}
    # directional 'from gjb'
    if "from gjb" in nq or "from gjbc" in nq or "from golden jubilee" in nq or "from golden" in nq:
        for k in KB:
            if k in nq and k != "golden jubilee block":
                return {"type":"directions", "answer":KB[k].get("directions_from_gjbc", KB[k]["short"])}
        return {"type":"directions", "answer":"From GJBC walk into the main courtyard and head towards the landmark you need: library (NW), gym (N), food court (E)."}
    return {"type":"fallback", "answer":"Sorry — I don't have a precise answer. Try 'List places' or ask 'Where is the library?'"}

# ---------------- Flask endpoints ----------------
@app.route("/map-image")
def map_image():
    if os.path.exists(MAP_PATH):
        try:
            return send_file(MAP_PATH)
        except Exception as e:
            abort(500, description=f"Error sending file: {e}")
    abort(404, description="Map file not found. Update MAP_PATH in app.py to your map file path.")

@app.route("/hotspots")
def hotspots():
    return jsonify(HOTSPOTS)

@app.route("/places")
def places():
    # return sorted list of place ids for UI list
    return jsonify(sorted([h["id"] for h in HOTSPOTS]))

@app.route("/has-fuzzy")
def has_fuzzy():
    return jsonify({"fuzzy": HAVE_RAPIDFUZZ})

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(force=True)
    q = data.get("q","")
    if not q:
        return jsonify({"ok":False, "answer":"Please ask a question."})
    resp = answer_question(q)
    return jsonify({"ok":True, "resp":resp})

# ---------------- Single-file HTML UI (prettier) ----------------
HTML = r"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <title>PESU GJBC — Pretty Chatbot</title>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <style>
    :root{
      --bg:#0f172a;
      --card:#0b1220;
      --accent:#06b6d4;
      --muted:#94a3b8;
      --surface:#071124;
      --glass: rgba(255,255,255,0.03);
      --radius:12px;
    }
    *{box-sizing:border-box}
    body{margin:0;font-family:Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial;background:linear-gradient(180deg,#071024 0%, #021016 100%);color:#e6eef6}
    .app{display:flex;gap:16px;padding:18px;height:calc(100vh - 36px)}
    .panel{background:var(--glass);border:1px solid rgba(255,255,255,0.04);border-radius:var(--radius);box-shadow:0 6px 30px rgba(2,6,23,0.6);padding:14px;overflow:auto}
    .left{width:320px}
    .center{flex:1;display:flex;flex-direction:column;gap:12px}
    .right{width:300px}
    h2{margin:0 0 8px 0;font-weight:600}
    .top-actions{display:flex;gap:8px;align-items:center;margin-bottom:8px}
    .btn{background:linear-gradient(90deg,var(--accent),#7dd3fc);border:none;color:#012a33;padding:8px 12px;border-radius:8px;cursor:pointer;font-weight:600}
    .ghost{background:transparent;border:1px solid rgba(255,255,255,0.06);color:var(--muted);padding:8px 10px;border-radius:8px;cursor:pointer}
    .mapcard{height:420px;border-radius:12px;padding:10px;position:relative;overflow:hidden;background:linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));display:flex;flex-direction:column}
    .mapwrap{position:relative;flex:1;border-radius:10px;overflow:hidden;background:#081022;border:1px solid rgba(255,255,255,0.02);display:flex;align-items:center;justify-content:center}
    .mapwrap img{max-width:100%;max-height:100%;display:block}
    .marker{position:absolute;transform:translate(-50%,-100%);width:18px;height:18px;border-radius:50%;background:var(--accent);display:flex;align-items:center;justify-content:center;color:#012a33;font-weight:700;box-shadow:0 4px 14px rgba(6,182,212,0.16);cursor:pointer;transition:transform .12s ease, box-shadow .12s ease}
    .marker:hover{transform:translate(-50%,-120%) scale(1.12);box-shadow:0 8px 24px rgba(6,182,212,0.28)}
    .poi-list{display:flex;flex-direction:column;gap:8px;margin-top:8px}
    .poi-btn{background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.03);padding:8px 10px;border-radius:8px;color:#e6eef6;text-align:left;cursor:pointer}
    .chat{display:flex;flex-direction:column;height:340px;background:linear-gradient(180deg, rgba(255,255,255,0.015), rgba(255,255,255,0.01));padding:12px;border-radius:10px}
    .messages{flex:1;overflow:auto;padding-right:6px;display:flex;flex-direction:column;gap:10px}
    .msg{max-width:78%;padding:10px 12px;border-radius:12px;white-space:pre-wrap}
    .msg.bot{background:linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.02));align-self:flex-start;border:1px solid rgba(255,255,255,0.02)}
    .msg.user{background:linear-gradient(180deg, rgba(6,182,212,0.15), rgba(6,182,212,0.08));align-self:flex-end;color:#012a33}
    .meta{font-size:11px;color:var(--muted);margin-top:6px}
    .input-row{display:flex;gap:8px;margin-top:10px}
    .input{flex:1;padding:10px;border-radius:10px;border:1px solid rgba(255,255,255,0.03);background:transparent;color:inherit}
    .small{font-size:13px;color:var(--muted)}
    footer{position:fixed;left:18px;bottom:18px;color:var(--muted);font-size:12px}
    @media(max-width:900px){
      .app{flex-direction:column;padding:10px;height:auto}
      .left,.right{width:100%}
      .mapcard{height:300px}
    }
  </style>
</head>
<body>
  <div class="app">
    <div class="panel left">
      <h2>Quick Actions</h2>
      <div class="top-actions">
        <button class="btn" onclick="showMap()">Show Map</button>
        <button class="ghost" onclick="togglePlaces()">List Places</button>
        <button class="ghost" onclick="clearChat()">Clear Chat</button>
      </div>

      <div id="placesPanel" style="display:none;margin-top:8px">
        <div class="small">Tap a place to ask about it:</div>
        <div id="poi-list" class="poi-list"></div>
      </div>

      <div style="margin-top:12px">
        <div class="small">Tips:</div>
        <ul style="padding-left:18px;color:var(--muted);margin-top:8px">
          <li>Click a marker on the map to ask that place.</li>
          <li>Type free text like "Where is the library?"</li>
          <li>Fuzzy matching: <span id="fuzzy-status">checking...</span></li>
        </ul>
      </div>
    </div>

    <div class="panel center">
      <div class="mapcard">
        <h2 style="margin-bottom:8px">Campus Map (GJBC area)</h2>
        <div class="mapwrap" id="mapwrap">
          <img id="campus-map" src="/map-image" alt="map">
          <!-- markers added dynamically -->
        </div>
      </div>

      <div class="chat">
        <div style="display:flex;justify-content:space-between;align-items:center">
          <h2 style="margin:0">Chat</h2>
          <div class="small" id="time-now"></div>
        </div>
        <div class="messages" id="messages">
          <div class="msg bot">Hi — I'm your PESU map assistant. Try "List Places" or ask "Where is the library?"</div>
        </div>

        <div class="input-row">
          <input id="q" class="input" type="text" placeholder="Ask something (e.g., 'Where is Hornbill Coffee?')">
          <button class="btn" onclick="send()">Send</button>
        </div>
        <div class="meta" id="meta"></div>
      </div>
    </div>

    <div class="panel right">
      <h2>About</h2>
      <div class="small">This is a local orientation helper for the GJBC crop of PESU RR campus. Markers are approximate. For official floor plans contact campus facilities.</div>
      <div style="margin-top:12px">
        <strong>Available places</strong>
        <div id="places-compact" style="margin-top:8px"></div>
      </div>
    </div>
  </div>

  <footer>Made for you — PESU GJBC assistant</footer>

<script>
async function fetchHotspots(){
  const r = await fetch('/hotspots');
  return r.ok ? r.json() : [];
}
async function fetchPlaces(){
  const r = await fetch('/places');
  return r.ok ? r.json() : [];
}

function ts(){ return new Date().toLocaleTimeString(); }
function appendMessage(text, who){
  const cont = document.getElementById('messages');
  const el = document.createElement('div');
  el.className = 'msg ' + (who==='user' ? 'user' : 'bot');
  el.textContent = text;
  const meta = document.createElement('div');
  meta.className = 'meta';
  meta.textContent = ts();
  el.appendChild(meta);
  cont.appendChild(el);
  cont.scrollTop = cont.scrollHeight;
}

async function send(){
  const qEl = document.getElementById('q');
  const q = qEl.value.trim();
  if(!q) return;
  appendMessage(q, 'user');
  qEl.value = '';
  await askServer(q);
}

async function askServer(q){
  try{
    const res = await fetch('/ask', {
      method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({q})
    });
    const j = await res.json();
    if(!j.ok){ appendMessage('Error: ' + (j.answer||'unknown'), 'bot'); return; }
    const r = j.resp;
    if(r.type === 'map'){
      appendMessage(r.answer, 'bot');
      // no-op: map is visible
    } else if(r.type === 'kb' || r.type === 'directions'){
      let out = r.answer;
      if(r.details) out += '\n' + r.details;
      if(r.score) out += '\n(match confidence: ' + r.score + '%)';
      appendMessage(out, 'bot');
    } else {
      appendMessage(r.answer, 'bot');
    }
  }catch(e){
    appendMessage('Network error: ' + e, 'bot');
  }
}

function clearChat(){
  const m = document.getElementById('messages');
  m.innerHTML = '';
  const welcome = document.createElement('div');
  welcome.className = 'msg bot';
  welcome.textContent = "Hi — I'm your PESU map assistant. Try 'List Places' or ask 'Where is the library?'";
  const meta = document.createElement('div'); meta.className='meta'; meta.textContent = ts();
  welcome.appendChild(meta);
  m.appendChild(welcome);
}

async function buildMarkers(){
  const hotspots = await fetchHotspots();
  const wrap = document.getElementById('mapwrap');
  // remove old markers
  document.querySelectorAll('.marker').forEach(x=>x.remove());
  hotspots.forEach(h => {
    const el = document.createElement('div');
    el.className = 'marker';
    el.style.left = h.left + '%';
    el.style.top = h.top + '%';
    el.title = h.id;
    el.onclick = ()=> askServer('Where is ' + h.id + '?');
    el.addEventListener('mouseenter', ()=> showTooltip(h.id, el));
    el.addEventListener('mouseleave', ()=> hideTooltip());
    wrap.appendChild(el);
  });
}

let tooltip;
function showTooltip(text, el){
  hideTooltip();
  tooltip = document.createElement('div');
  tooltip.style.position='absolute';
  tooltip.style.transform='translate(-50%,-120%)';
  tooltip.style.left = el.style.left;
  tooltip.style.top = (parseFloat(el.style.top) - 4) + '%';
  tooltip.style.padding='6px 8px';
  tooltip.style.borderRadius='6px';
  tooltip.style.background='rgba(6,182,212,0.95)';
  tooltip.style.color='#012a33';
  tooltip.style.fontSize='12px';
  tooltip.style.fontWeight='700';
  tooltip.textContent = text;
  document.getElementById('mapwrap').appendChild(tooltip);
}
function hideTooltip(){ if(tooltip){ tooltip.remove(); tooltip=null; } }

async function populatePlaceList(){
  const places = await fetchPlaces();
  const list = document.getElementById('poi-list');
  const compact = document.getElementById('places-compact');
  list.innerHTML = '';
  compact.innerHTML = '';
  places.forEach(p => {
    const btn = document.createElement('button');
    btn.className = 'poi-btn';
    btn.textContent = p;
    btn.onclick = ()=> { appendMessage('Where is ' + p + '?', 'user'); askServer('Where is ' + p + '?'); };
    list.appendChild(btn);

    // compact chip
    const chip = document.createElement('div');
    chip.className = 'small';
    chip.style.marginTop='6px';
    chip.textContent = '• ' + p;
    compact.appendChild(chip);
  });
}

function togglePlaces(){
  const p = document.getElementById('placesPanel');
  p.style.display = (p.style.display === 'none' || p.style.display === '') ? 'block' : 'none';
}

function showMap(){ appendMessage('Showing map...', 'user'); appendMessage('Map is visible above.', 'bot'); }

window.addEventListener('load', async () => {
  document.getElementById('time-now').textContent = new Date().toLocaleString();
  await buildMarkers();
  await populatePlaceList();
  const fuzzy = await fetch('/has-fuzzy').then(r=>r.json());
  document.getElementById('fuzzy-status').textContent = fuzzy.fuzzy ? 'enabled' : 'disabled';
});
</script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

if __name__ == "__main__":
    if not os.path.exists(MAP_PATH):
        print("WARNING: Map file not found at:", MAP_PATH)
        print("Update MAP_PATH in app.py to point to your local map file (e.g., 'gjbc_map.png').")
    print("Starting pretty PESU GJBC chatbot on http://127.0.0.1:5000")
    if HAVE_RAPIDFUZZ:
        print("Fuzzy matching enabled (rapidfuzz detected).")
    else:
        print("Fuzzy matching not installed; install rapidfuzz for typo-tolerance.")
    app.run(debug=True)
    from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# -------------------------------------
#  DATA: PESU RR Campus Map Information
# -------------------------------------

places = {
    "Front Gate": "Main entrance of PES RR campus, located at the south end.",
    "Scooter Parking": "Two-wheeler parking area near the front entrance.",
    "Car Parking": "Four-wheeler parking area in the upper north zone.",
    "Student Lounge": "Relaxation and hangout zone near the center of the campus.",
    "M Block": "Academic block located near the southern region.",
    "A Block": "One of the central academic buildings.",
    "F Block": "Academic block positioned toward the top-left area.",
    "Tech Park": "Located near the center, close to the library zone.",
    "Library": "Central library located near A Block.",
    "Boys Hostel": "Hostel near the eastern region.",
    "Food Stall": "Multiple food stalls in the middle of the campus.",
    "Cafeteria 158th Floor": "Main cafeteria area located near central campus.",
    "Cricket Field": "Sports field on the north side.",
    "Parking Lot": "Primary parking zone in the northern-most area.",
    "GJB Block": "Block located on the west side of campus.",
    "H Block": "Block located near the boys hostel.",
    "Girls Hostel": "Located near the central west area.",
    "B Block": "Academic block next to A Block.",
    "Gym": "Located near the recreation area close to the middle.",
    "Medical Room": "Near A Block and student lounge.",
    "Event Ground": "Open ground area for events near the center.",
    "Basketball Court": "Located near sports zone in the mid-east area."
}

@app.route("/")
def home():
    return render_template("index.html", places=places)

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")

    # Match place
    for name in places:
        if name.lower() in user_input.lower():
            return jsonify({"response": f"{name}: {places[name]}"})

    return jsonify({"response": "I couldn't find that place. Try clicking a button!"})


if __name__ == "__main__":
    app.run(debug=True)

