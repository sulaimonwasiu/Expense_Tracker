import unittest
from unittest.mock import MagicMock, patch
from expense_tracker import ExpenseTracker  # adjust import based on your file structure
import datetime

class TestExpenseTracker(unittest.TestCase):

    def setUp(self):
        """Set up the ExpenseTracker for testing with mocked storage."""
        self.tracker = ExpenseTracker()
        self.tracker.storage = MagicMock()  # Mock the Storage class
        self.tracker.expenses = []
        self.tracker.budgets = {}
    
    def test_add_expense(self):
        """Test adding a new expense."""
        self.tracker.budgets = {'10': 500}  # Set a budget for October
        args = '--description "Lunch" --amount 20 --category "Food"'
        
        self.tracker.do_add(args)

        self.assertEqual(len(self.tracker.expenses), 1)
        self.assertEqual(self.tracker.expenses[0]['description'], "Lunch")
        self.assertEqual(self.tracker.expenses[0]['amount'], 20)
        self.assertEqual(self.tracker.expenses[0]['category'], "Food")
        self.tracker.storage.save_expenses.assert_called_once()

    
    def test_add_expense_exceeds_budget(self):
        """Test adding an expense that exceeds the budget."""
        self.tracker.budgets = {'10': 20}  # Set a budget for October
        args = '--description "Dinner" --amount 25 --category "Food"'
        
        with patch('builtins.print') as mocked_print:
            self.tracker.do_add(args)
            mocked_print.assert_called_with("Warning: Adding this expense will exceed your budget of $20 for this month.")

    def test_delete_expense(self):
        """Test deleting an expense by ID."""
        self.tracker.expenses = [
            {'id': 1, 'description': 'Lunch', 'amount': 20, 'category': 'Food', 'created_at': '2023-10-01T12:00:00'},
        ]
        
        args = '--id 1'
        self.tracker.do_delete(args)

        self.assertEqual(len(self.tracker.expenses), 0)
        self.tracker.storage.save_expenses.assert_called_once()

    def test_update_expense(self):
        """Test updating an expense."""
        self.tracker.expenses = [
            {'id': 1, 'description': 'Lunch', 'amount': 20, 'category': 'Food', 'created_at': '2023-10-01T12:00:00'},
        ]

        args = '--id 1 --description "Brunch" --amount 25'
        self.tracker.do_update(args)

        self.assertEqual(self.tracker.expenses[0]['description'], "Brunch")
        self.assertEqual(self.tracker.expenses[0]['amount'], 25)
        self.tracker.storage.save_expenses.assert_called_once()

    #@unittest.skip("Skipping this test for now")
    def test_list_expenses(self):
        """Test listing expenses."""
        self.tracker.expenses = [
            {'id': 1, 'description': 'Lunch', 'amount': 20, 'category': 'Food', 'created_at': '2023-10-01T12:00:00'},
            {'id': 2, 'description': 'Groceries', 'amount': 50, 'category': 'Food', 'created_at': '2023-10-02T12:00:00'},
        ]

        with patch('builtins.print') as mocked_print:
            self.tracker.do_list('')
            
            # Check that the print was called correctly
            mocked_print.assert_any_call("-" * 60)
            mocked_print.assert_any_call(f"{'ID':<4} {'Date':<12} {'Description':<20} {'Amount':<7} {'Category':<15}")
            mocked_print.assert_any_call("-" * 60)
            mocked_print.assert_any_call(f"{1:<4} {'2023-10-01':<12} {'Lunch':<20} {'$20':<7} {'Food':<15}")
            mocked_print.assert_any_call(f"{2:<4} {'2023-10-02':<12} {'Groceries':<20} {'$50':<7} {'Food':<15}")

    def test_summary_no_month(self):
        """Test summary when no month is provided."""
        self.tracker.expenses = [
            {'id': 1, 'description': 'Lunch', 'amount': 20, 'category': 'Food', 'created_at': '2023-10-01T12:00:00'},
            {'id': 2, 'description': 'Groceries', 'amount': 50, 'category': 'Food', 'created_at': '2023-10-02T12:00:00'},
        ]

        with patch('builtins.print') as mocked_print:
            self.tracker.do_summary('')
            mocked_print.assert_called_once_with(f'Total Expenses: ${70}')

    #@unittest.skip("Skipping this test for now")
    def test_summary_with_month(self):
        """Test summary for a specific month."""
        self.tracker.expenses = [
            {'id': 1, 'description': 'Lunch', 'amount': 20, 'category': 'Food', 'created_at': '2024-10-01T12:00:00'},
            {'id': 2, 'description': 'Groceries', 'amount': 50, 'category': 'Food', 'created_at': '2024-10-15T12:00:00'},
        ]

        args = '--month 10'
        with patch('builtins.print') as mocked_print:
            self.tracker.do_summary(args)
            mocked_print.assert_called_once_with('Total expenses for October: $70')

    #@unittest.skip("Skipping this test for now")
    def test_export_expenses(self):
        """Test exporting expenses to a CSV file."""
        self.tracker.expenses = [
            {'id': 1, 'description': 'Lunch', 'amount': 20, 'category': 'Food', 'created_at': '2023-10-01T12:00:00'},
        ]
        
        with patch('builtins.open', unittest.mock.mock_open()) as mocked_open:
            self.tracker.do_export('test_expenses.csv')

            # Assert that the file was opened correctly
            mocked_open.assert_called_once_with('test_expenses.csv', mode='w', newline='')
            
            # Get the handle to the mocked file
            handle = mocked_open()
            
            # Check that the header was written once
            handle.write.assert_any_call('ID,Description,Amount,Category,Created At\r\n')
            # Check that the expense row was written once
            handle.write.assert_any_call('1,Lunch,20,Food,2023-10-01T12:00:00\r\n')

            # Verify the total number of write calls
            self.assertEqual(handle.write.call_count, 2)  # Expecting two calls: header + data

    def test_set_budget(self):
        """Test setting a monthly budget."""
        args = '--month 10 --amount 500'
        self.tracker.do_set_budget(args)

        self.assertEqual(self.tracker.budgets['10'], 500)
        self.tracker.storage.save_budgets.assert_called_once()

    def test_set_budget_invalid(self):
        """Test setting an invalid budget."""
        args = '--month 13 --amount 500'  # Invalid month
        with patch('builtins.print') as mocked_print:
            self.tracker.do_set_budget(args)
            mocked_print.assert_called_once_with("Error: Please provide a valid month (1-12) and amount.")

    def test_exit(self):
        """Test exiting the application."""
        with patch('builtins.print') as mocked_print:
            self.assertTrue(self.tracker.do_exit(''))
            mocked_print.assert_called_once_with('Exiting...')

if __name__ == '__main__':
    unittest.main()