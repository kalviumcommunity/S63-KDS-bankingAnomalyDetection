"""Simple demo of for and while loops in Python."""

print("Loops Demo")
print("----------")

# 1) for loop with range
print("1) for loop with range (1 to 5)")
for number in range(1, 6):
    print(number)
print()

# 2) for loop with list
print("2) for loop with list")
names = ["Asha", "Ravi", "Meera"]
for name in names:
    print("Name:", name)
print()

# 3) continue example
print("3) continue example (skip value 3)")
for value in range(1, 6):
    if value == 3:
        continue
    print("Value:", value)
print()

# 4) break example
print("4) break example (stop at value 4)")
for value in range(1, 8):
    if value == 4:
        print("Stopping loop at", value)
        break
    print("Value:", value)
print()

# 5) while loop with safe termination
print("5) while loop with safe termination")
count = 1
while count <= 5:
    print("Count:", count)
    count += 1
print("Loop ended safely")
