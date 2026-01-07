from tests import cpu_test, ram_test, disk_test # type: ignore
from typing import Callable

# =========================
# FUNCTION DEFINITIONS
# =========================
def run_test(mode: str = 'cpu') -> None:
    """
    Run a system stress test based on the selected mode.

    Args:
        mode (str): One of 'cpu', 'ram', or 'disk'. Defaults to 'cpu'.

    Behavior:
        - Executes the corresponding stress test function.
        - Catches KeyboardInterrupt to stop the test without exiting the script.
    """
    # Map mode strings to functions (do not call them yet)
    tests: dict[str, Callable[[], None]] = {
        'cpu': cpu_test.cpu_test,
        'ram': ram_test.ram_test,
        'disk': disk_test.disk_test
    }

    if mode not in tests:
        print(f"Invalid mode '{mode}'. Choose from {list(tests.keys())}.")
        return

    try:
        print(f"Starting {mode} stress test. Press Ctrl+C to stop this test...")
        tests[mode]()  # run the selected test
    except KeyboardInterrupt:
        print(f"\n{mode.upper()} test canceled by user.")


# =========================
# MAIN
# =========================
if __name__ == '__main__':
    print("System Stress Test Runner (CTRL+C cancels a test, not the script)")

    while True:
        mode_input = input("Enter mode to run ('cpu', 'ram', 'disk') or 'exit' to quit: ").strip().lower()
        if mode_input == 'exit':
            print("Exiting stress test runner.")
            break

        run_test(mode_input)
