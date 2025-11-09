import python_to_do_list

def main():
    """Main program loop."""
    tasks = python_to_do_list.load_tasks()
    while True:
        print("\n=== To-Do List Manager ===")
        print("1. Show Tasks")
        print("2. Add Task")
        print("3. Mark Task as Done")
        print("4. Delete Task")
        print("5. Exit")

        choice = input("Choose an option (1–5): ").strip()

        if choice == "1":
            python_to_do_list.show_tasks(tasks)
        elif choice == "2":
            python_to_do_list.add_task(tasks)
        elif choice == "3":
            python_to_do_list.mark_done(tasks)
        elif choice == "4":
            python_to_do_list.delete_task(tasks)
        elif choice == "5":
            print("Exiting To-Do List. Have a productive day!")
            break
        else:
            print("Invalid choice! Please choose between 1–5.")


if __name__ == "__main__":
    main()