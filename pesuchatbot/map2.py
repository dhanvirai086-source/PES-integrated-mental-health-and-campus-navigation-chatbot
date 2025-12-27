from flask import Flask, request, jsonify, render_template_string, send_file, abort
import os, re

# Try to import rapidfuzz (optional, used for fuzzy matching)
try:
    from rapidfuzz import process, fuzz
    HAVE_RAPIDFUZZ = True
except Exception:
    HAVE_RAPIDFUZZ = False

app = Flask(__name__)

# === IMPORTANT ===
# Using the uploaded image path you provided earlier.
# If you want to use a local copy (e.g., gjbc_map.png in same folder), change this path.
MAP_PATH = "/mnt/data/8b3b1ee7-3924-47bd-b940-050213295fd9.png"

# Knowledge base: keys are canonical POI names.
KB = {
    "golden jubilee block": {
        "short": "Golden Jubilee Block (GJBC) — main academic block in the southeast of the crop.",
        "directions_from_gjbc": "You are at GJBC. Use the GJBC entrance to go north to the main courtyard."
    },
    "hornbill coffee": {
        "short": "Hornbill Coffee — east side near the food court.",
        "directions_from_gjbc": "From GJBC head east; Hornbill Coffee is visible on the right side of the crop."
    },
    "central library": {
        "short": "Central Library — northwest of the GJBC block.",
        "directions_from_gjbc": "Walk northwest across the open area toward the library building."
    },
    "pesu gym": {
        "short": "PESU Gym — north / top-center on the crop.",
        "directions_from_gjbc": "Head north from GJBC across the courtyard to reach the gym."
    },
    "mechanical block": {
        "short": "Mechanical (C) Block — central landmark in the crop.",
        "directions_from_gjbc": "From GJBC go slightly north-west to locate the Mechanical block."
    },
    "badminton court": {
        "short": "Badminton Court — northeast of Mechanical block.",
        "directions_from_gjbc": "From GJBC: go north-east across the courtyard to reach the badminton courts."
    },
    "basketball court": {
        "short": "Basketball Court — just south of GJBC.",
        "directions_from_gjbc": "Exit GJBC and walk south to find the basketball court."
    },
    "food court": {
        "short": "GJB Food Court — near GJBC and Hornbill Coffee (east/southeast).",
        "directions_from_gjbc": "From the GJBC main entry, walk east/southeast to the food court area."
    }
}

# Hotspot definitions for clickable overlay.
# Coordinates are given in percentages (left%, top%) and an optional label.
# You can tweak these values visually if the marker is off.
HOTSPOTS = [
    {"id": "golden jubilee block", "left": 74, "top": 68},
    {"id": "hornbill coffee", "left": 85, "top": 60},
    {"id": "central library", "left": 30, "top": 18},
    {"id": "pesu gym", "left": 46, "top": 6},
    {"id": "mechanical block", "left": 50, "top": 38},
    {"id": "badminton court", "left": 62, "top": 28},
    {"id": "basketball court", "left": 74, "top": 80},
    {"id": "food court", "left": 80, "top": 72},
]

def normalize(text):
    t = text.lower().strip()
    t = re.sub(r"[^\w\s]", " ", t)
    t = re.sub(r"\s+", " ", t)
    return t

def fuzzy_match(query):
    """Return best matching KB key and score. Uses rapidfuzz if available otherwise simple substring."""
    nq = normalize(query)
    keys = list(KB.keys())
    if HAVE_RAPIDFUZZ:
        match = process.extractOne(nq, keys, scorer=fuzz.token_sort_ratio)
        if match:
            # match -> (best_key, score, index)
            best_key, score, _ = match
            return best_key, score
        return None, 0
    else:
        # fallback: substring or exact
        for k in keys:
            if all(tok in nq for tok in k.split()):
                return k, 100
        # simple partial match
        best = None
        best_score = 0
        for k in keys:
            # count common words
            common = sum(1 for w in k.split() if w in nq)
            if common > best_score:
                best_score = common
                best = k
        if best:
            return best, best_score * 20  # rough score
        return None, 0

