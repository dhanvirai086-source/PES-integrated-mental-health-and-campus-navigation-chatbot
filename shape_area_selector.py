shape = input("enter name of the shape")
if shape == ("circle"):
    r = int(input("enter radius"))
    area = 3.14*r**2
    print("area is",area)
elif shape == ("square"):
    s = int(input("enter side"))
    area = s**2
    print("area is",area)
elif shape == ("rectangle"):
    l = int(input("enter length"))
    b = int(input("enter breadth"))
    area = l*b
    print("area is",area)
else:
    h = int(input("enter height"))
    b = int(input("enter base"))
    area = (1/2)*b*h
    print("area is",area)