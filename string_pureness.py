

number_lines = int(input())

for line in range(number_lines):
    pstring = input()

    if "," in pstring or "." in pstring or "_" in pstring:
        print(f"{pstring} is not pure!")
    else:
        print(f"{pstring} is pure.")
  