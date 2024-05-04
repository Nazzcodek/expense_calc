#!/usr/bin/env python3
from views import *
from models import User

def main():
    filename = "users.json"
    all_users = User.load_all_users(filename)

    if not all_users:
        print("No users found in the database. Please create a new user.")
    
    while True:
        command = input("Enter command: ")
        parts = command.split()
        if parts[0] == "CREATE" and parts[1] == "USER" and len(parts) > 2:
            user_id = parts[2]
            name = parts[3]
            user = create_user(user_id, name, filename)
            print(f"User {user_id} created with name {name}.")
        elif parts[0] == "EXPENSE":
            payer_id = parts[1]
            total_amount = float(parts[2])
            num_users = int(parts[3])
            users = parts[4:4+num_users]
            expense_type = parts[4+num_users]
            if expense_type in ["EXACT", "PERCENT"]:
                amounts = list(map(float, parts[5+num_users:]))
                if len(amounts) != num_users:
                    print("Error: The number of amounts does not match the number of users.")
                    continue
            else:
                amounts = []
            add_expense(payer_id, total_amount, users, expense_type, filename, *amounts)
        elif parts[0] == "SHOW":
            if len(parts) > 1:
                user_id = parts[1]
                user = next((user for user in all_users if user.user_id == user_id), None)
                if user:
                    if user.owes:
                        for owes_user_id, amount in user.owes.items():
                            print(f"{user_id} owes {owes_user_id}: {amount}")
                    else:
                        print('No balances')
                else:
                    print("User not found.")
            else:
                for user in all_users:
                    if user.owes:
                        for owes_user_id, amount in user.owes.items():
                            print(f"{user.user_id} owes {owes_user_id}: {amount}")
        elif parts[0] == "QUIT" or parts[0] == "q":
            break
        else:
            print("Invalid command")

if __name__ == "__main__":
    main()
