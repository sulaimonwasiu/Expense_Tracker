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