

f_number = float(input())

while f_number < 1 or f_number > 100:
    f_number = float(input())
    continue
print(f'The number {f_number} is between 1 and 100')