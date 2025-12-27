from flask import Flask, request, jsonify, render_template_string, send_file
import os
import re

app = Flask(__name__)

# Map image file (keep this file in same folder as app.py)
MAP_PATH = "gjbc_map.png"

# Simple knowledge base
KB = {
    "library": "The Central Library is northwest of the GJBC block on campus.",
    "hornbill": "Hornbill Coffee is on the east/right side of GJBC.",
    "gym": "The PESU Gym is directly north of GJBC.",
    "mechanical block": "The Mechanical block is located in the center of campus.",
    "badminton": "The badminton courts are northeast of the Mechanical block.",
    "basketball": "The basketball court is south of GJBC.",
    "food court": "The GJB Food Court is southeast of GJBC."
}

def normalize(text):
    """Clean user input for matching."""
    t = text.lower().strip()
    t = re.sub(r"[^\w\s]", " ", t)
    t = re.sub(r"\s+", " ", t)
    return t

def answer(q: str):
    """Return chatbot response."""
    nq = normalize(q)

    # If user asks to show map
    if "map" in nq or "show" in nq and "map" in nq:
        return {"type": "map", "answer": "Here is the PESU GJBC map.", "map": True}

    # Check keywords in knowledge base
    for k in KB:
        if k in nq:
            return {"type": "text", "answer": KB[k]}

    # Unknown question
    return {"type": "text", "answer": "I don't know that yet. Try asking: 'Where is the library?' or 'Show map'."}

@app.route("/map")
def map_img():
    """Serve map image."""
    if os.path.exists(MAP_PATH):
        return send_file(MAP_PATH)
    return "Map image not found."

@app.route("/")
def home():
    """Simple chat interface."""
    return """
    <html>
    <body style='font-family:Arial;padding:20px'>
    <h2>PESU GJBC Campus Chatbot</h2>
    <p>Try asking: "Where is the library?" or "Show map"</p>
    
    <input id='q' style='width:300px;padding:5px'>
    <button onclick='ask()'>Ask</button>

    <div id='ans' style='margin-top:20px;white-space:pre-line'></div>

    <script>
    function ask(){
        let q = document.getElementById("q").value;
        fetch("/ask", {
            method:"POST",
            headers:{"Content-Type":"application/json"},
            body:JSON.stringify({q:q})
        })
        .then(r => r.json())
        .then(x => {
            if(x.type=="map"){
                document.getElementById("ans").innerHTML = x.answer + "<br><img src='/map' width='400'>";
            } else {
                document.getElementById("ans").innerHTML = x.answer;
            }
        })
    }
    </script>
    </body>
    </html>
    """

@app.route("/ask", methods=["POST"])
def ask():
    """Handle user questions."""
    q = request.json.get("q", "")
    return jsonify(answer(q))

if __name__ == "__main__":
    print("Running on http://127.0.0.1:5000")
    app.run(debug=True)
