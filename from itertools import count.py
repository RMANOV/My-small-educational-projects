from itertools import count


string = ""
for i in range(1, 20, 4):
    string += "&" * i


print(string)
print(i)