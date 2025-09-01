#Author: sapoorna janani
#Date: 2024/12/9
#Student ID: w2120239/20231542

import csv
import tkinter as tk
from datetime import datetime

#Task A: Input Validation
def validate_dates():
    """
    Prompts the user for a date in DD MM YYYY format, validates the input for:
    - Correct data type
    - Correct range for day, month, and year
    """
    while True:
        
        try:
            #Prompt user to enter the day and validate the range
            day = int(input("Please enter the day of the survey in the format DD: "))
            if day < 1 or day > 31:
                print("Out of range - values must be in the range 1 to 31.")
                continue

            ##Prompt user to enter the month and validate the range
            month = int(input("Please enter the month of the survey in the format MM: "))
            if month < 1 or month > 12:
                print("Out of range -values must be in range 1 to 12.")
                continue

            #Prompt user to enter the year and validate the range
            year = int(input("Please enter the year of the survey in the format YYYY: "))
            if year < 2000 or year > 2024:
                print("Out of range-values must be in range 2000 to 2024.")
                continue

            #Checking the number of days for the given month,according to leap year
            if month in [1,3,5,7,8,10,12]:
                month_days = 31
                
            elif month in [4,6,9,11]:
                month_days = 30
                
            elif month == 2:
                if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                    month_days = 29
                else:
                    month_days = 28

            #validate the day dosen't exceed the maximum days for that month 
            if day > month_days:
                print(f"Invalid day: In {year} , month {month} has only {month_days} days")
                continue
                

           #Return the formatted date 
            return (f"{day:02d}{month:02d}{year}")

        #Handling non-integer inputs
        except ValueError:
            print("Integer required.")

    
def validate_continue_input():
     """
    Prompts the user to decide whether to load another dataset:
    - Validates "Y" or "N" input
    """
     
     while True: 
        #Get the you input for continuing the analyze
        choice = input("Do you want to select another data file for a different date? (Y/N): ")
        if choice in ["Y" , "y" , "N" , "n"]:
            return choice
        print("Please enter 'Y' or 'N'.")


