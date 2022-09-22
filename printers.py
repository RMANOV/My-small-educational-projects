

f_number = float(input("Enter a number: "))

for i in range(1,11):
    # print(format(f_number*i, ".3f"), end=" ")
    # print(format(f_number*i+1, ".2f"), end="\t")
    # print(format(f_number*i+2, ".1f"), end="\n")
# print in the same line
    print(format(f_number*i, ".3f"), end="\t", flush=True)  # flush is used to print the numbers in the same line
    print(format(f_number*i+1, ".2f"), end="\t", flush=True)   # \t is used to print tabulation
    print(format(f_number*i+2, ".1f"), end="\n", flush=True)    # \n is used to print new line