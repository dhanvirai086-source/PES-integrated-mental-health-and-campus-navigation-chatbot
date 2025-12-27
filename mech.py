import math

try:
    F = float(input("Enter the force (F) in N: "))
    r = float(input("Enter the radius (r) in m: "))
    x = float(input("Enter the horizontal position (x) in m: "))

    if r == 0:
        print("Invalid input: radius cannot be zero")
    elif abs(x) > r:
        print("Invalid input: x must be within [-r, r]")
    else:
        Fn = F * (x / r)
        Ft = F * (math.sqrt(r*2 - x*2) / r)
        print(f"\nNormal Component (Fn): {Fn:.2f} N")
        print(f"Tangential Component (Ft): {Ft:.2f} N")

except Exception:
    print("invalid input")

'''def safe_float(value):
    try:
        return float(value)
    except:
        return None

print("\n=== Trapezoid Centroid Calculator (Rectangle + Triangle Method) ===")

# inputs
a = safe_float(input("Enter top base (a): "))
b = safe_float(input("Enter bottom base (b): "))
h = safe_float(input("Enter height (h): "))

# Validation
if a is None or b is None or h is None or a <= 0 or b <= 0 or h <= 0:
    print("\nInvalid input")
else:
    # Extra width of the triangle
    t = abs(a - b)

    # Areas
    A_rect = b * h
    A_tri = 0.5 * t * h
    A_total = A_rect + A_tri

    # Centroid of rectangle (measured from bottom-left)
    x_rect = b / 2
    y_rect = h / 2

    # Centroid of right triangle
    # If top base > bottom base → triangle on right
    if a > b:
        x_tri = b + t / 3
    else:  # triangle on left
        x_tri = t / 3

    y_tri = h / 3

    # Composite centroid formula
    x_c = (A_rect * x_rect + A_tri * x_tri) / A_total
    y_c = (A_rect * y_rect + A_tri * y_tri) / A_total

    print("\n=== Centroid Using Composite Method ===")
    print(f"X-centroid: {x_c:.2f} mm")
    print(f"Y-centroid: {y_c:.2f} mm")'''

        
