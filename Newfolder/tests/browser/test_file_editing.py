#!/usr/bin/env python3
"""
Test file for demonstrating file editing capabilities
"""

def greet_user(name):
    """Enhanced greeting function with timestamp"""
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Hello, {name}! Current time: {timestamp}")
    return f"Greeting sent to {name} at {timestamp}"

def calculate_sum(a, b):
    """Calculate sum of two numbers"""
    result = a + b
    print(f"The sum of {a} and {b} is {result}")
    return result

# Main execution
if __name__ == "__main__":
    user_name = "Test User"
    greet_user(user_name)
    
    num1 = 10
    num2 = 20
    total = calculate_sum(num1, num2)
    
    print("File editing test completed!")

