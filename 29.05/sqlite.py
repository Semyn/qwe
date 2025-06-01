import sqlite3


conn = sqlite3.connect('students.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    major TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    subject TEXT,
    grade INTEGER,
    FOREIGN KEY (student_id) REFERENCES students(id)
)
''')

students_data = [
    ('Alice', 20, 'Computer Science'),
    ('Bob', 22, 'Mathematics'),
    ('Charlie', 21, 'Physics'),
    ('David', 23, 'Chemistry'),
    ('Eve', 20, 'Biology')
]
cursor.executemany('INSERT INTO students (name, age, major) VALUES (?, ?, ?)', students_data)

grades_data = [
    (1, 'Math', 5),
    (1, 'Physics', 4),
    (1, 'Chemistry', 4),
    (2, 'Math', 3),
    (2, 'Physics', 4),
    (2, 'Chemistry', 2),
    (3, 'Math', 5),
    (3, 'Physics', 5),
    (3, 'Chemistry', 4),
    (4, 'Math', 4),
    (4, 'Physics', 3),
    (4, 'Chemistry', 3),
    (5, 'Math', 5),
    (5, 'Physics', 4),
    (5, 'Chemistry', 5)
]
cursor.executemany('INSERT INTO grades (student_id, subject, grade) VALUES (?, ?, ?)', grades_data)

cursor.execute('''
SELECT students.id, students.name, AVG(grades.grade) as average_grade
FROM students
JOIN grades ON students.id = grades.student_id
GROUP BY students.id, students.name
''')
students_avg = cursor.fetchall()
print("Все студенты и их средний балл:")
for student in students_avg:
    print(student)

cursor.execute('''
SELECT students.id, students.name, AVG(grades.grade) as average_grade
FROM students
JOIN grades ON students.id = grades.student_id
GROUP BY students.id, students.name
HAVING average_grade > 4
''')
high_avg_students = cursor.fetchall()
print("\nСтуденты с средним баллом выше 4:")
for student in high_avg_students:
    print(student)

cursor.execute('''
SELECT major, COUNT(*) as num_students
FROM students
GROUP BY major
''')
students_by_major = cursor.fetchall()
print("\nКоличество студентов по специальностям:")
for major_group in students_by_major:
    print(major_group)

conn.close()