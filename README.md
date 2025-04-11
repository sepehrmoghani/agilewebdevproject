Owen: Authentication

Sepehr: Transactions

William: Budgeting and Goals

Matthew: Dashboard and Analytics

# agilewebdevproject
CITS3403 Agile Web Development Group Project


## The list of core allowable technologies and libraries are the following:

    HTML
    CSS
    One of Bootstrap/Tailwind/SemanticUI/Foundation (no others allowed).
    JQuery
    Flask
    AJAX/Websockets
    SQLite interfaced to via the SQLAlchemy package

You may not use any other core technologies, this includes frameworks (e.g. React/Angular), database systems (e.g. MySQL), or advanced CSS frameworks (e.g. directly using SASS yourself). However, you may freely use any JavaScript or Python libraries that implement non-core functionality that is particular to your application, e.g. libraries that provide bindings for ChatGPT or displaying graphs is fine! Font and icon libraries are also fine.
The creation of the web application should be done in a private GitHub repository that includes a README containing:

    a description of the purpose of the application, explaining its design and use.
    a table with with each row containing the i) UWA ID ii) name and iii) Github user name of the group members.
    instructions for how to launch the application.
    instructions for how to run the tests for the application.

## A few notes
  1. First clone the repository on your machine,
  2. Ensure to install venv on your machine, within the project enviornment
  3. Install the requirements.txt after you activate your venv.
  4. We should each have a branch and make changes to that.
  5. Start the project then after every change, commit changes to your branch
  6. At the end, we will discuss merging branches with the main branch.

If anyone else has any suggestions, please feel free to add.

## App Features
Please enter all the app features here:

Must Have:
  - Welcome page
  - Sign in / Login page
  - able to upload CSV files (when logged in)
    - Validate the data first
    - Visualise the data given
  - able to set goals
  - able to selectively share data or goals

Should have:

  **Settings**
  - Settings for "Welcome page":
    - Dark mode
    - Change language
  - Settings for "Logged-in users":
    - Dark mode
    - Change language
    - Log out
    - Text size / font
    - Change colour palette + color-blind option
    - Clear all data (CSV)

  **Data Representation**
  - Format e.g.:
    - Pie chart
    - Line chart
    - Bar graph
    - Summary table
  - Filter / grouping data:
    - Automatically tag / group data
    - Option to hide selected data groups
    - Filter by date range
  - Recommendation goals:
    - A preset goal from the data given
    - Show the recommended / average goals set by the users with the same income range
    - A page for different budget strategies recommended by other users
  - Shows a trend / pattern to predict future spending / savings
  - Support for multiple CSV files at once (connect multiple files)
  - Option to selectively remove specific files
