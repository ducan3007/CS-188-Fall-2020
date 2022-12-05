import numpy as np
import time

a = np.random.rand(10)
b = np.random.rand(10)

print('a', a)
print('b', b)

start = time. time()

c = np.dot(a, b)
end = time.time()

print(end - start)

print(c)

start = time.time()
d = 0
for i in range(len(a)):
    d += a[i] * b[i]
end = time.time()

print("For-loop time : ", end-start, d)
