def add(x,y):
    return x+y

def sub(x,y):
    return x-y

def mult(x,y):
    return x*y

def div(x, y):
    return x/y


while True:
    print("Select operator: 1.Add, 2.Subtract, 3.Multi, 4.Division \n If you want to stop the program: Press X")
    choice = input("Enter 1, 2, 3 or 4: ")
    if choice == "x":
        break
    #break choice on x

    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))

    #try while loop so the program doesnt close when finshed. 
    #Update: when only "While True" it ran infinite. Need ot move input into the while loop.

    if choice == "1":
        print(num1+num2)
    elif choice == "2":
        print(num1-num2)
    elif choice == "3":
        print(num1*num2)
    elif choice == "4":
        print(num1/num2)

    else:
        print(f"{choice} is not a choice")

    

