import random
from datetime import datetime, timedelta

# Generate 15 random dates in 2009
birthdates = []
start_date = datetime(2009, 1, 1)
end_date = datetime(2009, 12, 31)

for i in range(15):
    # Generate random number of days between start and end
    days_between = (end_date - start_date).days
    random_days = random.randint(0, days_between)
    random_date = start_date + timedelta(days=random_days)
    
    # Format as mddyyyy (month without leading zero, day with leading zero if needed, year)
    month = random_date.month
    day = random_date.day
    year = random_date.year
    formatted_date = f"{month}{day:02d}{year}"
    
    birthdates.append({
        "Birthdate": formatted_date,
        "Readable Date": random_date.strftime("%B %d, %Y")
    })

# Print the birthdates
print("15 Random Birthdates for 2009 (format: mddyyyy):")
print("-" * 50)
for i, bd in enumerate(birthdates, 1):
    print(f"{i:2d}. {bd['Birthdate']:10s} ({bd['Readable Date']})")
