def compute_reactions(W, a, b):
    RA = W * a / (a + b)
    RB = W * b / (a + b)
    return RA, RB

def main():
    import math
    try:
        rawW = input("Enter load W (in kN, e.g. 5): ").strip()
        raw_a = input("Enter horizontal distance of A from center (mm, default 24): ").strip()
        raw_b = input("Enter horizontal distance of B from center (mm, default 24): ").strip()

        W_kN = float(rawW)
        a = float(raw_a) if raw_a != "" else 24.0
        b = float(raw_b) if raw_b != "" else 24.0

        if W_kN <= 0 or a < 0 or b < 0:
            print("Invalid input")
            return

        if abs(a - b) < 1e-9:
            RA = RB = W / 2.0
        else:
            RA, RB = compute_reactions(W, a, b)
        print(f"\nReactions (kN):")
        print(f"RA = {RA:.3f} kN")
        print(f"RB = {RB:.3f} kN")

    except Exception:
        print("Invalid input")
if _name_ == "_main_":
    main()