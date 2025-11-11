# 🧑‍💻 UIU Mariner - Week 2 Task Report

## 📘 Overview
This repository contains the **Week 2 task submissions** for the UIU Mariner program.  
The main focus of this week’s work was on **Functions**, **Exception Handling**, and building small **Python CLI Projects**.

---

## 🎯 Objectives
- Learn **modular programming** using Python functions.  
- Understand **scope, arguments, and return values**.  
- Implement **error handling** using `try-except` blocks.  
- Build **CLI-based mini projects** demonstrating these concepts.

---

## 📂 Project Files
| Project Name | Description | Main Files |
|---------------|-------------|-------------|
| **Wishing_Card_CLI_Project** | CLI project to display wishing messages (Morning, Noon, Afternoon, Night, Birthday, Anniversary). | `main.py`, `wish.py`, `use_case.txt` |
| **Python_CLI_Project** | Task management CLI application with argument handling and file storage. | `main.py`, `python_to_do_list.py`, `tasks.json`, `use_case.txt` |
| **Python_Operations** | Mathematical and object-based operation CLI with exception handling. | `main.py`, `operations.py`, `use_case.txt` |
| **Python_Function** | Demonstration of Python function usage with modular code. | `python_function.py` |

---

## 🧠 Concepts Implemented

### 🔹 Functions
A **function** in Python is a reusable block of code designed to perform a single task.
- Promotes **code reusability** and **modularity**.
- Example features implemented:
  - Parameter passing
  - Return values
  - Function calling
  - Global and local variable scopes

### 🔹 Scope
- **Global Scope:** Accessible throughout the program.  
- **Local Scope:** Accessible only inside a function.

### 🔹 Arguments
- **Parameters** → Defined in function declaration.  
- **Arguments** → Actual values passed during function call.

### 🔹 Return Values
- Functions return computed results to the caller using `return`.
- If no return is specified, Python implicitly returns `None`.

### 🔹 Try–Except Handling
Used to manage **runtime errors** gracefully.
```python
try:
    # Code that may cause an error
    result = divide(x, y)
except ZeroDivisionError as e:
    print("Error:", e)
