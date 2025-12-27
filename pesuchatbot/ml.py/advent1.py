'''def fib(n):
    if n==0:
        return 0
    elif n==1:
        return 1
    else:
        return fib(n-1)+fib(n-2)
print(fib(7))'''

'''import numpy
b=numpy.array([[1,2],[3,4]])
print(b)'''

'''def sum(lst):
    if len(lst)==0:
        return 0
    else:
        return lst[0]+sum(lst[1:])
def avg(lst):
    if len(lst)==0:
        return 0
    else:
        return sum(lst)/len(lst)
numbers=[1,2,3,4]
print(avg(numbers))'''

'''def neg(lst):
    if len(lst)==0:
        return []
    val=lst[0]
    if val<0:
        val=0
    return [val]+neg(lst[1:])
numbers=[-4,4,-6,8]
print(neg(numbers))'''

def rev(x):
    for i in range(len(x)-1, -1, -1):
        yield x[i]
x="python"
gen=rev(x)
for char in gen:
    print(char)




