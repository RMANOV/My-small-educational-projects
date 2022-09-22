menu = True
answer = ""
while menu:
    print("1. Option 1")
    print("2. Option 2")
    print("3. Option 3")
    print("4. Sub-menu")
    print("X. Exit/Quit")
    answer = input("What would you like to do? ")
    print()
    if answer == "1":
        print("you chose option 1")
        print()
    elif answer == "2":
        print("you chose option 2")
        print()
    elif answer == "3":
        print("you chose option 3")
        print()
    elif answer == "4":
        answer4 = True
        while answer4:
            print("You chose the sub-menu:")
            print("1. you chose option 4.1.")
            print("2. you chose option 4.2.")
            print("3. you chose option 4.3")
            print("X. exit/quit")
            print()
            answer = input("What would you like to do? ")
            if answer == "1":
                print("Option 4.1")
                print()
            elif answer == "2":
                print("Option 4.2")
                print()
            elif answer == "3":
                print("Option 4.3")
                print()
            elif answer.lower() == "x":
                print("\nGoodbye") 
                answer4 = None
            else:
               print("\n Not Valid Choice Try again")
    elif answer.lower() == "x":
        print("\nGoodbye") 
