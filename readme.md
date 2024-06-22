# Expense Track Project

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Configuration](#configuration)
6. [Contributing](#contributing)
7. [License](#license)

## Introduction
The Expense Tracker is a Django-based web application that helps you manage your finances by tracking your daily expenses. It allows you to categorize your expenses, visualize your expenses & analyze spending patterns.

## Features
- Add, edit, and delete expenses
- Categorize expenses
- Visualize expenses
- Analyze spending patterns with charts
- Filter expenses based on start and end date

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/ankitpakhale/ExpenseTrack.git
   ```
2. Navigate to the project directory:
   ```bash
   cd ExpenseTrack
   ```
3. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```
4. Activate the virtual environment:
   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     . .venv/bin/activate
     ```
5. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
6. Apply the migrations:
   ```bash
   python manage.py migrate
   ```
7. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
8. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Usage
1. Open your browser and go to `http://localhost:8000`
2. Log in with the superuser credentials.
3. Start adding and managing your expenses.

## Configuration
- You can configure categories and other settings in the `settings.py` file.

## Contributing
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
