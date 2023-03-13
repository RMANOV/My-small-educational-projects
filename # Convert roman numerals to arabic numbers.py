# Convert roman numerals to arabic numbers
roman = input("Enter a roman numeral: ")
roman = roman.upper()
arabic = 0

roman_to_arabic = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}

for i in range(len(roman)):
    if i > 0 and roman_to_arabic[roman[i]] > roman_to_arabic[roman[i - 1]]:
        arabic += roman_to_arabic[roman[i]] - 2 * roman_to_arabic[roman[i - 1]]
    else:
        arabic += roman_to_arabic[roman[i]]

print("The arabic number is", arabic)
