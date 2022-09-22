

f_number = int(input())

for i in range (1, f_number + 1):
    for j in range (0, i):
        print("*", end="")
    print()
for i in range (f_number - 1, 0, -1):
    for j in range (0, i):
        print("*", end="")
    print()
    