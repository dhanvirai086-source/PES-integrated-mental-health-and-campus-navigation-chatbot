n = int(input("Enter number of students: "))
readers = {}

for i in range(n):
    name = input("\nEnter student name: ")
    genres = input("Enter genres (comma separated): ").split(",")
    readers[name] = [g.strip() for g in genres]

result = {}

for student, g_list in readers.items():
    for g in g_list:
        result.setdefault(g, set()).add(student)

print("\nOutput:")
print(result)