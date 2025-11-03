def get_student_mark():
    marks = []
    num_student = int(input("Enter number of students: "))

    for i in range(num_student):
        mark = float(input(f"Enter mark for student {i + 1}: "))
        marks.append(mark)
    return marks

def analyze_marks(marks):
    total = 0
    passed = 0
    for mark in marks:
        total += mark
        if mark >= 55:
            passed += 1
    average = total / len(marks) if marks else 0

    print(f"Total Marks: {sum(marks)}")
    print(f"Average Marks: {average}")
    print(f"Number of Passes: {passed}/{len(marks)}")

def main():
    marks = get_student_mark()
    analyze_marks(marks)

main()
