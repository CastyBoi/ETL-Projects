import tkinter as tk
from tkinter import filedialog
from Report_Clean_Import_1 import clean_report, export_report
import os

# Declare variables globally
prod_file_path = ""
coois_file_path = ""
output_folder_path = ""
output_file_name_text = None
output_file_name_entry = ""
button_accept_file_name = None

def prod_file_input():
    global prod_file_path
    prod_file_path = filedialog.askopenfilename(title="Select Productivity Report File")
    
    if prod_file_path:
        print(f"Prod Path is: {prod_file_path}")
        label1.config(text=f"File path selected: {prod_file_path}")
    
    return prod_file_path

def coois_file_input():
    global coois_file_path
    coois_file_path = filedialog.askopenfilename(title="Select COOIS Report File")
    
    if coois_file_path:
        print(f"COOIS Path is : {coois_file_path}")
        label2.config(text=f"File path selected: {coois_file_path}")
    
    return coois_file_path

def output_folder_input():
    global output_folder_path
    output_folder_path = filedialog.askdirectory(title="Select Output Folder")
    
    if output_folder_path:
        print(f"Output folder selected: {output_folder_path}")
        label3.config(text=f"Output folder selected: {output_folder_path}")
    return output_folder_path

def output_file_name_input():
    global output_file_name_text
    global button_accept_file_name

    # Text widget for user input
    output_file_name_text = tk.Text(app, height=1, width=30)
    output_file_name_text.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

    # Create a button to accept the file name
    button_accept_file_name = tk.Button(app, text="Accept File Name", command=accept_file_name)
    button_accept_file_name.grid(row=4, column=2, padx=10, pady=10, sticky="ew")

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
    label4.config(text=f"Output File Name Entered: {output_file_name_entry}")

def run_report_clean_function():
    global prod_file_path
    global coois_file_path
    global output_folder_path
    global output_file_name_entry

    prod_path = prod_file_path
    coois_path = coois_file_path
    output_folder = output_folder_path

    # Input validation
    if not all([os.path.isfile(prod_path), os.path.isfile(coois_path), os.path.isdir(output_folder)]):
        print("Error: One or more input files or output folder do not exist.")
        return

    # Check if the output file name is empty
    if not output_file_name_entry:
        print("Error: Output file name is empty.")
        return

    # Call the imported functions with the provided paths
    result_df = clean_report(prod_path, coois_path)
    export_report(result_df, output_folder, output_file_name_entry)

# Close application
def close_program():
    app.destroy()

# Create the main application window
app = tk.Tk()
app.title("Report Clean Program: Select Prod and COOIS Reports")

# Set the size of the main window
app.geometry("1500x500")

# Create buttons with custom sizes
button_prod = tk.Button(app, text="Select Productivity Report File", command=prod_file_input, width=30, height=2)
button_coois = tk.Button(app, text="Select COOIS Report File", command=coois_file_input, width=30, height=2)
button_output_folder = tk.Button(app, text="Select Output Folder", command=output_folder_input, width=30, height=2)
button_text = tk.Button(app, text="Enter Output File Name", command=output_file_name_input, width=30, height=2)
button_run = tk.Button(app, text="Run Report Clean Program", command=run_report_clean_function, width=50, height=2)
button_close = tk.Button(app, text="Close", command=close_program, width=50, height=2)


# Create labels to display file paths and output file name
label1 = tk.Label(app, text="File path selected: ")
label2 = tk.Label(app, text="File path selected: ")
label3 = tk.Label(app, text="Output folder selected: ")
label4 = tk.Label(app, text="Output File Name Entered: ")

# Place buttons and labels using the grid manager
button_prod.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
button_coois.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
button_output_folder.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
button_text.grid(row=4, column=0, padx=10, pady=10, sticky="ew")
button_run.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="ew")  
button_close.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="ew")  # Align to the north, south, east, and west

label1.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
label2.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
label3.grid(row=3, column=1, padx=10, pady=10, sticky="ew")
label4.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

# Run the Tkinter event loop
app.mainloop()
