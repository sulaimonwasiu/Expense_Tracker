# Expense Tracker

## Overview

The **Expense Tracker** is a command-line application designed to help users manage their personal finances. Users can add, update, delete, and view expenses categorized by type, set monthly budgets, and export their expenses to a CSV file.

## Features

- **Add Expenses**: Record new expenses with descriptions, amounts, and categories.
- **Update Expenses**: Modify existing expenses by updating their details.
- **Delete Expenses**: Remove expenses by their unique ID.
- **List Expenses**: View all recorded expenses, with optional filtering by category.
- **Set Monthly Budgets**: Define a budget for each month and receive warnings if expenses exceed the budget.
- **Monthly Summary**: View a summary of total expenses for a specific month.
- **Export to CSV**: Export all recorded expenses to a CSV file for external analysis.
- **User-Friendly Interface**: Interactive command-line interface with clear prompts and instructions.

## Requirements

- Python 3.x
- Required libraries:
  - `cmd`
  - `argparse`
  - `csv`
  - `datetime`
  - `json`
  - `os`

## Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/sulaimonwasiu/expense-tracker.git
   cd expense-tracker
   ```

2. Run the application:

   ```bash
   python expense_tracker.py
   ```

## Usage

### Commands

- **Add an Expense**
  
  ```bash
  expense-tracker add --description <description> --amount <amount>
  ```

- **Update an Expense**
  
  ```bash
  expense-tracker update --id <id> --description <description> --amount <amount>
  ```

- **Delete an Expense**
  
  ```bash
  expense-tracker delete --id 1
  ```

- **List Expenses**
  
  ```bash
  expense-tracker list [--category <category>]
  ```

- **Set a Monthly Budget**
  
  ```bash
  expense-tracker set_budget --month 10 --amount 500
  ```

- **View Monthly Summary**
  
  ```bash
  expense-tracker summary --month 10
  ```

- **Export Expenses to CSV**
  
  ```bash
  expense-tracker export expenses.csv
  ```

- **Exit the Application**
  
  ```bash
  expense-tracker exit
  ```

### Example

1. Start the application:

   ```bash
   python expense_tracker.py
   ```

2. Add a new expense:

   ```bash
   expense-tracker add --description "Grocery Shopping" --amount 150 --category "Groceries"
   ```

3. View all expenses:

   ```bash
   expense-tracker list
   ```

4. Set a budget for October:

   ```bash
   expense-tracker set_budget --month 10 --amount 600
   ```

5. Check the summary for October:

   ```bash
   expense-tracker summary --month 10
   ```

6. Export expenses to a CSV file:

   ```bash
   expense-tracker export expenses.csv
   ```

## Data Storage

The application stores expenses in a JSON format file (`finance.json`) and budgets in another JSON file (`budgets.json`). These files are created in the same directory as the application upon the first run.

## Contributing

Contributions are welcome! If you have suggestions or want to report issues, feel free to open an issue or a pull request on GitHub.

## License

This project is licensed under the MIT License.

## Contact

For any inquiries, please contact [sulaimonwasiu13@gmail.com].
```

### Key Sections of the README

1. **Overview**: A brief description of the application and its purpose.
2. **Features**: A list of the main functionalities.
3. **Requirements**: Any dependencies or prerequisites for running the application.
4. **Installation**: Instructions on how to set up and run the application.
5. **Usage**: Detailed command usage examples to guide users.
6. **Data Storage**: Explanation of how and where the data is stored.
7. **Contributing**: Information on how others can contribute to the project.
8. **License**: Licensing information for the project.
9. **Contact**: Contact information for further inquiries.
