n = int(input("Enter number of students: "))
readers = {}

for i in range(n):
    name = input("\nEnter student name: ")
    genres = input("Enter genres (comma separated): ").split(",")
    readers[name] = [g.strip() for g in genres]

genre_map = {}
for student, genres in readers.items():
    for genre in genres:
        genre_map.setdefault(genre, set()).add(student)

avg_map = {}
for genre, students in genre_map.items():
    avg = sum(len(readers[s]) for s in students) / len(students)
    avg_map[genre] = round(avg, 2)

print("\nReversed mapping (genre → students):")
print(genre_map)
print("\nAverage genres per student for each genre:")
print(avg_map)