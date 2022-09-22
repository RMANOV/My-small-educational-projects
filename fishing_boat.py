


budjet = int(input("Enter your budjet: "))
season = input("Enter the season: ")
num_fishmen = int(input("Enter the number of fishmen: "))

price_boat = 0

#if season == "Spring":
#    price_boat = 3000
#elif season == "Summer" or season == "Autumn":
#    price_boat = 4200
#elif season == "Winter":
#    price_boat = 2600

if season == "Spring": price_boat = 3000  
if season == "Summer": price_boat = 4200
if season == "Autumn": price_boat = 4200
if season == "Winter": price_boat = 2600

# if num_fishmen > 6:
#     price_boat *= 0.9
#     if 7< num_fishmen >= 11:
#         price_boat *= 0.85
#         if num_fishmen > 11:
#             price_boat *= 0.8

if num_fishmen > 11:
    price_boat *= 0.8
elif 7< num_fishmen >= 11:
    price_boat *= 0.85
elif num_fishmen <= 6:
    price_boat *= 0.9


# price_boat = price_boat * num_fishmen

dif = budjet - price_boat



if dif >= 0:
    print("Yes! You have got a fishing boat for {0:.2f} lv.".format(price_boat))
    print("Left: {0:.2f} lv.".format(dif))      
else:
    print("Not enough money! You need {0:.2f} lv. more.".format(price_boat - budjet))
    print("Left: {0:.2f} lv.".format(dif))
