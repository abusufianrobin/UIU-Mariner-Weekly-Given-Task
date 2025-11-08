import operations

def main():
    print(" Welcome to the Multi-Calculator CLI App ")
    print("""
Available options:
1. BMI Calculator
2. CGPA Calculator
3. Area Calculator (Rectangle, Circle, Square, Triangle)
4. Exit
""")

    while True:
        try:
            choice = int(input("Enter your choice (1-4): "))
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 4.")
            continue
        if choice == 1:
            try:
                weight = float(input("Enter weight in kg: "))
                height = float(input("Enter height in meters: "))
                bmi = operations.calculate_bmi(weight, height)
                print(f"Your BMI is: {bmi}")
            except ValueError:
                print("Invalid input. Please enter numeric values for weight and height.")

        elif choice == 2:
            try:
                num_subjects = int(input("Enter Number of Subjects: "))
                grade_points = []
                credit_hours = []

                for i in range(num_subjects):
                    g = float(input(f"Enter Grade Point for Subject {i+1}: "))
                    c = float(input(f"Enter Credit Hour for Subject {i+1}: "))
                    grade_points.append(g)
                    credit_hours.append(c)

                result = operations.calculate_cgpa(grade_points, credit_hours)
                print(f" Calculated CGPA (UIU Grading System): {result}\n")

            except ValueError:
                print("Invalid input! Enter numeric values only.\n")



        elif choice == 3:
            print("""Area Calculator Options:
1. Rectangle
2. Circle
3. Square
4. Triangle
""")
            try:
                shape_choice = int(input("Enter choice: "))


                if shape_choice == 1:
                    l = float(input("Enter length: "))
                    w = float(input("Enter width: "))


                    print(f" Area of Rectangle: {operations.area_rectangle(l, w)}\n")



                elif shape_choice == 2:

                    r = float(input(" Enter Radius: "))

                    print(f" Area of Circle: {operations.area_circle(r)}\n")



                elif shape_choice == 3:

                    s = float(input(" Enter side: "))
                    print(f" Area of Square: {operations.area_square(s)}\n")


                elif shape_choice == 4:

                    b = float(input(" Enter base: "))
                    h = float(input(" Enter height: "))

                    print(f" Area of Triangle: {operations.area_triangle(b, h)}\n")
                
                else:

                    print("Invalid shape choice!\n")

            except ValueError:

                print("Please enter numeric values!\n")


        elif choice == 4:
            print("Exit!")
            break

        else:
            print("Invalid option! Please choose between 1–4.\n")


if __name__ == "__main__":
    main()