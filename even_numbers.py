

n_lines = int(input())

for i in range(n_lines):
    number = int(input())
    if not number % 2 == 0:
        print(f'{number} is odd!')
        break
else:
    print(f'All numbers are even.')