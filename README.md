
# Trading Data Dashboard

This project is a trading data application designed to fetch, store, and visualize market data. The application includes functionalities to fetch symbols and market data from external APIs, store them in a database, and visualize them through a command-line interface.

## Features

- **Fetch and Store Data**: Fetch trading symbols and market data from APIs and store them in a SQLite database.
- **View Stored Data**: View stored symbols and market data in a tabulated format.
- **Subscribe to Market Data**: Continuously fetch and display real-time market data for a specified symbol.
- **Automated Testing**: Unit and integration tests to ensure the reliability of the application.

## Requirements

- Python 3.7+
- Required Python packages are listed in the `requirements.txt` file.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/pedrosfaria2/crypto-currency-market-data.git
    cd trading_data_dashboard
    ```

2. Create and activate a virtual environment:

    ### On Windows

    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

    ### On macOS and Linux

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Apply the database migrations:

    ```bash
    alembic upgrade head
    ```

2. Run the application:

    ```bash
    python main.py
    ```

3. Follow the on-screen menu to interact with the application.

## Running Tests

1. To run the tests, use:

    ```bash
    pytest
    ```

    This will execute all the tests located in the `tests` directory.

## Project Structure

- `main.py`: Main file to run the application.
- `app/database.py`: Database setup and session management.
- `app/fetch_data.py`: Functions to fetch symbols and market data from APIs.
- `app/models.py`: SQLAlchemy models for the database tables.
- `app/workers.py`: Functions to handle displaying and storing data.
- `requirements.txt`: Lists all the required Python packages.
- `tests/`: Directory containing unit and integration tests for the application.

## Overview

This project demonstrates how to build a trading data dashboard using Python. It includes functionalities for:

- **Fetching Data**: Using `requests` to fetch data from APIs.
- **Storing Data**: Using `SQLAlchemy` to store data in a SQLite database.
- **Data Visualization**: Using the command-line interface to display data.
- **Automated Testing**: Using `pytest` for unit and integration tests.

## License

This project is licensed under the MIT License.
