'''def outer(a):
    def inner(b):
        return(a+b)
    return inner
f=outer("hello")
print(f("bye"))'''

'''def outer(a):
    def inner():
        nonlocal a
        a=a+1
        return(a)
    return inner
f=outer(10)
print(f())
del outer
print("after deleting:",f())'''

'''def outer(a):
    def inner(b):
        return(a/b)
    return inner
f=outer(10)
print(f(5))'''

'''def outer(a):
    def inner(b):
        return(a-b)
    return inner
f=outer(10)
print(f(5))'''

'''def outer(a):
    def inner(b):
        return(a**b)
    return inner
f=outer(10)
print(f(5))'''

'''def outer(a):
    def inner(b):
        return(a*b)
    return inner
f=outer(10)
print(f(5))'''

'''def outer(a):
    def inner(b):
        return(a+b)
    return inner
f=outer(10)
print(f(5))'''

'''def outer():
    x=1
    print(x)
    def inner ():
        nonlocal x
        x=x+2
        return x
    return inner
f=outer()'''

'''import math
try:
 F = float(input("Enter the force (F) in N: "))
 r = float(input("Enter the radius (r) in m: "))
 x = float(input("Enter the horizontal position (x) in m: "))'''

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
        Ft = F * (math.sqrt(r**2 - x**2) / r)
        print(f"\nNormal Component (Fn): {Fn:.2f} N")
        print(f"Tangential Component (Ft): {Ft:.2f} N")

except Exception:
    print("Invalid input")

