import multiprocessing as mp
import time
import os


# =========================
# FUNCTION DEFINITIONS
# =========================
def burn_cpu():
    """
    Function to max out a CPU core.
    Runs an infinite loop to simulate 100% CPU usage.
    """
    while True:
        pass  # tight loop consumes CPU


def cpu_test(duration: int = 30):
    """
    Stress all available CPU cores for a specified duration.

    Args:
        duration (int, optional): Stress duration in seconds. Defaults to 30.

    Behavior:
        - Starts one process per CPU core running a tight loop.
        - Runs for `duration` seconds, then terminates all processes.
        - Prints status messages to indicate start and stop.
    """
    cores = os.cpu_count()
    print(f"Stressing {cores} CPU cores for {duration} seconds...")

    processes = []
    for _ in range(cores):
        p = mp.Process(target=burn_cpu)
        p.start()
        processes.append(p)

    try:
        time.sleep(duration)
    finally:
        for p in processes:
            p.terminate()
            p.join()  # ensure clean termination
        print("CPU stress test completed.")


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    cpu_test(duration=30)
import multiprocessing as mp
import time
import os


# =========================
# FUNCTION DEFINITIONS
# =========================
def burn_cpu():
    """
    Function to max out a CPU core.
    Runs an infinite loop to simulate 100% CPU usage.
    """
    while True:
        pass  # tight loop consumes CPU


def cpu_test(duration: int = 30):
    """
    Stress all available CPU cores for a specified duration.

    Args:
        duration (int, optional): Stress duration in seconds. Defaults to 30.

    Behavior:
        - Starts one process per CPU core running a tight loop.
        - Runs for `duration` seconds, then terminates all processes.
        - Prints status messages to indicate start and stop.
    """
    cores = os.cpu_count()
    print(f"Stressing {cores} CPU cores for {duration} seconds...")

    processes = []
    for _ in range(cores):
        p = mp.Process(target=burn_cpu)
        p.start()
        processes.append(p)

    try:
        time.sleep(duration)
    finally:
        for p in processes:
            p.terminate()
            p.join()  # ensure clean termination
        print("CPU stress test completed.")


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    cpu_test(duration=30)
