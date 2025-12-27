print("french_fries=(100)")
print("softie=(30)")
print("burger=(150)")
print("churos=(170)")
print("fried_chicken=(200)")
choice = input("enter your order")
if choice == ("french_fries"):
    a = int(100)
    print("total bill is 100 rs")
elif choice == ("softie"):
    a = int(30)
    print("total bill is 30rs")
elif choice == ("burger"):
    a = int(150)
    print("total bill is 150rs")
elif choice == ("churos"):
    a = int(170)
    print("total bill is 170rs")
else:
    a = int(200)
    print("total bill is 200 rs")
number_of_people = int(input("enter the number of people"))
tip_percentage = int(input("enter tip precentage"))

if number_of_people == 0:
    print("you can't split bill among 0 people!")
else:
    tip_amount = (tip_percentage/100)*a
    each_person_should_pay = (a+tip_amount)/number_of_people
    print("each person should pay Rs",each_person_should_pay)