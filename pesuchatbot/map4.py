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
