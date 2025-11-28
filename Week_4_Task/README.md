# 📘 UIU Mariner — Week 4 Task Report  
**Author:** Abu Sufian Robin  

This repository contains the work completed during **Week 4** of the UIU Mariner project.  
The focus of this week was **Database Integration**, **SQL CRUD operations**, and **Python–MySQL connectivity**, along with GUI implementation using **PyQt**.

---

## 📌 Week 4 Overview

### 🔧 **Focus Area: Database Integration**

| Task Area | Goals | Completed Work | Related Files |
|----------|--------|----------------|---------------|
| **SQL CRUD Operations** | Integrate MySQL with Python | Created student table operations (insert, update, delete, fetch). Connected databases using custom connection functions. | `MySQL_Python_Project_1`, `MySQL_Python_Project_2` |
| **Database Handling** | Build UI using PyQt & SQL | Implemented multi-page UI to show student data in tables. Separated SQL setup file for database creation. | `Multi_page_app`, `UIU_Mariner.sql`, `example.py`, `test_gui.py` |

---

## 📂 Project Details

---

## 🟦 MySQL_Python_Project_1 — Details

This project demonstrates **Python–MySQL connectivity** and **GUI table display using PyQt**.

### ✔ Implemented Features
- `db_connect()` method handles database connection using required credentials.
- `Data_Table.sql` contains SQL table definitions.
- `gui_main.py` implements a PyQt interface to display database table data.
- `crud.py` includes full CRUD operations with SQL queries and permission handling.

### 📁 Key Files
- `db_connect.py`  
- `Data_Table.sql`  
- `gui_main.py`  
- `crud.py`

---

## 🟩 MySQL_Python_Project_2 — Details

A more advanced version with a virtual environment and improved structure.

### ✔ Implemented Features
- All CRUD operations and database connection logic are written in **main.py**.
- Includes **try–except blocks** for safe database connectivity.
- `command.txt` contains instructions for running the project and sample outputs.

### 📁 Key Files
- `main.py`  
- `command.txt`


---

## 🚀 How to Run

### 1️⃣ Install Dependencies
```bash
pip install PyQt5 mysql-connector-python
```

### 2️⃣ Setup Database
Import the SQL file:
```bash
mysql -u root -p < UIU_Mariner.sql
```

### 3️⃣ Run the Project
```bash
python main.py
```

---

## 📝 Summary

In Week 4, the major focus was mastering:

- MySQL and Python Integration  
- CRUD Operations  
- GUI Display using PyQt  
- Multi-page Application Structure  
- Clean Database Handling  

This repository includes all code files, SQL files, and instructions needed to run and understand the work completed.

---
