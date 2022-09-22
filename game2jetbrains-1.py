
print("How many pencils would you like to use:")
pencils = int(input())
print("Who will be the first (John, Jack):")
names = str(input())


while pencils > 0:
        print( names + "'s turn:" )
        if names == "John":
            names = "Jack"
        else:
            names = "John"
        print( pencils * "|" )
        pencils2 = int( input() )
        pencils = pencils - pencils2
    

