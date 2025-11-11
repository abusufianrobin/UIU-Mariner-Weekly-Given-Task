import wish

def main():
    print("Welcome to the Wishing Card CLI Project!")
    print("""
          Choose your wishing type:
1. Morning
2. Afternoon
3. Evening
4. Night
5. Birthday
6. Marriage Anniversary
7. Exit
""")

    while True:
        try:
            choice = int(input("Enter your choice (1–7): "))
        except ValueError:
            print("Please enter a valid number!\n")
            continue
        if choice == 7:
            print("Exiting... Have a great day!")
            break

        name = input("Enter the name of the person you want to wish: ")
        if choice == 1:
            print(wish.morning_wish(name))
        elif choice == 2:
            print(wish.afternoon_wish(name))
        elif choice == 3:
            print(wish.evening_wish(name))
        elif choice == 4:
            print(wish.night_wish(name))
        elif choice == 5:
            print(wish.birthday_wish(name))         
        elif choice == 6:
            print(wish.anniversary_wish(name))
        else:
            print("Invalid option! Please choose from 1–7.\n")

        print("\n-----------------------------\n")


if __name__ == "__main__":
    main()