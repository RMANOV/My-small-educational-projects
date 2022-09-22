first_number = float(input("Enter first number: "))
second_number = float(input("Enter second number: "))
operatins = input("Enter operation: ")

if first_number==0 and second_number==0 and operatins=="/":
    print("Division by zero is not possible")


if operatins == "+":
    print(first_number + second_number) # Addition
elif operatins == "-":  # Subtraction
    print(first_number - second_number) 
elif operatins == "*":  # Multiplication
    print(first_number * second_number)
elif operatins == "/":  # Division
    print(first_number / second_number)
elif operatins == "%":  # Modulus
    print(first_number % second_number)
elif operatins == "**":  # Exponent
    print(first_number ** second_number)
else:
    print("Invalid operation")
    print("Valid operations: +, -, *, /, %, **")
