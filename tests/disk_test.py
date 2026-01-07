import os
import time

# =========================
# CONFIGURATION
# =========================
FILE_PATH = "disk_stress_test.bin"
FILE_SIZE_MB = 15048  # Total size to write (MB). Adjust as needed.
CHUNK_MB = 500        # Write in chunks of this size
SLEEP_SEC = 0         # Sleep between chunk writes (seconds)


# =========================
# FUNCTION DEFINITIONS
# =========================
def disk_test(file_path: str = FILE_PATH,
              file_size_mb: int = FILE_SIZE_MB,
              chunk_mb: int = CHUNK_MB,
              sleep_sec: int = SLEEP_SEC):
    """
    Perform a disk stress test by writing and reading a large file.

    Steps:
        1. Write a file of `file_size_mb` in `chunk_mb` increments.
        2. Flush and sync each chunk to disk to ensure actual write.
        3. Optionally sleep between writes.
        4. Read the file repeatedly to stress the disk I/O.
        5. Delete the file after testing.

    Args:
        file_path (str): Path of the file to create for testing.
        file_size_mb (int): Total size of the file to write in MB.
        chunk_mb (int): Size of each write chunk in MB.
        sleep_sec (int): Seconds to sleep between writing chunks.
    """
    chunk = b"\0" * (chunk_mb * 1024 * 1024)  # Memory chunk for writing

    print("Starting disk stress test...")

    try:
        # -------------------
        # WRITE PHASE
        # -------------------
        with open(file_path, "wb") as f:
            written = 0
            while written < file_size_mb:
                f.write(chunk)
                f.flush()
                os.fsync(f.fileno())
                written += chunk_mb
                print(f"Written {written} MB")
                time.sleep(sleep_sec)

        # -------------------
        # READ PHASE
        # -------------------
        print("Reading file repeatedly to stress disk I/O...")
        for _ in range(10):
            with open(file_path, "rb") as f:
                while f.read(1024 * 1024):  # Read in 1MB chunks
                    pass

        time.sleep(10)  # Optional pause after read phase

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
            print("Disk stress file removed successfully.")


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    disk_test()
