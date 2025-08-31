import subprocess
import os
from datetime import datetime

def run_tests():
    # Create the output directory if it doesn't exist
    output_dir = "unit_test_results"
    os.makedirs(output_dir, exist_ok=True)

    # Format the filename with current date and time
    filename = datetime.now().strftime("%Y-%m-%d %H-%M-%S_unit_test_results.md")
    filepath = os.path.join(output_dir, filename)

    # Run pytest and capture output
    result = subprocess.run([
        "pytest", "tests/", "--tb=short"
    ], capture_output=True, text=True)

    # Write output to markdown file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("# Unit Test Results\n\n")
        f.write("```")
        f.write(result.stdout)
        f.write("\n```")

    print(f"Test results written to {filepath}")

if __name__ == "__main__":
    run_tests()