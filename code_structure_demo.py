"""Demo of clean code structure for readability and reuse."""

# Imports at the top
from typing import List

# Setup / variable definitions
student_scores = [78, 85, 92, 88]
passing_score = 80


def calculate_average(scores: List[int]) -> float:
    """Return average score."""
    return sum(scores) / len(scores)


def count_passing(scores: List[int], threshold: int) -> int:
    """Return number of scores that meet or exceed threshold."""
    return sum(1 for score in scores if score >= threshold)


def format_summary(average_score: float, passing_count: int, total_count: int) -> str:
    """Return formatted summary text."""
    return (
        f"Average Score: {average_score:.2f}\n"
        f"Passing Students: {passing_count}/{total_count}"
    )


def main() -> None:
    """Main execution flow."""
    average_score = calculate_average(student_scores)
    passing_count = count_passing(student_scores, passing_score)
    summary = format_summary(average_score, passing_count, len(student_scores))

    print("Code Structure Demo")
    print("-------------------")
    print("Scores:", student_scores)
    print("Passing Threshold:", passing_score)
    print(summary)


if __name__ == "__main__":
    main()
