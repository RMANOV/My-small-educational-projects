

f_string = input()
s_string = input()
last_printed = f_string

for char in range(len(f_string)):

    left_part = s_string[:char + 1]
    right_part = f_string[char+1:]
    curr_string = left_part + right_part
    if curr_string != last_printed:
        print(curr_string)
        last_printed = curr_string
    else:
        continue