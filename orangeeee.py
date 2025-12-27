n = int(input("Enter number of students: "))
readers = {}

# Taking input
for i in range(n):
    name = input("\nEnter student name: ")
    genres = input("Enter genres (comma separated): ").split(",")
    readers[name] = [g.strip() for g in genres]

# Reverse mapping: genre → students
genre_map = {}
for student, genres in readers.items():
    for genre in genres:
        genre_map.setdefault(genre, set()).add(student)

# Average genres per student for each genre
avg_map = {}
for genre, students in genre_map.items():
    avg = sum(len(readers[s]) for s in students) / len(students)
    avg_map[genre] = round(avg, 2)

# Store both in a tuple and print
result = (genre_map, avg_map)
print("\nFinal Output (Tuple of Dictionaries):")
print(result)