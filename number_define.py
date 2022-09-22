

k_number = float(input())

if k_number > 0:
    if k_number < 1 and k_number > 0:
        print("small positive")
    elif k_number > 1000000:
        print("large positive")
    else:
        print("positive")
elif k_number < 0:
    if k_number > -1 and k_number < 0:
        print("small negative")
    elif k_number < -1000000:
        print("large negative")
    else:
        print("negative")
else:
    print("zero")
    
