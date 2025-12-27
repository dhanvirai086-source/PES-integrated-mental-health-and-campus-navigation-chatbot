'''n=int(input("enter number"))
def factorial(n):
    if n==0:
        return 1
    else:
        return n*factorial(n-1)
print(factorial(n))'''

n=int(input("enter number"))
for i in range(n):
 def fibonacci(n):
  if n<=1:
   return(n)
  else:
   return fibonacci(n-1)+fibonacci(n-2)
print(fibonacci(i))
