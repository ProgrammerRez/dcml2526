import time
import psutil
from typing import List

# =========================
# CONFIGURATION
# =========================
CHUNK_MB = 100       # Allocate 100 MB at a time
MAX_MB = 15000       # Maximum total allocation (adjust based on your system)
SLEEP_SEC = 1        # Pause between allocations (seconds)

chunks: List[bytearray] = []  # Stores allocated memory chunks


# =========================
# FUNCTION DEFINITIONS
# =========================
def ram_test(max_mb: int = MAX_MB,
             chunk_mb: int = CHUNK_MB,
             sleep_sec: int = SLEEP_SEC):
    """
    Perform a RAM stress test by allocating memory in chunks.

    Steps:
        1. Allocate memory repeatedly in `chunk_mb` increments until `max_mb` is reached.
        2. Print current allocated memory and system RAM usage.
        3. Hold allocated memory for 20 seconds.
        4. Release memory cleanly.

    Args:
        max_mb (int): Maximum total memory allocation in MB.
        chunk_mb (int): Size of each memory allocation in MB.
        sleep_sec (int): Seconds to sleep between allocations.
    """
    allocated = 0
    print("Starting memory stress test...")

    try:
        while allocated < max_mb:
            chunks.append(bytearray(chunk_mb * 1024 * 1024))
            allocated += chunk_mb

            vm = psutil.virtual_memory()
            print(f"Allocated: {allocated} MB | RAM used: {vm.percent:.2f}%")

            time.sleep(sleep_sec)

    except MemoryError:
        print("MemoryError encountered — system limit reached.")

    finally:
        print("Holding memory for 20 seconds...")
        time.sleep(20)

        chunks.clear()
        print("Memory released cleanly.")


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    ram_test()
