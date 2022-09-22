

number_of_orders = int(input())

total_price = 0

for i in range(number_of_orders):
    
    price_per_capsule = float(input())
    days = int(input())
    capsules_per_day = int(input())
    
    if price_per_capsule <= 0 or days <= 0 or 2000 < capsules_per_day <= 0 or 1 > days > 31:
        coffe_price = 0
        continue


    coffe_price = price_per_capsule * capsules_per_day * days
    print(f"The price for the coffee is: ${coffe_price:.2f}")
    total_price = total_price + coffe_price
    

     
    




print(f"Total: ${total_price:.2f}")