import datetime
import cmd
from storage import Storage
import argparse
import shlex
import csv

class ExpenseTracker(cmd.Cmd):
    intro = "Welcome. Type 'help' to list commands."
    prompt = 'expense-tracker  '

    def __init__(self):
        super().__init__()
        self.storage = Storage()  # Use the Storage class
        self.expenses = self.storage.load_expenses()
        self.budgets = self.storage.load_budgets()
    
    def arg_parser(self, args):
        """Parse command line arguments using argparse and return them as a dictionary."""
        parser = argparse.ArgumentParser()
        parser.add_argument('--description', type=str, help='Description of the expense')
        parser.add_argument('--amount', type=int, help='Amount of the expense')
        parser.add_argument('--id', type=int, help='ID of the expense to update or delete')
        parser.add_argument('--category', type=str, help='Category of the expense')
        parser.add_argument('--month', type=int, help='Month number to view summary (1-12)')
        
        # Parse the command
        args = parser.parse_args(args)
        
        # Convert Namespace to dictionary
        return vars(args)
    
    def do_set_budget(self, args):
        """Set a monthly budget. Usage: set_budget --month <month_number> --amount <amount>."""
        data = self.arg_parser(shlex.split(args))
        month = data.get('month')
        amount = data.get('amount')

        if month is None or amount is None or not (1 <= month <= 12):
            print("Error: Please provide a valid month (1-12) and amount.")
            return
        
        self.budgets[str(month)] = amount
        self.storage.save_budgets(self.budgets)
        print(f'Set budget of ${amount} for month {month}.')


    def do_add(self, args):
        """Create a new expense. Usage: add --description "Lunch" --amount 20."""
        args = self.arg_parser(shlex.split(args))
        if not args:
            print("Error: Expense cannot be empty.")
            return
        
        data = args.copy()
        description = data.get('description')
        amount = data.get('amount')
        category = args.get('category')

        if not description or not amount or not category:
            print("Error: Description, amount, and category are required.")
            return
        
        # Check budget
        month = datetime.datetime.now().month
        budget = self.budgets.get(str(month), 0)
        total_monthly_expenses = sum(exp['amount'] for exp in self.expenses if 
                                      datetime.datetime.fromisoformat(exp['created_at']).month == month)
        
        if total_monthly_expenses + amount > budget:
            print(f"Warning: Adding this expense will exceed your budget of ${budget} for this month.")
            return

        expense = {
            'id': len(self.expenses) + 1,
            'description': description,
            'amount': amount,
            'category': category,
            'created_at': datetime.datetime.now().isoformat(),
            'updated_at': datetime.datetime.now().isoformat()
        }
        self.expenses.append(expense)
        self.storage.save_expenses(self.expenses)
        print(f'# Expense added successfully (ID: {expense["id"]})')

    def do_delete(self, args):
        """Delete an expense by ID. Usage: delete --id <id>."""
        try:
            #expense_id = self.parse_command_line(args.strip().split()).get('id')
            expense_id = self.arg_parser(shlex.split(args)).get('id')
            ids = [exp['id'] for exp in self.expenses]
            if expense_id in ids:
                self.expenses = [exp for exp in self.expenses if exp['id'] != expense_id]
            else:
                print(f"Expsense with ID {expense_id} does not exist.")
                return
            self.storage.save_expenses(self.expenses)
            print(f'# Expense with ID {expense_id} deleted successfully.')
        except ValueError:
            print("Error: ID must be a number.")

    def do_update(self, args):
        """Update an expense. Usage: update --id <id> --description <new_description> --amount <new_amount>."""
        #args = args.replace('"', '').strip().split()
        args = shlex.split(args)
        data = self.arg_parser(args)

        expense_id = data.get('id')
        if not expense_id or not isinstance(expense_id, int):
            print("Error: Please provide a valid expense ID.")
            return

        expense_id = expense_id
        expense = next((exp for exp in self.expenses if exp['id'] == expense_id), None)

        if expense is None:
            print(f"Error: No expense found with ID {expense_id}.")
            return

        # Update fields if provided
        if 'description' in data:
            expense['description'] = data['description']
        if 'amount' in data:
            try:
                if data['amount'] is not None:
                    expense['amount'] = data['amount']
            except ValueError:
                print("Error: Amount must be a number.")
                return

        expense['updated_at'] = datetime.datetime.now().isoformat()  # Update the timestamp
        self.storage.save_expenses(self.expenses)  # Save the updated expenses
        print(f'# Expense with ID {expense_id} updated successfully.')

    def do_list(self, args):
        """View all expenses. Usage: list [--category <category>]"""

        category_filter = None
        if args:
            data = self.arg_parser(shlex.split(args))
            category_filter = data.get('category')

        if not self.expenses:
            print("No expenses to display.")
            return
        
        # Print the header
        print("-" * 60)
        print(f"{'ID':<4} {'Date':<12} {'Description':<20} {'Amount':<7} {'Category':<15}")
        print("-" * 60)  # Print a separator line
        
        
        for exp in self.expenses:
            # Format the date and amount
            date_str = exp['created_at'][:10]  # Get the date part from the timestamp
            description = exp['description']
            amount = f"${exp['amount']}"
            category = exp.get('category', 'Unknown')

            if category_filter and category != category_filter:
                continue
            
            # Print each expense in the desired format
            print(f"{exp['id']:<4} {date_str:<12} {description:<20} {amount:<7} {category:<15}")


    def do_summary(self, args):
        """View a summary of expenses for a specific month of the current year. 
        Usage: summary [--month <month_number>].
        """
        data = {
            'month': None
        }

        try:
            data = self.arg_parser(shlex.split(args))
            if all(value is None for value in data.values()):
                total_expenses = sum(exp['amount'] for exp in self.expenses)
                print(f'Total Expenses: ${total_expenses}')
                return
        except SystemExit:
            #print("Error: Invalid input. Please ensure you provide a valid month as integer.")
            pass

        month = data.get('month')

        # Mapping of month numbers to their respective names
        month_map = {
            1: 'January',
            2: 'February',
            3: 'March',
            4: 'April',
            5: 'May',
            6: 'June',
            7: 'July',
            8: 'August',
            9: 'September',
            10: 'October',
            11: 'November',
            12: 'December'
        }

        if not month or not (1 <= month <= 12):
            print("Error: Please provide a valid month number (1-12).")
            return

        month_name = month_map[month]
        current_year = datetime.datetime.now().year
        
        monthly_expenses = [
            exp for exp in self.expenses 
            if datetime.datetime.fromisoformat(exp['created_at']).month == month
            and datetime.datetime.fromisoformat(exp['created_at']).year == current_year
        ]

        total_monthly_expenses = sum(exp['amount'] for exp in monthly_expenses)

        if monthly_expenses:
            print(f'Total expenses for {month_name}: ${total_monthly_expenses}')
        else:
            print(f'No expenses found for {month_name}, {current_year}.')

    def do_export(self, args):
        """Export expenses to a CSV file. Usage: export <filename>."""
        filename = args.strip() or 'expenses.csv'
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Description', 'Amount', 'Category', 'Created At'])
            for exp in self.expenses:
                writer.writerow([exp['id'], exp['description'], exp['amount'], exp['category'], exp['created_at']])
        print(f'Expenses exported to {filename} successfully.')


    def do_exit(self, arg):
        """Exit the application. Usage: exit"""
        print('Exiting...')
        return True

    def do_EOF(self, args):
        """Handle the End-of-File condition"""
        return True

    def emptyline(self):
        """Override emptyline to display a blank line before the prompt."""
        print()

if __name__ == "__main__":
    expense_tracker = ExpenseTracker()
    expense_tracker.cmdloop()
