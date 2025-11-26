from crud import insert_student, read_students, update_student, delete_student
from pandas_sql import read_students_pandas, export_to_csv

print("\n==== UIU Mariner Student Management System ====\n")

# Insert sample students
insert_student("Rajib", "rajib@uiu.ac.bd", 23)
insert_student("Tanvir", "tanvir@uiu.ac.bd", 24)

# Read all students
rows = read_students()
print("\n--- Student Records ---")
for row in rows:
    print(row)

# Update a student
update_student(1, "newrajib@uiu.ac.bd")

# Delete a student
delete_student(3)

# Pandas integration
read_students_pandas()

# Export to CSV
export_to_csv()