def answer_question(q):
    nq = normalize(q)
    # map request
    if "map" in nq or "show map" in nq or "show me map" in nq:
        return {"type":"map", "answer":"Here's the GJBC map crop.", "map_url":"/map-image"}
    # direct match
    for k in KB:
        if k in nq:
            return {"type":"kb", "key":k, "answer":KB[k]["short"], "details":KB[k].get("directions_from_gjbc","")}
    # try fuzzy match
    best_key, score = fuzzy_match(q)
    if best_key and score >= 50:
        return {"type":"kb", "key":best_key, "answer":KB[best_key]["short"], "details":KB[best_key].get("directions_from_gjbc",""), "score":score}
    # directional phrasing from GJBC
    if "from gjb" in nq or "from gjbc" in nq or "from golden jubilee" in nq or "from golden" in nq:
        # try to detect destination keyword
        for k in KB:
            if k in nq and k != "golden jubilee block":
                return {"type":"directions", "answer":KB[k].get("directions_from_gjbc", KB[k]["short"])}
        return {"type":"directions", "answer":"From GJBC, move into the main courtyard and use the map markers: library (NW), gym (N), food court (E)."}
    # fallback
    return {"type":"fallback", "answer":"I don't have a precise answer for that. Try 'Where is the library?' or click a marker on the map."}

# === Flask endpoints ===

@app.route("/map-image")
def map_image():
    if os.path.exists(MAP_PATH):
        try:
            return send_file(MAP_PATH)
        except Exception as e:
            abort(500, description=f"Error sending file: {e}")
    abort(404, description="Map file not found. Update MAP_PATH in app.py to point to your map file.")

@app.route("/hotspots")
def hotspots():
    return jsonify(HOTSPOTS)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(force=True)
    q = data.get("q","")
    if not q:
        return jsonify({"ok":False, "answer":"Please ask a question."})
    resp = answer_question(q)
    return jsonify({"ok":True, "resp":resp})

