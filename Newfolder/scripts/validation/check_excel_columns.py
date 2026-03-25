#!/usr/bin/env python3
"""
Quick script to check all columns in the International_Parent_form_data.xlsx file
"""

import pandas as pd
import os

def check_excel_columns():
    """Check all columns in the International Parent Excel file"""
    excel_file = r"C:\Users\rgunalan\OneDrive - College Board\Documents\GitHub\MyRepo\Newfolder\dsr\data\International_Parent_form_data.xlsx"
    
    print(f"📊 Checking Excel file: {excel_file}")
    
    try:
        # Load the Excel file
        df = pd.read_excel(excel_file, engine='openpyxl', na_filter=True, keep_default_na=True, dtype=str)
        
        print(f"\n✅ Excel file loaded successfully!")
        print(f"📈 Total rows: {len(df)}")
        print(f"📋 Total columns: {len(df.columns)}")
        
        print(f"\n📝 ALL COLUMN NAMES:")
        for i, column in enumerate(df.columns, 1):
            print(f"  {i:2d}. '{column}'")
        
        print(f"\n🔍 SAMPLE DATA (First 3 rows):")
        for i, column in enumerate(df.columns):
            sample_values = df[column].head(3).tolist()
            print(f"  {column}: {sample_values}")
            
        print(f"\n📊 DATA TYPES:")
        for column in df.columns:
            print(f"  {column}: {df[column].dtype}")
        
        return df.columns.tolist()
        
    except Exception as e:
        print(f"❌ Error loading Excel file: {str(e)}")
        return []

if __name__ == "__main__":
    columns = check_excel_columns()
    print(f"\n🎯 Found {len(columns)} columns total")
