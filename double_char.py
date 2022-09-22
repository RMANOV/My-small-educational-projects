

end_command = 0

while end_command != "End":
    command = input()
    
    if command == "End":
        break
    
    if command == "SoftUni":       
        continue
    for char in command:
        print(char * 2, end = ""),
    print()
# print()
        
        
        
        
        
        
# print()

# # Задача-2: Напишите функцию, принимающую на вход имя, возраст и город проживания человека
#     for i in range(len(command)):
    
#         # if command[i] == "SoftUni":
#         #     continue
#         # print(command[i:i-(i-1):1], end = ""), print(command[i:i-(i-1):1], end = ""),
#         print(command[i:i-(i-1):i+1], end = ""), print(command[i:i-(i-1):i+1], end = ""),
        
        
#     # print(command[0:i-(i-1):1],end="")
#     # print(command[0:i-(i-1):1],end = "")
#     # print(command[i::1])
    
        
#     # print(command[i::1], end = "")
# print(command[i::1], end = "")
    