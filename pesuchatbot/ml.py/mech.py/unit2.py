import tkinter as tk
import re

# ------------------------------
# TEXT → NUMBER PARSER (safe)
# Returns (value, is_valid)
# ------------------------------

_units = {
    "zero":0,"one":1,"two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,"eight":8,"nine":9,
    "ten":10,"eleven":11,"twelve":12,"thirteen":13,"fourteen":14,
    "fifteen":15,"sixteen":16,"seventeen":17,"eighteen":18,"nineteen":19
}

_tens = {
    "twenty":20,"thirty":30,"forty":40,"fifty":50,"sixty":60,
    "seventy":70,"eighty":80,"ninety":90
}

_scales = {"hundred":100, "thousand":1000}

def parse_number(text):
    if not text:
        return 0.0, False

    s = text.lower().strip().replace("-", " ")

    # Try direct float ('5', '-3.2', '50kg')
    try:
        return float(s), True
    except:
        pass

    # Extract digit substring (e.g. "50kg")
    m = re.search(r"[+-]?\d+(\.\d+)?", s)
    if m:
        try:
            return float(m.group()), True
        except:
            pass

    # Word parsing
    words = s.split()
    if not words:
        return 0.0, False

    negative = False
    if words[0] in ("negative", "minus"):
        negative = True
        words = words[1:]

    total = 0
    current = 0

    for w in words:
        if w in _units:
            current += _units[w]
        elif w in _tens:
            current += _tens[w]
        elif w == "hundred":
            current *= 100
        elif w == "thousand":
            current *= 1000
            total += current
            current = 0
        elif w == "and":
            continue
        else:
            return 0.0, False

    total += current
    if negative:
        total = -total

    return float(total), True


# ------------------------------
# CALCULATION FUNCTION
# ------------------------------
def calculate():
    raw_W = entry_W.get()
    raw_a = entry_a.get()
    raw_b = entry_b.get()

    W, okW = parse_number(raw_W)
    a, oka = parse_number(raw_a)
    b, okb = parse_number(raw_b)

    # Avoid zero division
    if (a + b) == 0:
        RA = RB = 0
        note = "(a + b = 0 → invalid geometry)"
    else:
        RA = W * b / (a + b)
        RB = W * a / (a + b)
        note = ""

    # Note for invalid inputs
    notes = []
    if not okW: notes.append("W invalid → treated as 0")
    if not oka: notes.append("a invalid → treated as 0")
    if not okb: notes.append("b invalid → treated as 0")
    if note: notes.append(note)

    final_note = "\n".join(notes)

    result.set(
        f"Input W: {raw_W}\n"
        f"Input a: {raw_a}\n"
        f"Input b: {raw_b}\n\n"

        f"Interpreted W = {W} kN\n"
        f"Interpreted a = {a} m\n"
        f"Interpreted b = {b} m\n\n"

        f"Reaction at A = {RA} kN\n"
        f"Reaction at B = {RB} kN\n\n"
        f"{final_note}"
    )


# ------------------------------
# GUI
# ------------------------------
root = tk.Tk()
root.title("Reaction Calculator (3 Inputs)")
root.geometry("420x420")
root.config(bg="#1e1e1e")

title = tk.Label(root, text="Reaction Calculator", 
                 fg="white", bg="#1e1e1e", font=("Arial", 16, "bold"))
title.pack(pady=10)

# W
tk.Label(root, text="Enter Load W:", fg="white", bg="#1e1e1e", font=("Arial", 13)).pack()
entry_W = tk.Entry(root, font=("Arial", 14), justify="center")
entry_W.pack(pady=5)

# a
tk.Label(root, text="Enter Distance a:", fg="white", bg="#1e1e1e", font=("Arial", 13)).pack()
entry_a = tk.Entry(root, font=("Arial", 14), justify="center")
entry_a.pack(pady=5)

# b
tk.Label(root, text="Enter Distance b:", fg="white", bg="#1e1e1e", font=("Arial", 13)).pack()
entry_b = tk.Entry(root, font=("Arial", 14), justify="center")
entry_b.pack(pady=5)

btn = tk.Button(root, text="Calculate", font=("Arial", 14),
                bg="#333", fg="white", command=calculate)
btn.pack(pady=15)

result = tk.StringVar()
output = tk.Label(root, textvariable=result, fg="white",
                  bg="#1e1e1e", font=("Arial", 12), justify="left")
output.pack(pady=10)

root.mainloop()

