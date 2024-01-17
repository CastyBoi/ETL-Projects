# This program is meant to function as a simple and clean user interface that 

import tkinter as tk
from tkinter import filedialog
from Report_Append_Import_1 import report_card_export, report_append
import os

## Declare variables globally
original_file_path = "" # Original File Path (Existing Dataset or whatever)
append_file_1_path = "" # Appending File 1
append_file_2_path = "" # Appending File 2 (If applicable)
output_folder_path = "" # Folder to Output New Combined File

# Append File Number Variables
number_append_file_text = 1
number_of_append_file_entry = None # Number of files being appended to pass to the imported function
button_accept_append_file_num = None # Button to accept the number of files being appended

output_file_name_text = None # Name to assign to output File
output_file_name_entry = "" # Idk the entry of the text box or something
button_accept_file_name = None # Button to accept the file name initial value

# Function for getting input of OG file path
def original_file_path_input():
    global original_file_path
    original_file_path = filedialog.askopenfilename(title="Select Original Report File")
    
    if original_file_path:
        print(f"Original Report Path is: {original_file_path}")
        label1.config(text=f"File path selected: {original_file_path}")
    
    return original_file_path

# Function to get Append File 1 file path
def append_file_1_path_input():
    global append_file_1_path
    append_file_1_path = filedialog.askopenfilename(title="Select Appending File 1")
    
    if append_file_1_path:
        print(f"Append File 1 Path is: {append_file_1_path}")
        label2.config(text=f"File path selected: {append_file_1_path}")
    
    return append_file_1_path

# Function to get the Append File 2 file path
def append_file_2_path_input():
    global append_file_2_path
    append_file_2_path = filedialog.askopenfilename(title="Select Appending File 2")
    
    if append_file_2_path:
        print(f"Append File 2 Path is: {append_file_2_path}")
        label3.config(text=f"File path selected: {append_file_2_path}")
    
    return append_file_2_path

# Function to get the Output Folder path
def output_folder_input():
    global output_folder_path
    output_folder_path = filedialog.askdirectory(title="Select Output Folder")
    
    if output_folder_path:
        print(f"Output folder selected: {output_folder_path}")
        label4.config(text=f"Output folder selected: {output_folder_path}")
    return output_folder_path

# Function to assign the Output File name
def output_file_name_input():
    global output_file_name_text
    global button_accept_file_name

    # Text widget for user input
    output_file_name_text = tk.Text(app, height=1, width=30)
    output_file_name_text.grid(row=6, column=1, padx=10, pady=10, sticky="ew")

    # Create a button to accept the file name
    button_accept_file_name = tk.Button(app, text="Accept File Name", command=accept_file_name)
    button_accept_file_name.grid(row=6, column=2, padx=10, pady=10, sticky="ew")
    
# Fuction to setup the button to accept the file name, then delete the popup  
def accept_file_name():
    global output_file_name_text
    global output_file_name_entry
    global button_accept_file_name

    # Get the entered file name from the Text widget
    output_file_name_entry = output_file_name_text.get("1.0", tk.END).strip()

    # Destroy the Text widget and Accept button
    output_file_name_text.destroy()
    button_accept_file_name.destroy()

    # Update label to show the entered file name
    label6.config(text=f"Output File Name Entered: {output_file_name_entry}")

# Function to assign the Number of Append Files
def number_append_files():
    global number_append_file_text
    global button_accept_append_num

    # Text widget for user input
    number_append_file_text = tk.Text(app, height=1, width=30)
    number_append_file_text.grid(row=5, column=1, padx=10, pady=10, sticky="ew")

    # Create a button to accept the file name
    button_accept_append_num = tk.Button(app, text="Accept Append Number", command=accept_append_quantity)
    button_accept_append_num.grid(row=5, column=2, padx=10, pady=10, sticky="ew")
  
# Fuction to setup the button to accept the number of append files
def accept_append_quantity():
    global number_append_file_text
    global number_of_append_file_entry
    global button_accept_append_num

    # Get the entered number from the Text widget
    number_of_append_file_entry = number_append_file_text.get("1.0", tk.END).strip()

    # Destroy the Text widget and Accept button
    number_append_file_text.destroy()
    button_accept_append_num.destroy()

    # Update label to show the entered number of append files
    label5.config(text=f"Input Number of Files: {number_of_append_file_entry}")
   
