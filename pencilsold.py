
print("How many pencils would you like to use:")
pencils = int(input())
print("Who will be the first (John, Jack):")
names = str(input())
# print ()
# print(names + "s turn")

while pencils > 0:

    if names == "John":
     names = "Jack"
     print(pencils * "|")
     print(names + "s turn:")
     pencils2 = int(input())
     pencils = pencils - pencils2  # decrement pencils
    if names == "Jack":
     names = "John"
     print((pencils)* "|")
     print(names + "s turn:")
     pencils = pencils - pencils2  # decrement pencils



# print("Game over")


    
