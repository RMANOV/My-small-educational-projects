

budjet = int(input())
command = input()

while command != "End" :
    if budjet < int(command):
        print("You went in overdraft!")
        # print(f"You need {int(command) - budjet} leva!")
        break
    budjet -= int(command)
    command = input()
else:
    print("You bought everything needed.")
    # print(f"You have {budjet} leva left!")