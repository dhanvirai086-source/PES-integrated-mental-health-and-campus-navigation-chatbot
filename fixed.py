def compute_reactions(W, a, b):
    RA = W * a / (a + b)
    RB = W * b / (a + b)
    return RA, RB

