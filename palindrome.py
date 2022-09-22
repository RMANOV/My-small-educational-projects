user_i = (input())

palindrome = user_i[::-1]
if user_i == palindrome:
    print("Palindrome")
else:
    print("Not palindrome")
