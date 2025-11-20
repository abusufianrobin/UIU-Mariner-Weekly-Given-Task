## 📌 Heart Disease Dataset – Data Pre-Processing Questions

### ✅ Questions to Perform:
1. Import the Libraries and Dataset  
2. Display Top 5 Rows of the Dataset  
3. Check the Last 5 Rows of the Dataset  
4. Find Shape of the Dataset (Rows & Columns)  
5. Get Dataset Information (rows, columns, datatypes, memory)  
6. Check Null Values  
7. Check for Duplicate Data and Drop Them  
8. Get Overall Statistics  
9. Draw Correlation Matrix  
10. Count How Many People Have Heart Disease vs. Do Not  
11. Count of Male & Female  
12. Gender Distribution According to Target Variable  
13. Age Distribution  
14. Chest Pain Type Distribution  
15. Chest Pain Distribution per Target Variable  
16. Fasting Blood Sugar Distribution per Target Variable  
17. Resting Blood Pressure Distribution  
18. Compare Resting Blood Pressure by Sex  
19. Distribution of Serum Cholesterol  
20. Plot All Continuous Variables  

---

## ❤️ Heart Disease Dataset – Feature Description

### **🔸 Chest Pain Type (cp)**  
**4 values:**  
1. **0 – Typical Angina**  
2. **1 – Atypical Angina**  
3. **2 – Non-Anginal Pain**  
4. **3 – Asymptomatic**

---

### **🔸 Other Important Features**

- **Age**
- **Sex (0 = Female, 1 = Male)**  
- **Trestbps** – Resting blood pressure (mmHg)  
- **Chol** – Serum cholesterol in mg/dl  
- **fbs** – Fasting blood sugar > 120 mg/dl  
  - `1 = True`, `0 = False`

---

### **🔸 Restecg – Resting Electrocardiographic Results**
1. **0 – Normal**  
2. **1 – ST-T Wave Abnormality**  
3. **2 – Left Ventricular Hypertrophy (Estes Criteria)**

---

### **🔸 Additional Clinical Features**

- **Thalach** – Maximum heart rate achieved  
- **Exang** – Exercise-induced angina (`1 = Yes`, `0 = No`)  
- **Oldpeak** – ST depression induced by exercise  
- **Slope** – Slope of the peak exercise ST segment  
  1. **1 – Upsloping**  
  2. **2 – Flat**  
  3. **3 – Downsloping**
- **Ca** – Number of major vessels (0–3) colored by fluoroscopy  
- **Thal**  
  - `3 = Normal`  
  - `6 = Fixed Defect`  
  - `7 = Reversible Defect`

---

### 🎯 Target Variable
- **0 – Less chance of heart attack**  
- **1 – More chance of heart attack**

---
##  Run the Project in VS Code

Open your VS Code terminal and run:

```bash
pip install -r requirements.txt
python main.py