# Task B: Processed Outcomes
def process_csv_data(file_path):
    """
    Processes the CSV data for the selected date and extracts:
    - Total vehicles
    - Total trucks
    - Total electric vehicles
    - Two-wheeled vehicles, and other requested metrics .....
    """
    try:
        with open(file_path,'r') as file:
            reader = csv.reader(file)
            headers =  next(reader)  #skipping the header row

            #Initialize totals and counts
            total_vehicles = 0
            total_trucks = 0
            total_electric_vehicles = 0
            total_two_wheeled_vehicles = 0
            total_busses_heading_north = 0
            total_vehicles_not_turning = 0
            total_bicycles = 0
            total_vehicles_over_speed = 0
            total_elm_avenue_vehicles = 0
            total_hanley_highway_vehicles = 0
            elm_avenue_scooters = 0
            hours_of_rain = 0

            #Additional lists and dictionary for further trackings
            hourly_data = {}
            peak_hours = []
            rainy_hours = []
            bicycle_hours = []


            #Checking the if data have in the file
            data_found = False
        
            #Processing each row in the csv file
            for row in reader:
                if row:     #skip any empty rows
                    data_found = True #Mark that data exists

                junction_name = row[0]
                date = row[1]
                time_of_day = row[2]
                hour = time_of_day.split(":")[0] #Extract the hour from time 
                travel_direction_in = row[3]
                travel_direction_out = row[4]
                weather_condition = row[5]
                junction_speed_limit = int(row[6])
                vehicle_speed = int(row[7])
                vehicle_type = row[8]
                electric_hybrid = row[9]

                #Updating total vehicle count
                total_vehicles += 1

                #Counting specific vehicle totals and conditions
                if vehicle_type == 'Truck':
                    total_trucks += 1
                if electric_hybrid.strip().lower() == 'true':
                    total_electric_vehicles += 1
                if vehicle_type in ['Bicycle','Motorcycle','Scooter']:
                    total_two_wheeled_vehicles += 1
                if junction_name == 'Elm Avenue/Rabbit Road' and travel_direction_out == 'N' and vehicle_type.strip() == 'Buss':
                    total_busses_heading_north += 1
                if travel_direction_in == travel_direction_out:
                    total_vehicles_not_turning += 1
                if vehicle_speed > junction_speed_limit:
                    total_vehicles_over_speed += 1
                if vehicle_type == 'Scooter' and junction_name == 'Elm Avenue/Rabbit Road':
                    elm_avenue_scooters += 1
                if junction_name == 'Elm Avenue/Rabbit Road':
                    total_elm_avenue_vehicles += 1
                if junction_name == 'Hanley Highway/Westway':
                    total_hanley_highway_vehicles += 1
                if vehicle_type == 'Bicycle':
                    total_bicycles += 1

                #Tracking bicyle hours
                if vehicle_type == 'Bicycle' and hour not in bicycle_hours:
                    bicycle_hours.append(hour)
                    
                #Tracking rainy hours
                if weather_condition in ['Light Rain','Heavy Rain']:
                    if hour not in rainy_hours:
                        rainy_hours.append(hour)
                   
                #Tracking hourly data for Hanley Highway
                if junction_name == 'Hanley Highway/Westway':
                    #Checking if the current hour is not in the houry_data dictionary and initialize it with a 1
                    if hour not in hourly_data:
                        hourly_data[hour] = 1

                    #If the current hour is aleady in the dictionary increment it by 1
                    else:      
                        hourly_data[hour] += 1

        #If no data found display the message
        if not data_found:
            print("No vehicles recorded for this date")
            return []

        #Calculations
        hours_of_rain = len(rainy_hours) 
        
        trucks_percentage = round((total_trucks/total_vehicles) * 100) if total_vehicles > 0 else 0
        
        average_bicycles_per_hour = round(total_bicycles/len(bicycle_hours)) if len(bicycle_hours) > 0  else 0
 
        scooter_percentage_elm_avenue = round((elm_avenue_scooters/total_elm_avenue_vehicles) * 100) if total_elm_avenue_vehicles > 0 else 0

        peak_hour_vehicles_total_hanley = max([hourly_data[hour] for hour in hourly_data], default = 0)
        
        #Initialize an empty string to srore peak hours as a formatted string
        peak_hours_str = ""

        #Initialize an empty list to store peak traffic hours in Hanley Highway 
        peak_traffic_hours_hanley = []

        #Identify the hours with peak traffic in Hanley Highway  
        for hour in hourly_data:
            #Checking the vehicle count for the current hour matches the peak hour vehicle total in hanley
            if hourly_data[hour] == peak_hour_vehicles_total_hanley:
                peak_hour1 = hour   #Store the current housr as the start hour
                peak_hour2 = str(int(hour)+1)   #Calculating the end hour
                peak_traffic_hours_hanley.append(f"{peak_hour1}:00 and {peak_hour2}:00")  #Formatting the peak hour period

        #Constructing a string of peak traffic hours 
        for i in range(len(peak_traffic_hours_hanley)):
            if i > 0:
                peak_hours_str+=" , "    # , for seperate for multiple entries
            peak_hours_str+=peak_traffic_hours_hanley[i]
                     
                       
       #Results
        results = [
            f"*********************************",
            f"data file selected is {file_path.split('/').pop()}",
            f"*********************************",
            f"The total number of vehicles recorded for this date is {total_vehicles}",
            f"The total number of trucks recorded for this date is {total_trucks}",
            f"The total number of electric vehicles for this date is {total_electric_vehicles}",
            f"The total number of two-wheeled vehicles for this date is {total_two_wheeled_vehicles}",
            f"The total number of Busses leaving Elm Avenue/Rabbit Road heading north is {total_busses_heading_north}",
            f"The total number of vehicles through both junctions not turning left or right is {total_vehicles_not_turning}",
            f"The percentage of total vehicles recorded that are trucks for this date is {trucks_percentage}%",
            "",
            f"The average number of Bikes per hour for this date is {average_bicycles_per_hour}",
            f"The total number of vehicles recorded as over the speed limit for this date is {total_vehicles_over_speed}",
            f"The total number of vehicles recorded through Elm avenue/Rabbit Road junction is date is {total_elm_avenue_vehicles}",
            f"The total number of vehicles recorded through Hanley Highway/Westway junction is {total_hanley_highway_vehicles}",
            f"{scooter_percentage_elm_avenue}% of the vehicles recorded through Elm Avenue/Rabbit Road are scooters.",
            "",
            f"The number of vehicles recorded in the peak hour on Hanley Highway/Westway is {peak_hour_vehicles_total_hanley}",
            f"The most vehicles through Hanley/Westway were recorded between {peak_hours_str}",
            f"The number of hours of rain for this date is {hours_of_rain}" ]
            
        return results
    
    except FileNotFoundError:
       print(f"Error '{file_path}' not found")
       return []
    

