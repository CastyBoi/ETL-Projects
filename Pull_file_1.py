import paramiko
import datetime
from datetime import datetime
import os

# Replace with your actual values
device_ip = "10.10.101.18"
username = "eric-crafco"
password = "Crafco2022"
remote_file_path = "/home/eric-crafco/Documents/Data_Logging_Files/Break_Beam_Status.txt"
local_directory = r"C:\Users\ecastilla\OneDrive - Crafco Inc\Documents\1 - Programming Directory 2\ETL Project 1\Data Files (Input)\RaspPi Files"

def pull_and_delete_file():
    try:
        transport = paramiko.Transport((device_ip, 22))
        transport.connect(username=username, password=password)

        sftp = paramiko.SFTPClient.from_transport(transport)

        # Get the current date in YYYY-MM-DD format
        current_date = datetime.now().strftime("%Y-%m-%d")
        # Get the current time in a specific format (you can customize the format)
        current_time = datetime.now().strftime("%H%M")
        
        # Append the date to the original filename
        local_filename = f"Break_Beam_Status_({current_date})({current_time}).txt"
        local_path = os.path.join(local_directory, local_filename)

        # Download the file
        sftp.get(remote_file_path, local_path)

        # Additional logic to process the pulled data if needed

        # Delete the file on the Raspberry Pi
        sftp.remove(remote_file_path)

        sftp.close()
        transport.close()

        print("Data log file pulled and deleted successfully.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    pull_and_delete_file()
