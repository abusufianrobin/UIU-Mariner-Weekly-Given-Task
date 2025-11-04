num1 = int(input("Enter the 1st Number: "))
num2 = int(input("Enter the 2nd Number: "))

add = num1 + num2
print("Two Numbers Addition Result: ", add)

sub = num1 - num2
print("Two Numbers Subtraction Result: ", sub)

if num1 > num2:
    div = num1 / num2
    print("Two Numbers Division Result: ", div)
elif num1 < num2:
    div = num2 / num1
    print("Two Numbers Division Result: ", div)
else:
    print("Both numbers are equal.")

multiply = num1 * num2
print("Two Numbers Multiplication Result: ", multiply)