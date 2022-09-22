n = int(input().strip())
means_final = 0

for _ in range(1, n + 1):
    means = int(input().strip())
    means_final += means
    
print(means_final / n)
