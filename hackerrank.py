'''n = [-5,-4,0,1,2]
added = list(map(lambda x: x + 5, n))
positives = map(lambda x: 1 if x > 0 else 0, added)
print(sum(positives))'''

'''def calculation(x):
    def argument(*args):
        x(*args)
    return argument
def add(a,b):
    print(a+b)
def multiply(*l):
    print
result=calculation(add)
result(5,5) '''    

import math
def calculate(f):              
#decorator function
 def inner1(*args):
#*args is variable length argument
  print("Decorator")
  f(*args) 
# this is being decorated by decorator
 print("**************")
 return inner1 

@calculate
def maximum(*num): 
 print(max(num[0],num[1],num[2])) 
        
    

    
