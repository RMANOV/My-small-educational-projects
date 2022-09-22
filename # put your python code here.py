# put your python code here

while True:
    try:
        n = int(input())
        break
    except ValueError:
        print("Please enter an integer")
    if n < 10:
        continue
    if n > 100:
        break
    break
    print(n)
