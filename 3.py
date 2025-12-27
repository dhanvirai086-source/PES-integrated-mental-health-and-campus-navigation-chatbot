'''import csv
filepath=r"C:\Users\cbec\Desktop\file.csv"
with open(filepath,"r") as fp1:
    reader = csv.reader(fp1)
    header = next(reader)
    for row in reader:
        print(row)'''

count=0
import csv
with open("matches.csv","r") as fp1:
    reader=csv.reader(fp1)
    next(reader)
    for row in reader:
        if 2000<=int(row[1]):
            if row[10] not in d: