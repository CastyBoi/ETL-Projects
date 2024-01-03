from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time
import os
from datetime import datetime

# Set the user agent to mimic a real browser
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" 
# User Agent from network section of website inspect

# Set up Chrome options for headless mode
chrome_options = Options()
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument("--disable-background-timer-throttling")
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')
chrome_options.add_argument('--headless')  # Enable headless mode

# Path to the Chrome WebDriver executable
driver_path = r"ETL Project 1\Programs (Webscrapers)\ChromeDriver\chromedriver-win64\chromedriver.exe"
# Set this as a relative path, makes it more easily transferable (assuming similar directory structure)

# Initialize Chrome in headless mode
chrome_service = Service(driver_path)
browser = webdriver.Chrome(service=chrome_service, options=chrome_options)

# Initial URL
initial_url = "https://www.cars.com/shopping/results/?dealer_id=&keyword=&list_price_max=&list_price_min=&makes[]=&maximum_distance=100&mileage_max=&monthly_payment=&page_size=100&sort=best_deal&stock_type=used&transmission_slugs[]=manual&year_max=&year_min=&zip=85296"
    # Manual Cars, all years, all makes, 100 results per page, 100 miles from 85296
# Some learnings for the links that get put in
    # Apply high level filters from cars first
    # Manual or Auto
    # New or Used # This one specifically was causing some issues, think it had to do with the way the site was layed out with ads or some shit, haven't figured this one out yet.
    # Makes etc
    
# Setup transmission variables 
transmission_1 = 'Manual'
transmission_2 = 'Automatic'



# Function with a While Loop to go through multiple pages
def webscraper_func(url, browser, transmission, num_pages):
    # Navigate to the website
    browser.get(url)

    # Initialize lists to store scraped data
    Car_Info_list = []
    Car_Mileage_list = []
    Car_Price_list = []
    Car_Link_list = []
    Car_Transmission_list = []
    Car_New_Used_List = []
    
    # Setup the initial page counter at 0
    page_count = 0
    
    # While Loop
    while page_count < num_pages:
        try:
            # Code for extracting data from the page
            # Find the <div> elements with class "vehicle-card"
            time.sleep(10)  # Add a buffer to allow the page to load completely
            
            vehicle_card_divs = WebDriverWait(browser, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.vehicle-card")))

            for div in vehicle_card_divs:
                try:
                    # Wait for the h2.title element to be visible
                    Car_Info_element = WebDriverWait(div, 10).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, "h2.title")))
                    Car_Info = Car_Info_element.text
                    print('Car Info Appended')

                    # Wait for the div.mileage element to be visible
                    Car_Mileage_element = WebDriverWait(div, 10).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.mileage")))
                    Car_Mileage = Car_Mileage_element.text
                    print('Car Mileage Appended')
                    
                    # Wait for the span.primary-price element to be visible
                    Car_Price_element = WebDriverWait(div, 10).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, "span.primary-price")))
                    Car_Price = Car_Price_element.text
                    print('Car Price Appended')
                    
                    # Wait for the href element to be visible
                    Car_Link_element = WebDriverWait(div, 10).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, "a.vehicle-card-link.js-gallery-click-link")))
                    Car_Link = Car_Link_element.get_attribute('href')
                    print('Car Link Appended')

                    Car_Transmission_element = transmission
                    Car_Transmission = Car_Transmission_element
                    print('Transmission Appended')
                    
                    Car_New_Used_element = 'Used'
                    Car_New_Used = Car_New_Used_element
                    print('Car New/Used Appened')
                    
                    Car_Info_list.append(Car_Info)
                    Car_Mileage_list.append(Car_Mileage)
                    Car_Price_list.append(Car_Price)
                    Car_Link_list.append(Car_Link)  # Append the Car_Link to your list
                    Car_Transmission_list.append(Car_Transmission) 
                    Car_New_Used_List.append(Car_New_Used) 


                except (NoSuchElementException):
                    # Handle exceptions for individual elements here
                    print("Element not found")
                    print(f"Page Counter: {page_count}")
                    continue
                except (TimeoutException):
                    print('Timeout error')
                    print(f"Page Counter: {page_count}")
                    continue

            # Check if the "Next" button is available
            next_button = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.ID, 'next_paginate')))

            if next_button and next_button.get_attribute('href'):
                # Click the "Next" button to move to the next page
                next_button.click()

                # Wait for the next page to load (you may need to adjust the timeout)
                WebDriverWait(browser, 10).until(EC.url_changes(initial_url))

                # Increment the page count
                page_count += 1
            else:
                break  # Exit the loop if there's no "Next" button or it's disabled

        except StaleElementReferenceException:
            # Handle stale element exception by re-locating the element
            vehicle_card_divs = browser.find_element(By.CSS_SELECTOR, "div.vehicle-card")
            # Use the element again

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            print(f"Page Counter: {page_count}")
    # Continue with the rest of your code
    # Clean up and quit the browser
    browser.quit()

    # Create a DataFrame from the scraped data
    data_1 = {
        'Car Info': Car_Info_list,
        'Car Mileage': Car_Mileage_list,
        'Car Price': Car_Price_list,
        'Car Link': Car_Link_list,
        'Car Transmission': Car_Transmission_list,
        'Car New/Used': Car_New_Used_List
    }
    df_1 = pd.DataFrame(data_1)
    return df_1


# Execute function
original_df = webscraper_func(initial_url,browser,transmission_1,1)

# Print the DataFrame
print(f'Original Dataframe: \n {original_df}')

def clean_dataframe(input_df):
    
    # Split the 'Car Info' column into multiple columns by whitespace
    split_columns = input_df['Car Info'].str.split(expand=True)
    
    # Ensure that each entry has at least 9 columns (adjust based on your needs)
    while split_columns.shape[1] < 9:
        split_columns[split_columns.shape[1]] = pd.NA
    
    # Rename the split_columns column names    
    split_columns.columns = ['Year', 'Make', 'Model', 'Sub_Model', 'Trim_1', 'Trim_2', 'Info_1', 'Info_2', 'Info_3']

    # Combin back with original dataframe
    output_df = pd.concat([input_df, split_columns], axis=1)
    
    # Drop initial Car_Info Column
    output_df.drop(columns=['Car Info'], inplace=True)
    
    return output_df
# Run function and assign to variable
clean_df = clean_dataframe(original_df)

# Print the refined dataframe
print(f'Cleaned Dataframe: {clean_df}')


## Output the dataframe to a csv file
# Get the current time in a specific format (you can customize the format)
current_time = datetime.now().strftime("%H%M")
# File Name
output_file_name = f'Webscraper Data ({current_time}).csv'

# File path
output_directory = r"C:\Users\eric-c\ETL Project 1\Data Files (Input)\WebScraper Files"
output_file_path = os.path.join(output_directory, output_file_name)

# Output command
clean_df.to_csv(output_file_path,index=False)

time.sleep(10)

### Creating an executable file (for task scheduling or whatever tf we want)
# cd into the directory that the program is in, and we want the executable to be in
# pyinstaller --onefile WebScraper_Executable_1.0.py 
# change pyinstaller name to whatever the filename is