import json
import os

class Storage:
    def __init__(self, data_file='finance.json'):
        self.data_file = data_file

    def load_expenses(self):
        """Load data from the JSON file."""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return []

    def save_expenses(self, expenses):
        """Save expenses to the JSON file."""
        with open(self.data_file, 'w') as f:
            json.dump(expenses, f, indent=4)

    def load_budgets(self):
        """Load budgets from the JSON file."""
        budgets_file = 'budgets.json'
        if os.path.exists(budgets_file):
            with open(budgets_file, 'r') as f:
                return json.load(f)
        return {}

    def save_budgets(self, budgets):
        """Save budgets to the JSON file."""
        with open('budgets.json', 'w') as f:
            json.dump(budgets, f, indent=4)