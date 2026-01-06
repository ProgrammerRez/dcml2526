import multiprocessing as mp
import time
import os

def burn_cpu():
    while True:
        pass  # tight loop = 100% core usage

if __name__ == "__main__":
    cores = os.cpu_count()
    print(f"Stressing {cores} CPU cores")

    processes = []
    for _ in range(cores):
        p = mp.Process(target=burn_cpu)
        p.start()
        processes.append(p)

    try:
        time.sleep(30)  # stress duration (seconds)
    finally:
        for p in processes:
            p.terminate()
        print("CPU stress stopped")


# import time
# import psutil

# chunks = []
# CHUNK_MB = 100        # allocate 100MB at a time
# MAX_MB = 8000         # cap total allocation (adjust to your RAM)
# SLEEP_SEC = 1

# allocated = 0

# print("Starting memory stress test...")

# try:
#     while allocated < MAX_MB:
#         chunks.append(bytearray(CHUNK_MB * 1024 * 1024))
#         allocated += CHUNK_MB

#         vm = psutil.virtual_memory()
#         print(
#             f"Allocated: {allocated} MB | "
#             f"RAM used: {vm.percent:.2f}%"
#         )

#         time.sleep(SLEEP_SEC)

# except MemoryError:
#     print("MemoryError hit — system limit reached")

# finally:
#     print("Holding memory for 20 seconds...")
#     time.sleep(20)

#     chunks.clear()
#     print("Memory released cleanly")



# import os
# import time

# FILE_PATH = "disk_stress_test.bin"
# FILE_SIZE_MB = 15048   # 2 GB file (adjust if needed)
# CHUNK_MB = 500      # write in chunks
# SLEEP_SEC = 0

# chunk = b"\0" * (CHUNK_MB * 1024 * 1024)

# print("Starting disk stress test...")

# try:
#     # -------------------
#     # WRITE PHASE
#     # -------------------
#     with open(FILE_PATH, "wb") as f:
#         written = 0
#         while written < FILE_SIZE_MB:
#             f.write(chunk)
#             f.flush()
#             os.fsync(f.fileno())
#             written += CHUNK_MB
#             print(f"Written {written} MB")
#             time.sleep(SLEEP_SEC)

#     # -------------------
#     # READ PHASE
#     # -------------------
#     print("Reading file repeatedly...")
#     for _ in range(10):
#         with open(FILE_PATH, "rb") as f:
#             while f.read(1024 * 1024):
#                 pass

#     time.sleep(10)

# finally:
#     if os.path.exists(FILE_PATH):
#         os.remove(FILE_PATH)
#         print("Disk stress file removed")
