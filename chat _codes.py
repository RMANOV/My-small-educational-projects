

n_lines = int(input())

for i in range(n_lines):
    line = int(input())
    if line == 86:
        print("How are you?")
    elif line < 88:
        print("GREAT!")
    elif line == 88:
        print("Hello")
    else:
        print("Bye.")