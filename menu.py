"""
Provides a basic frontend
revised in previous assignment
added 3 new functions for assignment 4
"""

import sys
import main


# pylint: disable = E0606, C0301


def load_users():
    """
    Loads user accounts from a file
    """
    filename = input("Enter filename of user file: ")
    if not main.load_users(filename):
        print("An error occurred while loading users.")
    else:
        print("Accounts loaded successfully.")


def load_status_updates():
    """
    Loads status updates from a file
    """
    filename = input("Enter filename for status file: ")
    if not main.load_status_updates(filename):
        print("An error occurred while loading status updates.")
    else:
        print("Status updates loaded successfully.")


def add_user():
    """
    Adds a new user into the database
    """
    user_id = input("User ID: ")
    email = input("User email: ")
    user_name = input("User name: ")
    user_last_name = input("User last name: ")
    if main.add_user(user_id, email, user_name, user_last_name, user_collection):
        print("User was successfully added")
    else:
        print("This user already exists!")


def update_user():
    """
    Updates information for an existing user
    """
    user_id = input("User ID: ")
    email = input("User email: ")
    user_name = input("User name: ")
    user_last_name = input("User last name: ")
    if not main.update_user(user_id, email, user_name, user_last_name, user_collection):
        print("An error occurred while trying to update user")
    else:
        print("User was successfully updated")


def search_user():
    """
    Searches a user in the database
    """
    user_id = input("Enter user ID to search: ")
    result = main.search_user(user_id, user_collection)
    if result is False:
        print("ERROR: User does not exist")
    else:
        print(f"User ID: {result.user_id}")
        print(f"Email: {result.user_email}")
        print(f"Name: {result.user_name}")
        print(f"Last name: {result.user_last_name}")


def delete_user():
    """
    Deletes user from the database
    """
    user_id = input("User ID: ")
    if not main.delete_user(user_id, user_collection):
        print("An error occurred while trying to delete user")
    else:
        print("User was successfully deleted")


def add_status():
    """
    Adds a new status into the database
    """
    user_id = input("User ID: ")
    status_id = input("Status ID: ")
    status_text = input("Status text: ")
    if main.add_status(user_id, status_id, status_text, status_collection):
        print("New status was successfully added")
    else:
        print("An error occurred while trying to add new status")


def update_status():
    """
    Updates information for an existing status
    """
    status_id = input("Status ID: ")
    user_id = input("User ID: ")
    status_text = input("Status text: ")
    if not main.update_status(status_id, user_id, status_text, status_collection):
        print("An error occurred while trying to update status")
    else:
        print("Status was successfully updated")


def search_status():
    """
    Searches a status in the database
    """
    status_id = input("Enter status ID to search: ")
    result = main.search_status(status_id, status_collection)
    if result is False:
        print("ERROR: Status does not exist")
    else:
        print(f"User ID: {result.user_id}")
        print(f"Status ID: {result.status_id}")
        print(f"Status text: {result.status_text}")


def delete_status():
    """
    Deletes status from the database
    """
    status_id = input("Status ID: ")
    if not main.delete_status(status_id, status_collection):
        print("An error occurred while trying to delete status")
    else:
        print("Status was successfully deleted")


def quit_program():
    """
    Quits program
    """
    sys.exit()


def search_all_status_updates():
    """
    Looks for a user ID's status updates and displays them for that user.
    """
    user_id = input("Enter user ID: ")
    status_iterator = main.search_all_status_updates(user_id, status_collection)

    # Convert iterator to list to check if it's empty
    status_list = list(status_iterator)

    if not status_list:  # Check if the list is empty
        print("No status updates found for this user.")
        return

    count_len = len(status_list)
    print(f"A total of {count_len} status updates found for {user_id}")

    # Restart the iterator from the list
    status_iterator = iter(status_list)

    count = 0
    while True:
        try:
            status = next(status_iterator)
            count += 1
            while True:
                view_next = input(f"Status #{count}: Would you like to see this update? (Y/N): ").lower()
                if view_next == 'y':
                    print(status.status_text)
                    break  # Exit the nested loop to proceed to the next status
                if view_next == 'n':
                    print("Returning to main menu.")
                    return  # Exit the function and return to the main menu
                print("Invalid option, please enter y or n.")
        except StopIteration:
            print("INFO: You have reached the last update.")
            break  # Exit the main loop when all statuses are reviewed


def filter_status_by_string():
    """
    Looks for status updates containing a string and allows the user to view or delete them.
    """
    search_string = input("Enter the string to search: ").lower()
    status_iterator = main.filter_status_by_string(search_string, status_collection)

    status_list = list(status_iterator)
    if not status_list:
        print(f"No status updates found containing '{search_string}'.")
        return

    print(f"A total of {len(status_list)} status updates found containing '{search_string}'.")

    for count, status in enumerate(status_list, start=1):
        if not review_status(status, count):
            break


def review_status(status, count):
    """
    Reviews and optionally deletes a status update.
    """
    while True:
        view_next = input(f"Status #{count}: Review this status? (Y/N): ").lower()
        if view_next == 'y':
            print(status.status_text)
            if delete_status_prompt(status):
                print("Status deleted.")
            else:
                print("Okay, I won't delete this status.")
        elif view_next == 'n':
            print("Returning to main menu.")
            return False
        else:
            print("Invalid option, please enter y or n.")
            continue
        return True


def delete_status_prompt(status):
    """
    Prompts the user to delete a status update.
    """
    while True:
        delete = input("Delete this status? (Y/N): ").lower()
        if delete == 'y':
            main.delete_status(status.status_id, status_collection)
            return True
        if delete == 'n':
            return False
        print("Invalid option, please enter y or n.")
        continue

def flagged_status_updates():
    """
    Prints all statuses returned by filter_status_by_string
    """
    search_string = input("Enter the string to search: ").lower()
    results = main.filter_status_by_string(search_string, status_collection)

    # convert results to list to look through it
    results_list = list(results)

    if not results_list:
        print(f"No status updates found containing '{search_string}'.")
    else:
        for status_tuple in [(result.status_id, result.status_text) for result in results_list]:
            print(status_tuple)


if __name__ == "__main__":
    user_collection = main.init_user_collection()
    status_collection = main.init_status_collection()
    menu_options = {
        "A": load_users,
        "B": load_status_updates,
        "C": add_user,
        "D": update_user,
        "E": search_user,
        "F": delete_user,
        "G": add_status,
        "H": update_status,
        "I": search_status,
        "J": delete_status,
        "K": search_all_status_updates,
        "L": filter_status_by_string,
        "M": flagged_status_updates,
        "Q": quit_program,
    }
    while True:
        user_selection = input(
            """
                            A: Load user database (do this first at first run)
                            B: Load status database (do this second at first run)
                            C: Add user
                            D: Update user
                            E: Search user
                            F: Delete user
                            G: Add status
                            H: Update status
                            I: Search status
                            J: Delete status
                            K: Search all status updates by user id
                            L: Search all status updates matching a string
                            M: Show all flagged status updates
                            Q: Quit

                            Please enter your choice: """
        ).upper()
        if user_selection.upper() in menu_options:
            menu_options[user_selection]()
        else:
            print("Invalid option")
