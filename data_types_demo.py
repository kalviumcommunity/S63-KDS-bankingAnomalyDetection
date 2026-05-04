"""Simple demo of numeric and string data types in Python."""

# Numeric types
age = 21              # int
height = 5.7          # float
bonus_points = 4

total_points = age + bonus_points
half_age = age / 2

print("Numeric Examples")
print("----------------")
print("age =", age, "| type:", type(age))
print("height =", height, "| type:", type(height))
print("total_points =", total_points)
print("half_age =", half_age)
print()

# String types
first_name = "Data"
last_name = "Student"
full_name = first_name + " " + last_name

print("String Examples")
print("---------------")
print("first_name =", first_name, "| type:", type(first_name))
print("full_name =", full_name)
print()

# Mixing types: common mistake and fix
print("Mixing Types")
print("------------")
print("Common mistake: trying to add string + int directly")
print('Example error: "Age: " + age -> TypeError')

correct_message = "Age: " + str(age)
back_to_number = int("10") + 5

print("Correct conversion:", correct_message)
print('int("10") + 5 =', back_to_number)