# Single-file HTML UI with overlay markers and chat.
HTML = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <title>PESU GJBC Chatbot — Upgraded</title>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <style>
    body { font-family: Arial, sans-serif; margin:0; background:#f3f4f6; }
    .wrap { display:flex; gap:12px; padding:12px; height:calc(100vh - 24px); box-sizing:border-box; }
    .left { width:340px; background:#fff; border-radius:8px; padding:12px; box-shadow:0 6px 18px rgba(0,0,0,0.06); overflow:auto; }
    .center { flex:1; display:flex; flex-direction:column; gap:12px; }
    .mapcard { background:#fff; padding:8px; border-radius:8px; box-shadow:0 6px 18px rgba(0,0,0,0.06); }
    .mapwrap { position:relative; width:100%; padding-top:60%; /* maintains aspect ratio */ overflow:hidden; }
    .mapwrap img { position:absolute; left:0; top:0; width:100%; height:100%; object-fit:contain; }
    .marker { position:absolute; transform:translate(-50%,-100%); cursor:pointer; background:linear-gradient(#fff,#fff); border-radius:50%; padding:6px; border:2px solid #0ea5e9; width:18px; height:18px; display:flex; align-items:center; justify-content:center; font-size:11px; box-shadow:0 2px 6px rgba(0,0,0,0.12); }
    .chat { background:#fff; padding:10px; border-radius:8px; display:flex; flex-direction:column; height:320px; }
    .messages { flex:1; overflow:auto; padding:6px; }
    .msg { margin:6px 0; max-width:80%; padding:8px 10px; border-radius:8px; }
    .bot { background:#eef2ff; align-self:flex-start; }
    .user { background:#dcfce7; align-self:flex-end; }
    .poi-btn { display:block; margin:6px 0; padding:8px; border-radius:6px; background:#f8fafc; border:1px solid #eee; cursor:pointer; text-align:left; }
    .small { font-size:13px; color:#475569; }
    .inputrow { display:flex; gap:8px; margin-top:8px; }
    input[type=text] { flex:1; padding:8px; border-radius:6px; border:1px solid #e6e6e6; }
    button { padding:8px 12px; border-radius:6px; background:#0ea5e9; color:white; border:none; cursor:pointer; }
  </style>
</head>
<body>
  <div class="wrap">
    <div class="left">
      <h3>PESU — Quick POIs</h3>
      <div id="poi-list"></div>
      <hr/>
      <div class="small">Tip: Click a marker on the map or ask something like "Where is the library?" or "Show map".</div>
      <div style="margin-top:8px; font-size:12px; color:#475569;">
        <div>Fuzzy matching: <span id="fuzzy-status">disabled</span></div>
        <div style="margin-top:6px;">If fuzzy matching is enabled you'll get answers even for typos.</div>
      </div>
    </div>

    <div class="center">
      <div class="mapcard">
        <h3>Campus map (GJBC area)</h3>
        <div class="mapwrap" id="mapwrap">
          <img id="campus-map" src="/map-image" alt="map"/>
          <!-- markers injected here -->
        </div>
      </div>

      <div class="chat">
        <h3>Chat</h3>
        <div class="messages" id="messages">
          <div class="msg bot">Hi — I'm the upgraded PESU map helper. Click markers or ask questions.</div>
        </div>
        <div class="inputrow">
          <input id="q" type="text" placeholder="Ask: 'Where is the library?'">
          <button onclick="send()">Send</button>
        </div>
      </div>
    </div>

    <div style="width:280px;">
      <div style="background:#fff; padding:12px; border-radius:8px; box-shadow:0 6px 18px rgba(0,0,0,0.06);">
        <h4>About this bot</h4>
        <p style="font-size:13px; margin:0;">This is a local orientation helper — for official floorplans contact campus facilities. Hotspots are approximate; reposition markers in server code if needed.</p>
      </div>
    </div>
  </div>

<script>
async function loadHotspots(){
  const res = await fetch('/hotspots');
  const hotspots = await res.json();
  const list = document.getElementById('poi-list');
  list.innerHTML = '';
  const wrap = document.getElementById('mapwrap');

  hotspots.forEach(h => {
    // add list button
    const b = document.createElement('button');
    b.className = 'poi-btn';
    b.textContent = h.id;
    b.onclick = () => askServer('Where is ' + h.id + '?');
    list.appendChild(b);

    // add marker
    const m = document.createElement('div');
    m.className = 'marker';
    m.title = h.id;
    m.style.left = h.left + '%';
    m.style.top = h.top + '%';
    m.onclick = () => askServer('Where is ' + h.id + '?');
    m.innerText = '•';
    wrap.appendChild(m);
  });
}

function appendMessage(text, who){
  const cont = document.getElementById('messages');
  const div = document.createElement('div');
  div.className = 'msg ' + (who === 'user' ? 'user' : 'bot');
  div.style.whiteSpace = 'pre-line';
  div.textContent = text;
  cont.appendChild(div);
  cont.scrollTop = cont.scrollHeight;
}

function send(){
  const qEl = document.getElementById('q');
  const q = qEl.value.trim();
  if(!q) return;
  appendMessage(q, 'user');
  qEl.value = '';
  askServer(q);
}

async function askServer(q){
  try{
    const res = await fetch('/ask', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({q})
    });
    const data = await res.json();
    if(!data.ok){
      appendMessage('Error: ' + (data.answer || 'unknown'), 'bot');
      return;
    }
    const r = data.resp;
    if(r.type === 'map'){
      appendMessage(r.answer, 'bot');
      // map already visible
    } else if(r.type === 'kb' || r.type === 'directions'){
      let text = r.answer;
      if(r.details) text += "\\n" + r.details;
      if(r.score) text += `\\n(match confidence: ${r.score})`;
      appendMessage(text, 'bot');
    } else {
      appendMessage(r.answer, 'bot');
    }
  }catch(e){
    appendMessage('Network error: ' + e, 'bot');
  }
}

window.onload = async () => {
  await loadHotspots();
  // show fuzzy status
  const res = await fetch('/has-fuzzy');
  const js = await res.json();
  document.getElementById('fuzzy-status').textContent = js.fuzzy ? 'enabled' : 'disabled';
};
</script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/has-fuzzy")
def has_fuzzy():
    return jsonify({"fuzzy": HAVE_RAPIDFUZZ})

if __name__ == "__main__":
    # sanity checks
    if not os.path.exists(MAP_PATH):
        print("WARNING: Map file not found at:", MAP_PATH)
        print("Update MAP_PATH in app.py or place the map file at that path.")
    print("Starting upgraded PESU GJBC Chatbot on http://127.0.0.1:5000")
    if HAVE_RAPIDFUZZ:
        print("Fuzzy matching (rapidfuzz) is ENABLED.")
    else:
        print("Fuzzy matching is NOT installed; exact/keyword matching will be used.")
    app.run(debug=True)
