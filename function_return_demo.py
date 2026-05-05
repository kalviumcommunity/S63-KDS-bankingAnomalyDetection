"""Demo: passing data into functions and returning results."""


def add_numbers(a, b):
    """Return sum of two numbers."""
    return a + b


def calculate_average(values):
    """Return average of a numeric list."""
    return sum(values) / len(values)


print("Function Parameters and Return Demo")
print("-----------------------------------")

# Function calls with different arguments
sum_1 = add_numbers(10, 5)
sum_2 = add_numbers(7, 3)
print("sum_1 =", sum_1)
print("sum_2 =", sum_2)

scores = [80, 90, 70, 100]
avg_score = calculate_average(scores)
print("average score =", avg_score)

# Reuse returned values in further calculations
combined_total = sum_1 + sum_2
final_metric = combined_total * avg_score

print("combined_total =", combined_total)
print("final_metric =", final_metric)
