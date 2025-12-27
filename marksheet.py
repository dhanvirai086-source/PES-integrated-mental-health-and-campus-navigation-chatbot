m = int(input("enter maths marks"))
cse = int(input("enter cse marks"))  
c = int(input("enter chem marks"))
mech = int(input("enter mech marks"))
e = int(input("enter electronics marks"))
total =  m+cse+c+mech+e
print("total=", total)
percentage = (total/500)*100
if percentage >=95:
    print(percentage,"percentage")
elif percentage >=90 and percentage<=95:
    print("A")
elif percentage >=80 and percentage<=75:
    print("B")
else:
    print("u r too dumb just quit")

    