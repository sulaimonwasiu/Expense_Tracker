import unittest
from unittest.mock import MagicMock
from expense_tracker import ExpenseTracker

class TestExpenseTracker(unittest.TestCase):

    def setUp(self):
        """Set up the ExpenseTracker for testing with mocked storage."""
        self.tracker = ExpenseTracker()
        self.tracker.storage = MagicMock()  # Mock the storage
        
        # Initialize with some mock data
        self.tracker.expenses = [
            {'id': 1, 'description': 'Lunch', 'amount': 20.0, 'created_at': '2024-10-01T12:00:00', 'updated_at': '2024-10-01T12:00:00'},
            {'id': 2, 'description': 'Groceries', 'amount': 50.0, 'created_at': '2024-10-02T12:00:00', 'updated_at': '2024-10-02T12:00:00'},
        ]

    def test_add_expense(self):
        """Test adding an expense."""
        args = '--description "Dinner" --amount 30'
        self.tracker.do_add(args)

        # Verify that the expense was added
        self.assertEqual(len(self.tracker.expenses), 3)
        self.assertEqual(self.tracker.expenses[-1]['description'], 'Dinner')
        self.assertEqual(self.tracker.expenses[-1]['amount'], 30.0)

    def test_delete_expense(self):
        """Test deleting an expense by ID."""
        args = '--id 1'
        self.tracker.do_delete(args)

        # Verify that the expense was deleted
        self.assertEqual(len(self.tracker.expenses), 1)
        self.assertEqual(self.tracker.expenses[0]['description'], 'Groceries')

    def test_update_expense(self):
        """Test updating an expense."""
        args = '--id 2 --description "Weekly Groceries" --amount 55'
        self.tracker.do_update(args)

        # Verify that the expense was updated
        self.assertEqual(self.tracker.expenses[1]['description'], 'Weekly Groceries')
        self.assertEqual(self.tracker.expenses[1]['amount'], 55.0)


    def test_list_expenses(self):
        """Test listing expenses."""
        from io import StringIO
        import sys

        # Redirect stdout to capture print statements
        output = StringIO()
        sys.stdout = output

        self.tracker.do_list('')

        # Reset redirect.
        sys.stdout = sys.__stdout__

        # Check if the output contains the expenses
        output_lines = output.getvalue().strip().split('\n')
        self.assertIn("Lunch", output_lines[3])  # Check if 'Lunch' is in the output
        self.assertIn("Groceries", output_lines[4])  # Check if 'Groceries' is in the output


    def test_summary(self):
        """Test summarizing expenses for a specific month."""
        args = '--month 10'
        from io import StringIO
        import sys

        # Redirect stdout to capture print statements
        output = StringIO()
        sys.stdout = output

        self.tracker.do_summary(args)

        # Reset redirect.
        sys.stdout = sys.__stdout__

        # Check if the output indicates the correct total
        self.assertIn("Total expenses for October: $70.0", output.getvalue())
   
    def tearDown(self):
        """Clean up after each test."""
        pass  # No cleanup needed since we're using mocks


if __name__ == '__main__':
    unittest.main()