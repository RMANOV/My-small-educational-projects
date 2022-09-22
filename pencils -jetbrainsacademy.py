
print("How many pencils would you like to use:")

pencils = (input())
if ord(pencils) > 33:
    print("The number of pencils should be numeric")
    pencils = int( input() )
    pencils = int( pencils )
    

if 30 < ord(pencils):
    print("The number of pencils should be numeric")
    pencils = int( input())
    pencils = int(pencils)
    

# how to check if the number is positive?
if pencils < 0:
    print("The number of pencils should be positive")
    pencils = int( input() )
    pencils = int(pencils)
    exit()



print("Possible values: '1', '2' or '3'")
print("Too many pencils were taken")





print("Who will be the first (John, Jack):")
names = str(input())

if not names == "John" or names == "Jack":
    print("Choose between *John* and *Jack*")
    names = str(input())
    exit()

while pencils > 0:
        print( names + "'s turn:" )
        if names == "John":
            names = "Jack"
        else:
            names = "John"
        print( pencils * "|" )
        pencils2 = int( input() )
        pencils = pencils - pencils2
    
print("*Winner is -" + names + "won")