def display_outcomes(outcomes):
    """
    Displays the calculated outcomes in a clear and formatted way.
    """
    
    for outcome in outcomes:
        print(outcome)
    
        
# Task C: Save Results to Text File
def save_results_to_file(outcomes,file_name="results.txt"):
    """
    Saves the processed outcomes to a text file and appends if the program loops.
    """

    with open(file_name,'a') as file:
        for outcome in outcomes:
            file.write(outcome+'\n')
        file.write('\n')     #Adding a blank line after each set of results

# if you have been contracted to do this assignment please do not remove this line

def process_histogram_data(file_path):
    #Initialize histogram data for two locations with hourly counts set to 0
    histogram_data = {
        "Elm Avenue/Rabbit Road" : {f"{i:02d}": 0 for i in range(24)},
        "Hanley Highway/Westway" : {f"{i:02d}": 0 for i in range(24)}
        }
    try:
        with open(file_path, "r") as file:
            reader = csv.reader(file)
            next(reader)    #skip the header
            for row in reader:
                if row:     #skip empty rows
                    #Get the junction name and removing extra spaces
                    junction = row[0].strip() 
                    #Get the time field from the row
                    time = row[2]
                    #Extract hour from time in HH format
                    hour = f"{int(time.split(':')[0]):02d}"  

                    #Incrementing the count for the corresponding junction and hour
                    if junction in histogram_data:
                        histogram_data[junction][hour] += 1
        return histogram_data

    except Exception:  #Handling errors during file processing
        print(f"Error processing histogram data")
        return None

