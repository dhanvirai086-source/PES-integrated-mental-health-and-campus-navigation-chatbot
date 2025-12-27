def gcd(x,y):   
    if x == y:   
        result = x
    elif x > y:
        result = gcd(x-y,y)
    else:
        result = gcd(x, y-x)
    return result

print("GCD:", gcd(4,8))


