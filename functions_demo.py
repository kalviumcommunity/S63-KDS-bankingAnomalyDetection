"""Simple demo of Python functions."""

# Global variable (for scope example)
project_name = "functions_pr_demo"


def show_welcome():
    """Function with no parameters."""
    print("Welcome to the Python functions demo")


def calculate_sum(a, b):
    """Function with parameters."""
    result = a + b  # local variable
    return result


def check_even_odd(number):
    """Function with parameter and conditional logic."""
    if number % 2 == 0:
        return "even"
    return "odd"


print("Functions Demo")
print("--------------")

# Function calls
show_welcome()

num1 = 12
num2 = 8
total = calculate_sum(num1, num2)
print(f"Sum of {num1} and {num2} is {total}")

value = 7
status = check_even_odd(value)
print(f"{value} is {status}")

print(f"Global variable example: {project_name}")
