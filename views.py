#!/usr/bin/env python3
from models import User, Expense
import os
import json

def create_user(user_id, name, filename):
    user = User(user_id, name)
    all_users = User.load_all_users(filename)
    all_users.append(user)
    User.save_to_file(filename, user)
    return user

# def load_all_users(filename):
#     if os.path.exists(filename):
#         try:
#             with open(filename, 'r') as file:
#                 user_data = json.load(file)
#                 if user_data:
#                     return [User(**user_data)]
#                 else:
#                     return []
#         except json.JSONDecodeError:
#             return []
#     else:
        # return []

def show_user(user_id, filename):
    all_users = User.load_all_users(filename)
    for user in all_users:
        if user.user_id == user_id:
            return user
    return None

def add_expense(payer_id, total_amount, users, expense_type, filename, *amounts):
    expense = Expense(payer_id, total_amount, users, expense_type, *amounts)
    all_users = User.load_all_users(filename)
    expense.apply_expense(all_users)
    for user in all_users:
        User.save_to_file(filename, user)


def show_balances(all_users, user_id=None):
    if user_id:
        user = next((user for user in all_users if user.user_id == user_id), None)
        if user:
            print(f"Balances for {user.user_id}:")
            for owed_user_id, amount in user.owes.items():
                print(f"{owed_user_id} owes {user.user_id}: {amount}")
        else:
            print("No balances")
    else:
        for user in all_users:
            print(f"Balances for {user.user_id}:")
            for owed_user_id, amount in user.owes.items():
                print(f"{owed_user_id} owes {user.user_id}: {amount}")