#Task D: Histogram Display
class HistogramApp:
    def __init__(self,traffic_data,date):
        """
        Initializes the histogram application with the traffic data and selected date.
        """
        self.traffic_data = traffic_data  #Store processed traffic data
        self.date = date                  #Store the selected date for histogram
        self.root = tk.Tk()               #Create tkinter root window
        self.canvas = None                #Canvas for drawing

    def setup_window(self):
        """
        Sets up the Tkinter Window and canvas for the histogram.
        """
        #Set the window title
        self.root.title("Histogram ")  
    
        #creating a canvas for drawing histogram (light gray background)
        self.canvas = tk.Canvas(self.root, width = 1000, height = 600, bg = "#D3D3D3")
        #Add padding around the canvas
        self.canvas.pack()  
        
        
    def draw_histogram(self):
        """
        Draws the histogram with axes, labels, and bars.
        """
        width = 1000    #Width of the canvas
        height = 600    #Height of the canvas
        margin = 60     #Margin around the canvas
        bar_width = 15  #Width of each bar in histogram

        #Defining colours for two locations
        colors = {
            "Elm Avenue/Rabbit Road": "#008000",  #Green
            "Hanley Highway/Westway": "#FF0000"   #Red
            }

        #Adding a title to the canvas
        self.canvas.create_text(margin, 30,text = f"Histogram of Vehicle Frequency per Hour ({self.date})",font = ("Arial", 12, "bold"),anchor = "w")
        
        #Define x and y coordinates of start and end points
        start_x = margin
        stary_y = height - margin
        end_x = width - margin
        end_y = height - margin

        #Draw x axis
        self.canvas.create_line(start_x,stary_y,end_x,end_y, width = 2)
    
        #Add lables for each hour on the x-axis
        for i in range(24):
            x = margin + (i * (width - 2 * margin) / 23)
            self.canvas.create_text(x,height - margin + 20,text = f"{i:02d}")

        #Add a title for x axis
        self.canvas.create_text(width // 2,height - 10,text = "Hours 00:00 to 24:00",font = ("arial",10))

        #Finding the maximumun value of data  for scalling
        max_value = max(max(int(value) for value in values.values()) for values in self.traffic_data.values())
        #Adding 5 to max_value to ensure bars don't touch the top margin
        scale_factor = (height - 2 * margin) / (max_value + 5)

        #Draw bars for each location
        locations = list(self.traffic_data.keys()) #Get the list of locations
        for hour in range(24):
            #Format hour as HH
            hour_str = f"{hour:02d}"    
            #Calculate x coordinate
            x = margin + (hour * (width - 2 * margin) / 23)   
            
            for i in range(len(locations)):  #Use index based loop
                location = locations[i]      #Get location using index
                value = int(self.traffic_data[location][hour_str])  #Get the count for hour
                bar_height = value * scale_factor  #Calculate height of the bar

                #Bar coordinates
                x1 = x + (i - 0.5) * bar_width  #Left x coordinate of the bar
                x2 = x + (i + 0.5) * bar_width  #Right x coordinate of the bar
                y1 = height - margin - bar_height  #Top y coordinate of the bar
                y2 = height - margin     #Bottom y coordinate of the bar

                #Draw the  bar
                self.canvas.create_rectangle(x1, y1, x2, y2,fill = colors[location],outline = "black")

                #Adding lable above the bar showing its value
                if value > 0:
                    #Set the text color based on location
                    if location == "Hanley Highway/Westway":
                        text_color = "Red"
                    elif location == "Elm Avenue/Rabbit Road":
                        text_color = "Green"

                    #Draw the value above bar
                    self.canvas.create_text((x1 + x2) / 2, y1 - 10,text = str(value),font = ("Arial", 8),fill = text_color)



    def add_legend(self):
        """
        Adds a legend to the histogram to indicate which bar corresponds to which junction.
        """
        legend_x = 60    #Starting x coordinate for the legend
        legend_y = 70    #Starting y coordinate for the legend
        colors = {
            "Elm Avenue/Rabbit Road": "#008000", #Green
            "Hanley Highway/Westway": "#FF0000"  #Red
            }

        for location,color in colors.items():
            #Draw a colored rectangle for each location
            self.canvas.create_rectangle(legend_x, legend_y,legend_x + 20, legend_y + 10,fill = color, outline = "black")

            #Add the location name next to the rectangle
            self.canvas.create_text(legend_x + 25 + 20, legend_y + 5,text = location, anchor = "w")
            #Move to the next line for next location
            legend_y += 20  

    def run(self):
        """
        Runs the Tkinter main loop to display the histogram.
        """
        self.setup_window()    #Set up the tkinter window
        self.draw_histogram()  #Draw the histogram
        self.add_legend()      #Add the legend
        self.root.mainloop()   #Start the tkinter loop


#task E: code Loops to Handle multiple CSV files
class MultiCSVProcessor:
    def __init__(self):
        """
        Initializes the application for processing multiple CSV files.
        """
        self.current_data = None  #Place holder for currently loaded data


    def load_csv_file(self,file_path):
        """
        Loads a CSV file and processes its data.
        """
        try:
            self.current_data = process_csv_data(file_path)   #Process the csv file
            return True
        except Exception as e:
            print(f"Error processing file: {e}")
            return False

    def clear_previous_data(self):
        """
        Clears data from the previous run to process a new dataser.
        """
        self.current_data = None

    def handle_user_interaction(self):
        """
        Handle user input for processing multiple files.
        """
        #Get the valid date input from user
        date_input = validate_dates()  
        file_name = f"traffic_data{date_input}.csv"  #Generate the file name based on the date

        if self.load_csv_file(file_name):
            #Display and save results
            display_outcomes(self.current_data)   #Show the processed data
            save_results_to_file(self.current_data)  #Save the processed data to a file

            #Display histogram
            histogram_data = process_histogram_data(file_name)  #Get the histogram data
            if histogram_data:
                #Format the date for display
                formatted_date = f"{date_input[:2]}/{date_input[2:4]}/{date_input[4:]}"
                #Create a histogramApp and run 
                app = HistogramApp(histogram_data, formatted_date)
                app.run()

        return validate_continue_input()  #Check if user want to process another file

    def process_files(self):
        """
        Main loop for handling multiple CSv files until the user decides to quit.
        """
        while True:
            self.clear_previous_data()   #Clear the data from the previous file
            choice = self.handle_user_interaction() #Process the current file and interact with the user

            if choice.upper() == "N":  #Exit if the user choose N
                print("Exiting program.")
                break
            print("Loading another dataset.")  #prompt to load another dataset

#Main function to start the program
def main():
    processor = MultiCSVProcessor()  #Create a multiCSVProcessor instance
    processor.process_files()   #Start processing files

#Start the progra
if __name__ == "__main__":
    main()
