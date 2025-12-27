f = open(r"C:\Users\cbec\Downloads\R31.txt", "r")
a = f.readlines()
lt = []
sum1 = 50
pswrd = 0

for i in a:
    i = i.rstrip()
    i = i.replace("R", "+")
    i = i.replace("L", "-")
    lt.append(int(i))

for i in range(len(lt)):
    sum1 += lt[i]
    if sum1 == 0:
        pswrd += 1

print(pswrd)
print(sum1)







