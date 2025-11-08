import math

# --- BMI CALCULATOR ---
def calculate_bmi(weight, height):
    """Calculate BMI using weight (kg) and height (m)."""
    try:
        bmi = weight / (height ** 2)
        return round(bmi, 2)
    except ZeroDivisionError:
        return "Error: Height cannot be zero!"
    except Exception as e:
        return f"Unexpected error: {e}"



def calculate_cgpa(grade_points, credit_hours):
    """
    Calculate CGPA using the UIU formula:
    CGPA = (Sum of (grade_point × credit_hour)) / (Sum of credit_hours)
    """
    try:
        total_weighted_points = sum(gp * ch for gp, ch in zip(grade_points, credit_hours))
        total_credits = sum(credit_hours)

        if total_credits == 0:
            return "Error: Total credit hours cannot be zero!"

        cgpa = total_weighted_points / total_credits
        return round(cgpa, 2)

    except ZeroDivisionError:
        return "Error: No courses or invalid data!"
    except Exception as e:
        return f"Unexpected error: {e}"
    

# --- AREA CALCULATORS ---

def area_rectangle(length, width):
    try:
        return length * width
    except Exception as e:
        return f"Error: {e}"

def area_circle(radius):
    try:
        return round(math.pi * radius ** 2, 2)
    except Exception as e:
        return f"Error: {e}"

def area_square(side):
    try:
        return side ** 2
    except Exception as e:
        return f"Error: {e}"

def area_triangle(base, height):
    try:
        return 0.5 * base * height
    except Exception as e:
        return f"Error: {e}"
    
