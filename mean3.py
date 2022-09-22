a = int(input().strip())
b = int(input().strip())

mean = 0
n = 0

for a in range(a, b + 1):
    if a % 3 == 0:
        mean = mean + a
        n = n + 1
mean = mean / n
print(mean)