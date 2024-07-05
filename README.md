# Trading Data Tool

This project is a trading data application designed to fetch, store, and visualize market data. The application includes functionalities to fetch symbols and market data from external APIs, store them in a database, and visualize them through a command-line interface.

## Features

- **Fetch and Store Data**: Fetch trading symbols and market data from APIs and store them in a SQLite database.
- **View Stored Data**: View stored symbols and market data in a tabulated format.
- **Subscribe to Market Data**: Continuously fetch and display real-time market data for a specified symbol.
- **Automated Testing**: Unit and performance tests to ensure the reliability and efficiency of the application.
- **Benchmarking**: Measure the performance of key functions to ensure optimal efficiency.

## Requirements

- Python 3.7+
- Required Python packages are listed in the `requirements.txt` file.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/pedrosfaria2/crypto-currency-market-data.git
    cd crypto-currency-market-data
    ```

2. Create and activate a virtual environment:

    ### On Windows

    ```bash
    python -m venv venv
    venv\\Scripts\\activate
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

## Running Benchmark Tests

1. To run the benchmark tests, use:

    ```bash
    pytest --benchmark-only
    ```

    This will execute the benchmark tests and provide detailed performance metrics.

## Project Structure

- `main.py`: Main file to run the application.
- `app/database.py`: Database setup and session management.
- `app/fetch_data.py`: Functions to fetch symbols and market data from APIs.
- `app/models.py`: SQLAlchemy models for the database tables.
- `app/workers.py`: Functions to handle displaying and storing data.
- `requirements.txt`: Lists all the required Python packages.
- `tests/`: Directory containing unit, performance, and benchmark tests for the application.

## Performance and Benchmarking

### Performance Tests

Performance tests are designed to measure the time taken by critical functions in the application. The tests are located in `tests/test_performance.py`. The functions tested include:

- `fetch_symbols()`
- `store_symbols()`
- `fetch_market_data()`
- `store_market_data()`

The performance tests provide insights into how long each function takes to execute, helping identify potential bottlenecks.

### Benchmarking

Benchmarking is the process of measuring the performance of software applications. In this project, benchmarking is used to evaluate the efficiency of key functions. The benchmark tests are located in `tests/test_benchmark.py` and use the `pytest-benchmark` plugin to provide detailed metrics.

#### Benchmark Results

- **fetch_market_data**:
  - **Mean Time**: 148.4934 ms
  - **Operations Per Second (OPS)**: 6.7343

- **fetch_symbols**:
  - **Mean Time**: 207.4745 ms
  - **Operations Per Second (OPS)**: 4.8199

- **store_market_data**:
  - **Mean Time**: 2.9535 ms
  - **Operations Per Second (OPS)**: 338.5788

- **store_symbols**:
  - **Mean Time**: 72.6016 ms
  - **Operations Per Second (OPS)**: 13.7738

### Explanation

Benchmarking allows us to measure and compare the performance of different parts of the application. By identifying how long each function takes to execute and how many operations can be performed per second, we can optimize the code for better performance. Functions with higher mean times and lower operations per second may require optimization to improve the overall efficiency of the application.

## Overview

This project demonstrates how to build a trading data dashboard using Python. It includes functionalities for:

- **Fetching Data**: Using `requests` to fetch data from APIs.
- **Storing Data**: Using `SQLAlchemy` to store data in a SQLite database.
- **Data Visualization**: Using the command-line interface to display data.
- **Automated Testing**: Using `pytest` for unit, integration, and performance tests.
- **Benchmarking**: Using `pytest-benchmark` to measure the performance of critical functions.

## License

This project is licensed under the MIT License.
