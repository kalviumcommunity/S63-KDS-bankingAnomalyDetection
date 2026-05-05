"""Demo of readable variable naming and comments using basic PEP 8 style."""

print("PEP 8 Naming and Comments Demo")
print("------------------------------")

# Before: unclear variable names
x = 85
temp = 90
val = (x + temp) / 2
print("Before (unclear names) average =", val)

# After: clear snake_case names
math_marks = 85
science_marks = 90

# Use descriptive names so score meaning is clear in reports.
average_score = (math_marks + science_marks) / 2
print("After (clear names) average_score =", average_score)

# Keep pass/fail threshold in a named variable to avoid magic numbers.
pass_threshold = 75

# This condition shows eligibility check for final review.
if average_score >= pass_threshold:
    result_status = "pass"
else:
    result_status = "needs_improvement"

print("result_status =", result_status)
