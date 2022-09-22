
student = input()
end_command = 0

while end_command != "Welcome!":

    if student == "Voldemort":
        print(f'You must not speak of that name!')
        break

    if student == "Welcome!":
        print(f'Welcome to Hogwarts.')
        break

    if len(student) < 5:
        print(f'{student} goes to Gryffindor.')

    if len(student) == 5:
        print(f'{student} goes to Slytherin.')

    if len(student) == 6:
        print(f'{student} goes to Ravenclaw.')

    if len(student) > 6:
        print(f'{student} goes to Hufflepuff.')
    
    student = input()