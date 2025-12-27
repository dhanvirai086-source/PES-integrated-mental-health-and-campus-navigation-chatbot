from flask import Flask, request, jsonify, render_template_string, send_file
import os
import re

app = Flask(__name__)

# Map image file (keep this file in same folder as app.py)
MAP_PATH = "gjbc_map.png"

KB = {
    "library": "Central Library is northwest of GJBC on the map.",
    "hornbill": "Hornbill Coffee is on the east/right side of GJBC.",
    "gym": "PESU Gym is directly north of GJBC.",
    "mechanical block": "Mechanical block is located in the center of the map.",
    "badminton": "Badminton courts are northeast of Mechanical block.",
    "basketball": "Basketball court is south of GJBC.",
    "food court": "GJB Food Court is on the east-southeast of GJBC."
}

def normalize(text):
    t = text.lower().strip()
    t = re.sub(r"[^\w\s]", " ", t)
    t = re.sub(r"\s+", " ", t)
    return t

def answer(q: str):
    nq = normalize(q)

    if "map" in nq or "show map" in nq:
        return {"type": "map", "answer": "Here is the campus map.", "map": True}

    for k in KB:
        if k in nq:
            return {"type": "text", "answer": KB[k]}

    return {"type": "text", "answer": "I don't know that yet. Try asking: 'Where is the library?' or 'Show map'."}

@app.route("/map")
def map_img():
    if os.path.exists(MAP_PATH):
        return send_file(MAP_PATH)
    return "Map not found."

@app.route("/")
def home():
    return """
    <html>
    <body style='font-family:Arial;padding:20px'>
    <h2>PESU GJBC Chatbot</h2>
    <p>Ask: "Where is the library?" or "Show map"</p>
    <input id='q' style='width:300px;padding:5px'>
    <button onclick='ask()'>Ask</button>
    <div id='ans' style='margin-top:20px;white-space:pre-line'></div>

    <script>
    function ask(){
        let q = document.getElementById("q").value;
        fetch("/ask",{
            method:"POST",
            headers:{"Content-Type":"application/json"},
            body:JSON.stringify({q:q})
        })
        .then(r=>r.json())
        .then(x=>{
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
    q = request.json.get("q", "")
    return jsonify(answer(q))

if __name__ == "__main__":
    print("Running on http://127.0.0.1:5000")
    app.run(debug=True)
