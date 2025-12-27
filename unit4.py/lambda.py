'''greatest=lambda n,m:max(n,m)
print(greatest,type(greatest))'''

'''numbers=(1,2,3,4)
result=map(lambda x:x*x,numbers)
print(list(result))'''

'''a=(1,2,3,4)
b=(5,6,7,8)
result=map(lambda a,b:a+b,a,b)
print(list(result))'''

'''def double_num(n):
    if n%2==0:
        return n*2
    else:
        return n
n=[1,2,3,4]
result=list(map(double_num,n))
print(result)'''

'''odd=lambda x: bool(x%2)
num=[i for i in range(10)]
print(num)
n=list()
for i in num:
  if odd(i):
    continue
  else:
    break'''

'''marks = [55, 78, 90, 87, 65, 45]
def myFunc(m):
  if m <70 :
   return False
  else:
   return True
Distinction = list(filter(myFunc, marks))
print("Students with marks greater than 70 are",Distinction)'''


'''def myfinc(m):
    # for i in characters:
      if characters in vowels:
        return False
      else:
        return True
vo=list(filter(myfinc,characters))
vowels=[a,e,i,o,u]'h', 'e', 'l', 'l', 'o', 'w', 'o', 'r','l','d'
print(vo)'''

'''import functools
l=[2,4,1,6,7]
def func(a,b):
    return a*b
print(functools.reduce(func,l,2))'''

'''import functools
l=["sin","r","pa","sagara"]
print(functools.reduce(lambda x,y:x+y[0],l,""))'''

'''l1=[1,2,3]
l2=[5,6,7]
result=(zip(l1,l2))
print(list(result))'''

'''A=[23,22,55,99]
B=[88,99,22]
print(list(zip(A,B)))'''

'''A=[1,2,3,4,5]
B=list(map(lambda x:x^3,A))
print(list(zip(A,B)))
print(B)'''

'''l=[]
for i in range(0,11):
    l.append(i**3)'''
'''print([i**3 for i in range(0,11)])'''

'''import functools
n=5
print(functools.reduce(int.__mul__,range(1,n+1)))'''

'''import functools
print(functools.reduce(int.__add__,range(10)))'''

'''def product(x,y):
    import functools
    print(functools.reduce(x*y))'''

'''import functools
temperature = [22.5, 24.6, 26, 32, 27.5] 
print(functools.reduce(lambda a,b:a+b,temperature))
print(functools.reduce(lambda a,b:a if a>b else b,temperature))'''

'''name = [ "Sudha", "Suma", "Sara", "Asha" ]
roll_no = [ 404, 112, 393, 223 ]
print(list(zip(name,roll_no)))'''

'''a =[1, 2, 3, 4, 5]
b =list(map(lambda x : x * x * x, a))
print(list(zip(a,b)))'''

'''persons = ["Baskar", "Monica", "Riya", "Madhav", "John", 
"Prashanth"]
ages = (35, 26, 28, 14)
print(list(zip(persons,ages)))'''

'''lists= [1,2,3,4,5]
Chars= ['a', 'b','c', 'd', 'e']
print(list(zip(lists,Chars)))'''

#Lst=['orange', 'apple' , 'mango','apricot']
'''print(list(filter(lambda Fruits:Fruits.strip().startswith('a'),Lst)))'''
#print(list(filter(None,map(lambda fruits:fruits if fruits.strip().startswith('a') else None,Lst))))

'''from functools import reduce
n="1729"
print(reduce(lambda a,b: int(a)+int(b),n))'''

'''class Rectangle:
 def __init__(self, length, width):
   self.length = length
   self.width = width
 def display(self):
   print(f"Rectangle dimensions: {self.length} x {self.width}")
 def __del__(self):
   print("Rectangle object destroyed.")
# Creating a Rectangle object
rect = Rectangle(5, 10)
rect.display()'''

class A:
    def disp(self):
        print("in disp A")
class B(A):
    pass
a1=A()
a1.disp()
b1=B()
b1.disp()
        