# 📊 DATA FILES INFORMATION - OneTrust Automation

## 📁 FILE LOCATIONS & DETAILS

### 📂 Project Directory:
```
C:\Users\rgunalan\OneDrive - College Board\Documents\GitHub\MyRepo\New folder
```

### 📄 Data Files:

#### 1. **form_data.xlsx** (Primary Data Source)
- **Full Path**: `C:\Users\rgunalan\OneDrive - College Board\Documents\GitHub\MyRepo\New folder\form_data.xlsx`
- **Size**: 355 bytes
- **Last Modified**: July 24, 2025, 11:49 PM
- **Type**: Excel file (requires engine='openpyxl')
- **Status**: Sometimes corrupts ("File is not a zip file" error)
- **Usage**: Primary data source for automation

#### 2. **form_data.csv** (Backup Data Source)  
- **Full Path**: `C:\Users\rgunalan\OneDrive - College Board\Documents\GitHub\MyRepo\New folder\form_data.csv`
- **Size**: 355 bytes  
- **Last Modified**: July 24, 2025, 11:49 PM
- **Type**: CSV file (always reliable)
- **Status**: Backup when Excel fails
- **Usage**: Auto-fallback data source

## 📋 DATA CONTENT

### **Column Structure:**
```csv
Email Address,First_Name,Last_Name,birthDate,phone,country,stateOrProvince,postalCode,city,streetAddress,studentSchoolName,studentGraduationYear,educatorSchoolAffiliation,Request_type
```

### **Sample Data (Row 1):**
- **Email Address**: ethan.mitchell@mailinator.com
- **First_Name**: Ethan  
- **Last_Name**: Mitchell
- **birthDate**: 11/8/2004
- **phone**: 5712345572
- **country**: US
- **stateOrProvince**: Colorado ⭐ (Critical field)
- **postalCode**: 80209-3456
- **city**: Denver
- **streetAddress**: 1625 Cherry Creek Drive, Apt 3C
- **studentSchoolName**: Cherry Creek High School
- **studentGraduationYear**: 2022
- **educatorSchoolAffiliation**: N/A
- **Request_type**: Request a copy of my data

## 🔧 TECHNICAL DETAILS

### **Excel File Reading:**
```python
# Correct way to read Excel file
df = pd.read_excel("form_data.xlsx", engine='openpyxl')
```

### **CSV File Reading:**
```python
# Fallback CSV reading
df = pd.read_csv("form_data.csv")
```

### **Data Access:**
```python
# Get first row as dictionary
data = df.iloc[0].to_dict()

# Access specific field
state = data.get('stateOrProvince', 'New York')
```

## 🚨 COMMON ISSUES & SOLUTIONS

### **Excel Corruption:**
- **Error**: "File is not a zip file"
- **Solution**: Scripts auto-fallback to CSV
- **Manual Fix**: Run `python fix_excel.py`

### **File Not Found:**
- **Check**: Both files exist in project directory
- **Verify**: Current working directory is correct
- **Ensure**: Relative paths work from project root

### **Data Format Issues:**
- **Excel**: Must use `engine='openpyxl'`
- **CSV**: Standard pandas reading works
- **Encoding**: UTF-8 (default)

## 🎯 AUTOMATION USAGE

### **State Selection (Critical):**
- **Field**: stateOrProvince
- **Value**: "Colorado"
- **Dropdown**: Uses improved selection logic
- **Fallback**: Multiple selection methods

### **Form Target:**
- **URL**: OneTrust Privacy Portal
- **Form Type**: Data subject rights request
- **Success Message**: "Thank you for your interest in submitting..."

## 📍 FILE MANAGEMENT

### **Creating New Excel File:**
```python
# Recreate Excel from CSV
df = pd.read_csv("form_data.csv")
df.to_excel("form_data.xlsx", index=False, engine='openpyxl')
```

### **Verifying File Content:**
```python
# Quick verification
import pandas as pd
df = pd.read_excel("form_data.xlsx", engine='openpyxl')
print(df.iloc[0]['stateOrProvince'])  # Should print: Colorado
```

### **Backup Strategy:**
- ✅ CSV file always maintained as backup
- ✅ Scripts handle Excel corruption automatically  
- ✅ `fix_excel.py` recreates Excel from CSV

---
**File Documentation Created**: January 2025
**Last File Update**: July 24, 2025, 11:49 PM
**Current Status**: Working with both Excel and CSV fallback
