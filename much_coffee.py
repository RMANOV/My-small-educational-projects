

end_command = 0
coffe_number = 0
end_command = input()




while end_command != "END":

    if end_command == "coding" or end_command == "dog" or end_command == "cat" or end_command == "movie":
            coffe_number += 1
            
    elif end_command == "CODING" or end_command == "DOG" or end_command == "CAT" or end_command == "MOVIE":
            coffe_number += 2

    end_command = input() 
  
if coffe_number >= 5:
    
    print("You need extra sleep")
else:
    
    print(coffe_number)
 

 

  
