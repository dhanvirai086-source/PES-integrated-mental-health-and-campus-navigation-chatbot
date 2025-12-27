'''
def outer(a):
    def inner(b):
        return(a+b)
    return inner
f=outer(10)
print(f(5))'''


'''def outer(a):
    if len(a)==0:
      return""
    return 
        return(b)
    return inner
f=outer("hello")
print(f(outer))'''

'''def num(n):
    if n==0:
      return 1
    return n*num(n-1)
print(num(5))'''

'''def gcd(m,n):
    if m==n:
        return m
    elif m>n:
        return gcd(m-n,n)
    else:
        return gcd(m,n-m)
print(gcd(4,8))'''

'''def fib(n):
    if n<=1:
        return n
    return fib(n-1)+fib(n-2)
terms=int(input("enter no. of terms"))
for i in range (terms):
  print(fib(i))'''

'''def TowerOfHanoi(n, src, aux, dest):
  if n==1:
     print ("Move disk 1 from source",src,"to destination",dest) 
     return TowerOfHanoi(n-1, src, dest, aux)
  print ("Move disk",n,"from source",src,"to destination",dest)
  TowerOfHanoi(n-1, aux, src, dest)
n=int(input("Enter number of disks\n")) 
TowerOfHanoi(n, 'A', 'B', 'C')'''

'''def TowerOfHanoi(n, src, aux, dest):
    if n == 1:
        print("Move disk 1 from source", src, "to destination", dest)
    return TowerOfHanoi(n-1, src, dest, aux)
    print("Move disk", n, "from source", src, "to destination", dest)
    TowerOfHanoi(n-1, aux, src, dest)



n = int(input("Enter number of disks: "))
TowerOfHanoi(n, 'A', 'B', 'C')'''


'''def add(x,y):
    if x==y:
        return 2*x
    else:
        return x+y
print(add(4,4))'''

'''def sub(x,y):
    if y==0:
        return x
    else:
        return x-y
print(sub(4,4))'''

'''def mul(x,y):
    if y==0:
        return 0
    else:
        return x*y
print(mul(4,4))'''

'''def div(x,y):
    if y==0:
        return ("infinite")
    else:
        return x/y
print(div(5,0))'''

'''def test(i,j):
 if(i==0):
  return j
 else:
   return test(i-1,i+j)
print(test(4,7))'''

'''def fun(x, y) : 
  if x == 0 : 
    return y 
  else : 
    return fun(x - 1, x * y) 
print(fun(4, 2))'''

'''def list(n):
    a=0
    if n==0:
        return 0 
    else:
      for i in range (n):
        return a+i
print(list[2,3,4])'''

def greet():
    return f"good morning:(name)"    
       