"""Simple demo of conditional statements in Python."""

print("Conditional Statements Demo")
print("---------------------------")

# 1) Basic if statement (numeric condition)
num = 7
print("1) Basic if statement")
if num > 0:
    print(f"{num} is positive")
print()

# 2) if-else example
temperature = -2
print("2) if-else example")
if temperature >= 0:
    print("Temperature is above or equal to 0")
else:
    print("Temperature is below 0")
print()

# 3) if-elif-else with multiple conditions (grade system)
marks = 78
print("3) if-elif-else example")
if marks >= 90:
    grade = "A"
elif marks >= 75:
    grade = "B"
elif marks >= 60:
    grade = "C"
else:
    grade = "D"
print(f"Marks: {marks}, Grade: {grade}")
print()

# 4) Logical operators: and, or, not
age = 20
attendance = 82
has_id_card = False

print("4) Logical operators")
if age >= 18 and attendance >= 75:
    print("Using 'and': Eligible for exam")
else:
    print("Using 'and': Not eligible for exam")

if age < 18 or attendance < 75:
    print("Using 'or': Needs special approval")
else:
    print("Using 'or': No special approval needed")

if not has_id_card:
    print("Using 'not': ID card is missing")
else:
    print("Using 'not': ID card is available")
