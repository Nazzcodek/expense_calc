#!/usr/bin/env python3
import json
import os

class User:
    def __init__(self, user_id, name, owes=None, is_owed=None):
        self.user_id = user_id
        self.name = name
        self.owes = owes if owes else {}
        self.is_owed = is_owed if is_owed else {}

    def add_owed(self, user_id, amount):
        if user_id in self.is_owed:
            self.is_owed[user_id] -= amount
            if self.is_owed[user_id] <= 0:
                del self.is_owed[user_id]
        else:
            if user_id in self.owes:
                self.owes[user_id] += amount
            else:
                self.owes[user_id] = amount

    def add_is_owed(self, user_id, amount):
        if user_id in self.owes:
            self.owes[user_id] -= amount
            if self.owes[user_id] <= 0:
                del self.owes[user_id]
        else:
            if user_id in self.is_owed:
                self.is_owed[user_id] += amount
            else:
                self.is_owed[user_id] = amount

    @classmethod
    def load_from_file(cls, filename):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                return cls(**data[list(data.keys())[0]])
        except FileNotFoundError:
            return None

    @classmethod
    def save_to_file(cls, filename, user):
        data = []
        if os.path.exists(filename) and os.path.getsize(filename) > 0:
            with open(filename, 'r') as file:
                data = json.load(file)
        
        # Check if the user already exists in the data
        for entry in data:
            if user.user_id in entry:
                # Merge the owes and is_owed dictionaries
                entry[user.user_id]['owes'] = {**entry[user.user_id]['owes'], **user.owes}
                entry[user.user_id]['is_owed'] = {**entry[user.user_id]['is_owed'], **user.is_owed}
                break
        else:
            # Add the new user
            data.append({user.user_id: {'name': user.name, 'owes': user.owes, 'is_owed': user.is_owed}})
        
        with open(filename, 'w') as file:
            json.dump(data, file)

    @classmethod
    def load_all_users(cls, filename):
        if not os.path.exists(filename) or os.path.getsize(filename) == 0:
            return []
        with open(filename, 'r') as file:
            data = json.load(file)
        users = []
        for user_dict in data:
            for user_id, user_data in user_dict.items():
                user = User(user_id, user_data['name'], user_data['owes'], user_data['is_owed'])
                users.append(user)
        return users


class Expense:
    def __init__(self, payer_id, total_amount, users, expense_type, *args):
        self.payer_id = payer_id
        self.total_amount = total_amount
        self.users = users
        self.expense_type = expense_type
        self.amounts = args

    def calculate_amounts(self):
        if self.expense_type == "EQUAL":
            return [round(self.total_amount / len(self.users), 2)] * len(self.users)
        elif self.expense_type == "EXACT":
            if sum(self.amounts) != self.total_amount:
                raise ValueError("Total exact amounts must equal the total amount")
            return [round(amount, 2) for amount in self.amounts]
        elif self.expense_type == "PERCENT":
            total_percent = sum(self.amounts)
            if total_percent != 100:
                raise ValueError("Total percentage must be 100")
            return [round(amount / 100 * self.total_amount, 2) for amount in self.amounts]

    def apply_expense(self, all_users):
        amounts = self.calculate_amounts()
        for i, user_id in enumerate(self.users):
            payer = next((user for user in all_users if user.user_id == self.payer_id), None)
            if payer:
                for user in all_users:
                    if user.user_id == user_id and user_id != self.payer_id:
                        user.add_owed(payer.user_id, amounts[i])
                        payer.add_is_owed(user_id, amounts[i])