# Python
import time

start = time.time()

sum_val = 0
for i in range(1000):
    sum_val += i

elapsed = int((time.time() - start) * 1000)
print(f"Sum: {sum_val}")
print(f"Elapsed: {elapsed} ms")

time.sleep(0.1)
print("Slept 100ms")
