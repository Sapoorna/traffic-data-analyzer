# Traffic Data Analysis and Visualization

## Project Description

This project is a Python-based application designed to process and analyze traffic data from CSV files. It performs a series of tasks including data validation, statistical analysis, and data visualization. The application can handle multiple daily traffic data files and saves the processed results into a text file.

## Key Features

* Input Validation: The program validates user input for the date to ensure it is in the correct format and within the specified range.
* Data Processing: It processes CSV files to calculate key traffic metrics, such as the total number of vehicles, trucks, electric vehicles, and two-wheeled vehicles. It also identifies peak traffic hours and the percentage of vehicles exceeding the speed limit.
* Outcomes & Reporting: The analyzed data is displayed in a formatted manner and also saved to a text file named `results.txt` for record-keeping.
* Data Visualization: The application generates a histogram using the `tkinter` library to visually represent vehicle frequency per hour for two main junctions: Elm Avenue/Rabbit Road and Hanley Highway/Westway.

## How to Run the Application

1.  Ensure you have Python installed with the `tkinter` library.
2.  Place the required `traffic_data*.csv` files and the `w2120239.py` script in the same directory.
3.  Open a terminal or command prompt and navigate to the project directory.
4.  Run the script using the command: `python w2120239.py`
5.  Follow the on-screen prompts to enter the date of the traffic data you wish to analyze.

## Included Files

* `w2120239.py`: The main Python script containing the logic for data processing, validation, and visualization.
* `traffic_data*.csv`: Raw traffic data files used as input for the analysis.
* `results.txt`: The output file where the processed results are stored.
* `w2120239.pdf`: The official coursework report.
