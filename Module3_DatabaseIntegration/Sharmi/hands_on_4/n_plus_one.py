# ================================================
# HANDS-ON 4: N+1 Problem
# Digital Nurture 5.0 | Module 3
# Name: Sharmi
# ================================================

import psycopg2
import time

# Connect to database
conn = psycopg2.connect(
    host="localhost",
    database="college_db",
    user="postgres",
    password="3125"  # ← change this!
)
cursor = conn.cursor()

# ================================================
# VERSION 1: N+1 Problem (BAD approach)
# ================================================
print("=" * 50)
print("VERSION 1: N+1 Problem")
print("=" * 50)

query_count = 0
start_time = time.time()

# Query 1: Get all enrollments
cursor.execute("SELECT * FROM enrollments")
enrollments = cursor.fetchall()
query_count += 1
print(f"Query 1: Got {len(enrollments)} enrollments")

# N queries: one per enrollment to get student name
for enrollment in enrollments:
    student_id = enrollment[1]  # student_id column
    cursor.execute(
        "SELECT first_name, last_name FROM students WHERE student_id = %s",
        (student_id,)
    )
    student = cursor.fetchone()
    query_count += 1

end_time = time.time()

print(f"Total queries executed: {query_count}")
print(f"Time taken: {round(end_time - start_time, 4)} seconds")
print()

# EXPLANATION:
# 1 query to get enrollments
# + 1 query per enrollment to get student name
# = 1 + 10 = 11 queries total! (N+1 problem)
# With 10,000 enrollments = 10,001 queries! VERY SLOW! ❌

# ================================================
# VERSION 2: Fixed with JOIN (GOOD approach)
# ================================================
print("=" * 50)
print("VERSION 2: Fixed with JOIN")
print("=" * 50)

query_count_v2 = 0
start_time_v2 = time.time()

# Single query with JOIN - gets everything at once!
cursor.execute("""
    SELECT
        e.enrollment_id,
        s.first_name,
        s.last_name,
        c.course_name,
        e.grade
    FROM enrollments e
    JOIN students s ON s.student_id = e.student_id
    JOIN courses c ON c.course_id = e.course_id
""")
results = cursor.fetchall()
query_count_v2 += 1

end_time_v2 = time.time()

print(f"Total queries executed: {query_count_v2}")
print(f"Time taken: {round(end_time_v2 - start_time_v2, 4)} seconds")
print()

# Print results
print("Results:")
print("-" * 60)
for row in results:
    print(f"Enrollment {row[0]}: {row[1]} {row[2]} | {row[3]} | Grade: {row[4]}")

# ================================================
# COMPARISON
# ================================================
print()
print("=" * 50)
print("COMPARISON")
print("=" * 50)
print(f"N+1 Version queries:  {query_count}")
print(f"JOIN Version queries: {query_count_v2}")
print(f"Queries saved:        {query_count - query_count_v2}")
print()
print("With 10,000 enrollments:")
print(f"N+1 Version:  10,001 queries ❌ VERY SLOW!")
print(f"JOIN Version: 1 query        ✅ FAST!")

# Close connection
cursor.close()
conn.close()
