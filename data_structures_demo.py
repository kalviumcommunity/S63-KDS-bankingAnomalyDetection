"""Simple demo of lists, tuples, and dictionaries."""

print("List Demo")
print("---------")
names = ["Asha", "Ravi", "Meera"]
print("Original list:", names)
print("First element:", names[0])

names[1] = "Rohan"          # modify
names.append("Nina")        # add
removed_name = names.pop(0)  # remove

print("After modify/add/remove:", names)
print("Removed element:", removed_name)
print()

print("Tuple Demo")
print("----------")
coordinates = (10.5, 20.3)
print("Tuple value:", coordinates)
print("First coordinate:", coordinates[0])
print("Attempted change: coordinates[0] = 99.9 -> TypeError (tuple is immutable)")
print()

print("Dictionary Demo")
print("---------------")
student = {
    "name": "Asha",
    "age": 20,
    "course": "Data Science"
}
print("Original dictionary:", student)
print("Student name:", student["name"])

student["age"] = 21          # update existing key
student["city"] = "Pune"     # add new key

print("Updated dictionary:", student)
