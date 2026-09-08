def get_int(pr:str = "Enter a number") -> float: 

    while True: 

        data:str = input(f"{pr}: ") 
        try:
            return float(data)
        except ValueError:
            print("You entered an invalid number. Try again") 


tall1:float = get_int() 
tall2:float = get_int("Enter a second number") 

print(f"{tall1} + {tall2} = {float(tall1)+float(tall2)}") 