# Calling the function and appending the files depending on the # of files selected  
def report_append_file():

    # Input validation
    if not all([os.path.isfile(original_file_path), os.path.isfile(append_file_1_path), os.path.isdir(output_folder_path)]):
        print("Error: One or more input files or output folder do not exist.")
        return
    elif number_of_append_file_entry not in ('1', '2'):
        print('Invalid number of files. Please only enter 1 or 2')
        return

    # Check if the output file name is empty
    if not output_file_name_entry:
        print("Error: Output file name is empty.")
        return

    # Convert the number_of_append_file_entry to an integer
    number_of_append_files = int(number_of_append_file_entry)

    # Call the imported functions with the provided paths
    if number_of_append_files == 1:
        if not os.path.isfile(append_file_1_path):
            print('No append file 1 selected')
            return
        result_df = report_append(original_file_path, append_file_1_path, None, 1)
    elif number_of_append_files == 2:
        if not os.path.isfile(append_file_1_path) or not os.path.isfile(append_file_2_path):
            print('Not all append files selected')
            return
        result_df = report_append(original_file_path, append_file_1_path, append_file_2_path, 2)

    report_card_export(result_df, output_folder_path, output_file_name_entry)


# Close application
def close_program():
    app.destroy()

# Create the main application window
app = tk.Tk()
app.title("Report Append Program: Select # of Files to append, The Append File(s), and the Original (Master) File")

# Set the size of the main window
app.geometry("1500x500")

# Create buttons with custom sizes
button_og = tk.Button(app, text="Select OG (Master) File", command=original_file_path_input, width=30, height=2)
# Append File 1 Button
button_append_1 = tk.Button(app, text="Select Append 1 File", command=append_file_1_path_input, width=30, height=2)
# Append File 2 Button
button_append_2 = tk.Button(app, text="Select Append 2 File", command=append_file_2_path_input, width=30, height=2)
# Output Folder Button
button_output_folder = tk.Button(app, text="Select Output Folder", command=output_folder_input, width=30, height=2)
# Append File Buttons
button_num = tk.Button(app, text='Enter Number of Files to Append', command=number_append_files, width=30, height=2)
# File Name Buttons
button_text = tk.Button(app, text="Enter Output File Name", command=output_file_name_input, width=30, height=2)
# Run program Button
button_run = tk.Button(app, text="Run Append Program", command=report_append_file, width=50, height=2)
# Close Program Button
button_close = tk.Button(app, text="Close", command=close_program, width=50, height=2)


# Create labels to display file paths and output file name
label1 = tk.Label(app, text="File path selected: ")
label2 = tk.Label(app, text="File path selected: ")
label3 = tk.Label(app, text="File path selected:  ")
label4 = tk.Label(app, text="Output Folder Selected: ")
label5 = tk.Label(app, text="Number of files to append:  ")
label6 = tk.Label(app, text="Output File Name Entered:  ")

# Place buttons and labels using the grid manager
button_og.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
# Append File 1 Button Location
button_append_1.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
# Append File 2 Button Location
button_append_2.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
# Output Folder Button Location
button_output_folder.grid(row=4, column=0, padx=10, pady=10, sticky="ew")
# Number of files Button Location
button_num.grid(row=5, column=0, padx=10, pady=10, sticky="ew")
# File Name Button Location
button_text.grid(row=6, column=0, padx=10, pady=10, sticky="ew")
# Run Button Location
button_run.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky="ew")  
# Close Button Location
button_close.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky="ew")  # Align to the north, south, east, and west

label1.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
label2.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
label3.grid(row=3, column=1, padx=10, pady=10, sticky="ew")
label4.grid(row=4, column=1, padx=10, pady=10, sticky="ew")
label5.grid(row=5, column=1, padx=10, pady=10, sticky="ew")
label6.grid(row=6, column=1, padx=10, pady=10, sticky="ew")

# Run the Tkinter event loop
app.mainloop()
