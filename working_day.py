number_day=int(input("Enter a number: "))


for i in range(1,number_day+1): 
    print("Monday" if i==1 else "Tuesday" if i==2 else "Wednesday" if i==3 else "Thursday" if i==4 else "Friday" if i==5 else "Saturday" if i==6 else "Sunday")
    if i==6 or i==7:
        print("It's the weekend")
    else:
        print("It's a weekday")