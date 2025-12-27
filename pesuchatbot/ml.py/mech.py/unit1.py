import tkinter as tk
import math
import re
_units = [
    "zero","one","two","three","four","five","six","seven","eight","nine","ten",
    "eleven","twelve","thirteen","fourteen","fifteen","sixteen","seventeen","eighteen","nineteen",
]
_tens = ["", "", "twenty","thirty","forty","fifty","sixty","seventy","eighty","ninety"]
_scales = {"hundred": 100, "thousand": 1000, "million": 1_000_000, "billion": 1_000_000_000}
_numwords = {}
for i, w in enumerate(_units):
    _numwords[w] = i
for i, w in enumerate(_tens):
    if w:
        _numwords[w] = i * 10
def parse_number_text(text):
    try:
        if text is None:
            return 0.0
        s = str(text).strip().lower()
        if s == "":
            return 0.0
        try:
            return float(s)
        except Exception:
            pass
        s = s.replace(",", " ")
        s = s.replace("-", " ")  # allow "forty-five"
        s = s.replace("minus", "negative")
        toks = re.split(r"\s+", s)
        sign = 1
        if toks and toks[0] in ("negative", "minus"):
            sign = -1
            toks = toks[1:]
        if not toks:
            return 0.0

        total = 0
        current = 0
        i = 0
        while i < len(toks):
            w = toks[i]
            i += 1

            if w == "and":
                continue
            if w in _numwords:
                current += _numwords[w]
            elif w in _scales:
                scale = _scales[w]
                if current == 0:
                    current = 1
                current *= scale
                total += current
                current = 0
            elif w in ("point", "dot"):
                # fractional part: gather remaining tokens as digits if possible
                frac = ""
                while i < len(toks):
                    token = toks[i]
                    i += 1
                    if token in _numwords:
                        frac += str(_numwords[token])
                    elif re.fullmatch(r"\d+", token):
                        frac += token
                    else:
                        # invalid token in fractional part -> give up and return 0
                        return 0.0
                if frac == "":
                    return 0.0
                try:
                    return sign * (total + current + float("0." + frac))
                except Exception:
                    return 0.0
            elif re.fullmatch(r"\d+(\.\d+)?", w):
                try:
                    current += float(w)
                except Exception:
                    return 0.0
            else:
                return 0.0

        return sign * (total + current)
    except Exception:
        return 0.0
def compute_components_safe(F, s, r):
    notes = []
    try:
        if r is None:
            notes.append("Radius r was missing; treated as 0.")
            return 0.0, 0.0, 0.0, 1.0, notes
        if r <= 0:
            notes.append("Invalid radius,enter a positive integer")
            return 0.0, 0.0, 0.0, 1.0, notes
        if abs(s) > r: 
            notes.append("invalid input,enter a postive integer")
            return 0.0, 0.0, 0.0, 1.0, notes
        sin_th = s / r
        sin_th = max(-1.0, min(1.0, sin_th))
        cos_th = math.sqrt(max(0.0, 1.0 - sin_th * sin_th))

        n = -F * cos_th
        t = F * sin_th
        return n, t, sin_th, cos_th, notes
    except Exception as e:
        notes.append(f"invalid input,enter an integer")
        return 0.0, 0.0, 0.0, 1.0, notes
class ForceApp:
    def __init__(self, root):
        self.root = root
        root.title("Force Components (safe, no crashes)")

        frm = tk.Frame(root, padx=12, pady=12)
        frm.pack(fill="both", expand=True)

        # Input rows
        tk.Label(frm, text="Vertical force F (e.g. 50 or 'negative fifty'):", anchor="w").grid(row=0, column=0, sticky="w")
        self.entry_F = tk.Entry(frm, width=30)
        self.entry_F.grid(row=0, column=1, pady=4, sticky="w")
        self.entry_F.insert(0, "50")

        tk.Label(frm, text="Horizontal position s (from top, e.g. 10 or 'minus twenty'):", anchor="w").grid(row=1, column=0, sticky="w")
        self.entry_s = tk.Entry(frm, width=30)
        self.entry_s.grid(row=1, column=1, pady=4, sticky="w")
        self.entry_s.insert(0, "0")

        tk.Label(frm, text="Circle radius r (e.g. 25):", anchor="w").grid(row=2, column=0, sticky="w")
        self.entry_r = tk.Entry(frm, width=30)
        self.entry_r.grid(row=2, column=1, pady=4, sticky="w")
        self.entry_r.insert(0, "25")

        btn_frame = tk.Frame(frm)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=(8,4), sticky="w")

        calc_btn = tk.Button(btn_frame, text="Calculate", command=self.on_calculate, width=12)
        calc_btn.pack(side="left", padx=(0,8))

        clear_btn = tk.Button(btn_frame, text="Clear Results", command=self.clear_results, width=12)
        clear_btn.pack(side="left")
        self.result_text = tk.Text(frm, width=70, height=14, wrap="word")
        self.result_text.grid(row=4, column=0, columnspan=2, pady=(6,0))
        self.result_text.configure(state="disabled")
        instr = (
            "Instructions: You may type numbers like -50, 3.14, or words like 'negative fifty', 'forty five',\n"
            "'one hundred and two', 'three point one four'.\n"
            "Any invalid input (e.g. 'a', 'hello', emojis, blank) will be treated as 0.0 and the program will not crash.\n"
        )
        tk.Label(frm, text=instr, justify="left").grid(row=5, column=0, columnspan=2, pady=(8,0), sticky="w")

    def clear_results(self):
        self.result_text.configure(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.configure(state="disabled")
    def on_calculate(self):
        rawF = self.entry_F.get()
        raws = self.entry_s.get()
        rawr = self.entry_r.get()

        F = parse_number_text(rawF)
        s = parse_number_text(raws)
        r = parse_number_text(rawr)

        n, t, sin_th, cos_th, notes = compute_components_safe(F, s, r)

        # Build output
        out_lines = []
        out_lines.append("Inputs (parsed; invalid → 0):")
        out_lines.append(f"  F = {F!s}")
        out_lines.append(f"  s = {s!s}")
        out_lines.append(f"  r = {r!s}")
        out_lines.append("")
        if notes:
            out_lines.append("Notes:")
            for note in notes:
                out_lines.append(f"  - {note}")
            out_lines.append("")

        out_lines.append("Formulas used:")
        out_lines.append("  sin(θ) = s / r")
        out_lines.append("  cos(θ) = sqrt(1 - (s/r)^2)")
        out_lines.append("  n = -F * cos(θ)")
        out_lines.append("  t = F * sin(θ)")
        out_lines.append("")
        out_lines.append("Computed values:")
        out_lines.append(f"  sin(θ) = {sin_th:.6g}")
        out_lines.append(f"  cos(θ) = {cos_th:.6g}")
        out_lines.append(f"  n (normal component) = {n:.6g}")
        out_lines.append(f"  t (tangential component) = {t:.6g}")
        out_lines.append("")
        out_lines.append("Sign convention: Force vector = (0, -F). Positive t follows s/r sign; negative n indicates compressive/inward.")

        # Display results (no popups)
        self.result_text.configure(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, "\n".join(out_lines))
        self.result_text.configure(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = ForceApp(root)
    root.mainloop()
