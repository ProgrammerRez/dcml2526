import os
import time
import psutil

# =========================
# CONFIGURATION
# =========================
FILE_PATH = "disk_stress_test.bin"
CHUNK_MB = 500
MAX_MB = 15048
SLEEP_SEC = 1


def disk_test(file_path: str = FILE_PATH,
              max_mb: int = MAX_MB,
              chunk_mb: int = CHUNK_MB,
              sleep_sec: int = SLEEP_SEC):
    """
    Perform a disk stress test by writing data in chunks while reporting
    system-level disk usage percentage.

    The test guarantees cleanup of the temporary file, even if interrupted.

    Steps:
        1. Write data to disk in fixed-size chunks up to `max_mb`.
        2. Flush and fsync each write to force physical disk I/O.
        3. Print total written size and current disk usage percentage.
        4. Hold the file for 20 seconds.
        5. Delete the file unconditionally on exit.

    Args:
        file_path (str): Path of the temporary disk test file.
        max_mb (int): Maximum total data to write (MB).
        chunk_mb (int): Size of each write chunk (MB).
        sleep_sec (int): Seconds to sleep between writes.
    """

    total_bytes = max_mb * 1024 * 1024
    chunk_bytes = chunk_mb * 1024 * 1024
    written_bytes = 0

    print("Starting disk stress test...")

    try:
        with open(file_path, "wb") as f:
            while written_bytes < total_bytes:
                remaining = total_bytes - written_bytes
                write_size = min(chunk_bytes, remaining)

                f.write(b"\0" * write_size)
                f.flush()
                os.fsync(f.fileno())

                written_bytes += write_size

                usage = psutil.disk_usage(
                    os.path.dirname(os.path.abspath(file_path)) or "/"
                )

                print(
                    f"Written: {written_bytes // (1024**2)} MB | "
                    f"Disk used: {usage.percent:.2f}%"
                )

                time.sleep(sleep_sec)

        print("Holding disk usage for 20 seconds...")
        time.sleep(20)

    except KeyboardInterrupt:
        print("\nInterrupted by user. Cleaning up...")

    finally:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print("Disk stress file removed successfully.")
        except OSError as e:
            print(f"Failed to remove test file: {e}")


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    disk_test()
