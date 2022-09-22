from math import trunc



num =float(input("Enter a number: "))
print("The number is: {} ".format(num,3))


if num%2 == 0:
    print("The number is even") # if the number is even
else:
    print("The number is odd") # if the number is odd

num1=0
num2=0
num3=0
num4=0
num5=0

num2=num%10     # is the last digit  
num3=num%100    # is the last two digits
num4=num%1000   # is the last three digits
num5=num//10000 # is the first four digits   

print("The integer part is {}".format(trunc(num)))  # trunc is used to remove the fractional part
print("The fractional part is {}".format(num - trunc(num))) # the fractional part is the number minus the truncated number
print("The absolute value is {}".format(abs(num)))

print("The last digit is {}".format(num2))
print("The last two digits are {}".format(num3))
print("The last three digits are {}".format(num4))
print("The last four digits are {}".format(num5))


#print every number in new line
print("\n") # print new line
for i in range(1,11):
    print(i)    # print the numbers from 1 to 10 on new line

print("\n")  # print new line
#print every number in one line
for i in range(1,11):
    print(i,end=" ") # print the numbers from 1 to 10 on one line
    # end=" " is used to print the numbers whith thousand separator
    # end="\n" is used to print the numbers on new line

print("\n")  # print new line
#print number with thousand separator
for i in range(10000,11000+1):   # print the numbers with thousand separator
    print(i,end=" ")     # print the numbers with thousand separator
    if i%1000 == 0:
        print("\n")  # print new line if the number is divisible by 1000
