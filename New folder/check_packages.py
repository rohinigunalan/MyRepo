#!/usr/bin/env python3

import sys
print("Python is working!")
print(f"Python version: {sys.version}")

try:
    import playwright
    print(f"✅ Playwright version: {playwright.__version__}")
except ImportError:
    print("❌ Playwright not found")

try:
    import pandas
    print(f"✅ Pandas version: {pandas.__version__}")
except ImportError:
    print("❌ Pandas not found")

try:
    import openpyxl
    print(f"✅ Openpyxl version: {openpyxl.__version__}")
except ImportError:
    print("❌ Openpyxl not found")
