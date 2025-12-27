import my_module 
x=int(input("enter a number"))
y=int(input("enter a number"))
o=input("enter operator")
if o=="+":
    print(my_module.add(x,y))
elif o=="-":
    print(my_module.sub(x,y))
elif o=="*":
    print(my_module.multiple(x,y))
elif o=="/":
    print(my_module.div(x,y))
else:
    print("invalid")