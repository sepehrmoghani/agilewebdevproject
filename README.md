# Financial Tracker

A comprehensive web application for managing personal finances, built with Flask and SQLAlchemy.

## Features

- **User Authentication**: Secure signup and login system
- **Transaction Management**: 
  - Upload transactions via CSV
  - Manual transaction entry
  - Multi-select and bulk delete transactions
  - Transaction history with pagination and sorting
- **Budgeting**: Create and manage budgets across different categories
- **Goal Setting**: 
  - Set financial goals with deadlines
  - Track progress towards goals
  - Public/private goal sharing
- **Analytics Dashboard**:
  - Monthly spending analysis
  - Category-wise expense breakdown
  - Visual charts and graphs
- **Data Sharing**: Selectively share financial data and goals with other users

## Tech Stack

- Backend: Flask, SQLAlchemy
- Frontend: Bootstrap, jQuery, DataTables
- Database: SQLite
- Additional Libraries: Pandas (for CSV processing)

## Project Structure

```
app/
├── authentication/     # User authentication
├── budgeting_and_goals/   # Budget and goals management
├── dashboard/         # Analytics and visualization
├── share/            # Data sharing functionality
├── static/           # Static assets (CSS, JS)
├── templates/        # HTML templates
└── transactions/     # Transaction management
```

## Setup Instructions

1. Clone the repository
2. Install required packages:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python app.py
   ```
4. Access the application at `http://localhost:5000`

## Testing

Run the test suite using:
```
python -m pytest
```

## Team Members

| Name | GitHub Username | UWA ID |
|------|----------------|---------|
| Owen | [blobbymcgee] | [23924722] |
| Sepehr | [sepehrmoghani] | [23642415] |
| William | [23722943] | [23722943] |
| Matthew | [sangyancs] | [24313338] |

## Module Responsibilities

- Owen: Authentication
- Sepehr: Transactions
- William: Budgeting and Goals
- Matthew: Dashboard and Analytics

## Core Technologies

- HTML
- CSS
- Bootstrap
- jQuery
- Flask
- AJAX/Websockets
- SQLite with SQLAlchemy

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Submit a pull request
4. Code review and merge

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## AI References

### Matthew - 24313338
https://chatgpt.com/share/68256805-52f0-8012-a0ec-b868d747394a

### Sepehr - 23642415
https://chatgpt.com/share/6826e05a-d97c-8000-9b71-8679082a639e  
https://chatgpt.com/share/6826e07a-4d68-8000-8bdd-844aa798dcb1  
https://chatgpt.com/share/6826e097-eb08-8000-be02-0941ee22eeeb  
https://chatgpt.com/share/6826e0c7-595c-8000-be7d-37143feb773b  
https://chatgpt.com/share/6826e126-376c-8000-9643-6276073d499f  
https://chatgpt.com/share/6826e14a-fa94-8000-bf5a-b3e38c994d60  
https://chatgpt.com/share/6826e167-e070-8000-9ab4-eb23634bbce9  

https://replit.com/@sepehrmoghani/agilewebdevproject?v=1  
https://replit.com/@sepehrmoghani/agilewebdevproject-1?v=1  
https://replit.com/@sepehrmoghani/agilewebdevproject-1?v=1  
https://replit.com/@sepehrmoghani/FinanceTracker?v=1

### William - 23722943

https://enzostvs-deepsite.hf.space/  
https://chatgpt.com/share/6826eb2a-3144-8003-bf53-c7147663ee33

### Owen - 23924722
https://chatgpt.com/share/6826e30a-e338-8010-bdf3-d2750405dd03


