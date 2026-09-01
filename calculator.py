def add(x,y):
    return x+y

def sub(x,y):
    return x-y

print("Select operator: 1.Add, 2.Subtract")
choice = input("Enter 1 or 2: ")
num1 = float(input("Enter first number: "))
num2 = float(input("Enter second number: "))

if choice == "1":
    print(num1+num2)
elif choice == "2":
    print(num1-num2)

else:
    print(f"{choice} is not 1 or 2")

