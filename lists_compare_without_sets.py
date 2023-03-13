# Description: Compare two lists without using sets
list1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
list2 = [1, 2, 3, 4, 5, 6]

# Check if list2 is sublist in list1 - using in operator
if list2 in list1:
    print("list2 is in list1")
else:
    print("list2 is not in list1")

# Check if list2 is in list1 - using all() method
if all(elem in list1 for elem in list2):
    print("list2 is in list1")
else:
    print("list2 is not in list1")

# Check if any elements of list2 is in list1 - using any() method
if any(elem in list1 for elem in list2):
    print("list2 is in list1")
else:
    print("list2 is not in list1")
