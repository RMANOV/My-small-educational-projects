
beer = int(input("How many beers do you have? "))

for i in range(beer):
    print("Take one down, pass it around, ", beer-i-1, " bottles of beer on the wall.")
    print("\n") # print new line
    if i == beer-1:
        print("No more bottles of beer on the wall, no more bottles of beer.")
        print("Go to the store and buy some more, 99 bottles of beer on the wall.")
        print("\n") # print new line
        break
    else:
        print("Take one down, pass it around, ", beer-i-2, " bottles of beer on the wall.")
        print("\n") # print new line
        continue
    