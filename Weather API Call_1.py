# API calls to OpenWeatherMap
# Creating this to pull weather data from an opensource weather API call

# PIP installs
import time
import requests
import json

# API URL Variables
lat = "33.3528" # N
long = "-111.7890" # W
api_key = 'dbcbd9d8e0f8d74d0f455ad03377d5cb'

# API Endpoint URL
api_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={long}&appid={api_key}&units=imperial"


# Define various variables for the HTTP request function
maxRetries = 3  # Maximum number of retry attempts
retryCount = 0

def requestData():
    global retryCount

    try:
        # Send a GET request to the API
        response = requests.get(api_url)
        
        # Check for rate limiting (429 response)
        if response.status_code == 429:
            # Implement rate limit handling, e.g., wait and retry
            time.sleep(10)
            if retryCount < maxRetries:
                retryCount += 1
                return requestData()
            else:
                print('Max retries reached. Exiting.')
                return None

        # Check for a successful response
        if response.status_code == 200:
            json_data = response.json()
            # Process the response data here (assuming it's JSON)
            # print('\nResponse Data:', json_data, '\n')  
            temp_data = json_data['main'] 
            current_temp = temp_data['temp']
            print(f'Temperature Data: {current_temp}')
            return current_temp
        else:
            print('Non-200 status code:', response.status_code)
            return None

    except requests.exceptions.RequestException as error:
        # Handle specific request exceptions
        print('A request error occurred:', str(error))
        return None

# Call the function to request data
current_temp = requestData()

# Add a delay
time.sleep(1)

