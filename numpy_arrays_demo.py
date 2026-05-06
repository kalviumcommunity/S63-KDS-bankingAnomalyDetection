"""Simple demo of creating and using NumPy arrays from Python lists."""

import numpy as np

print("NumPy Arrays Demo")
print("-----------------")

# 1D NumPy array from Python list
python_list_1d = [1, 2, 3, 4, 5]
array_1d = np.array(python_list_1d)

print("1D Python list:", python_list_1d)
print("1D NumPy array:", array_1d)
print("1D array shape:", array_1d.shape)
print("1D array dtype:", array_1d.dtype)
print()

# 2D NumPy array from nested lists
python_list_2d = [[10, 20, 30], [40, 50, 60]]
array_2d = np.array(python_list_2d)

print("2D Python nested list:", python_list_2d)
print("2D NumPy array:\n", array_2d)
print("2D array shape:", array_2d.shape)
print("2D array dtype:", array_2d.dtype)
print()

# Basic arithmetic operations
print("Arithmetic on 1D NumPy array")
print("array_1d + 2 =", array_1d + 2)
print("array_1d * 3 =", array_1d * 3)
print()

# Python list vs NumPy array behavior
print("List vs NumPy behavior")
print("python_list_1d + [2] ->", python_list_1d + [2])
print("array_1d + 2 ->", array_1d + 2)
