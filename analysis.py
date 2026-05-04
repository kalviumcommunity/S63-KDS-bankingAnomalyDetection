"""Basic data analysis script for PR verification."""

# Sample data
scores = [72, 85, 90, 68, 95]
student_data = {
    "class_name": "data_science_basics",
    "total_students": len(scores),
}

# Basic calculations
total_score = sum(scores)
average_score = total_score / len(scores)
max_score = max(scores)
min_score = min(scores)

# Print clear summary
print("Basic Analysis Summary")
print("----------------------")
print(f"Class: {student_data['class_name']}")
print(f"Student Count: {student_data['total_students']}")
print(f"Scores: {scores}")
print(f"Total Score: {total_score}")
print(f"Average Score: {average_score:.2f}")
print(f"Highest Score: {max_score}")
print(f"Lowest Score: {min_score}")
