
f_number = float(input("Enter a number: "))

if -100 < f_number < 100:
    for i in range(1,4):
        print(f'Valid number : {f_number:.3f}', end='\t')
        print(format(f_number*i, ".3f"), end="\t", flush=True)
        print(format(f_number*i+1, ".2f"), end="\t", flush=True)
        print(format(f_number*i+2, ".1f"), end="\n", flush=True)
else:
    print("Invalid number")
    print("\n") # print new line
    