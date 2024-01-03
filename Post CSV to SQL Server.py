# Setup imports
import sqlalchemy
from sqlalchemy.engine import URL
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine, text
import pandas as pd
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import random
from sqlalchemy import func, DateTime

### Connection Test Function
def SQL_Connection_Test():
    
    # Set Global Variables
    global Server_Name, Server_Port, Database_Name, Username_1, Password_1, connection_url, engine
    
    # Connection Variable Setup
    Server_Name = '10.10.100.70' # Desktop Server Address
    Server_Port = 1433
    Database_Name = 'Test_Database_1'
    # Driver_Name = '{SQL Server}' # Driver Name
    # Driver_Name_2 = '{ODBC Driver 18 for SQL Server}'

    # Login Info for Crafco_Data_Logging DB 
    Username_1 = 'Python_1' 
    Password_1 = 'Pythoniscool10!'
    # User has Read and Write permission
        
    connection_url = URL.create(
        "mssql+pyodbc",
        username=Username_1,
        password=Password_1,
        host=Server_Name,
        port=Server_Port,
        database=Database_Name,
        query={
            "driver": 'SQL Server',
            "TrustServerCertificate": "yes",
            "authentication": "ActiveDirectoryIntegrated",
        },
    ) 
    # Setup Link:
    # https://docs.sqlalchemy.org/en/20/dialects/mssql.html#module-sqlalchemy.dialects.mssql.pyodbc

    engine = create_engine(connection_url, use_setinputsizes = False) 
    # New verion of SQL Alchemy updated the default value of use_setinputsizes. look up 'invalid precision value sqlalchemy' for more info.

    try:
        engine.connect()
        print("success")
    except SQLAlchemyError as err:
        print("error", err.__cause__)

### Test Connection Output
print('\n')
SQL_Connection_Test()
print('\n')
### Test Connection Output


def sql_append():
    # CSV file path (adjust as needed)
    file_path = r'ETL Project 1\Data Files\RaspPi Files\Break_Beam_Status_2023-12-11.txt'
    
    # Assuming your DataFrame columns are ['Status', 'Location', 'Timestamp']
    # Adjust the names accordingly based on your DataFrame columns
    columns_mapping = {
        'Status': 'Breakbeam_Status',
        'Location': 'Location',
        'Timestamp': 'TimeStamp'
    }
    
    try:
        # Read CSV into a pandas DataFrame
        df = pd.read_csv(file_path)
        
        # Rename the columns before inserting
        df.rename(columns={'Status': 'Breakbeam_Status', 'Timestamp': 'TimeStamp'}, inplace=True)
        
        # Re-order the columns
        df = df[['Breakbeam_Status', 'TimeStamp', 'Location']]
        
        # Convert to datetime 
        df['TimeStamp'] = pd.to_datetime(df['TimeStamp'], errors='coerce')

        # Insert DataFrame into the SQL Server table using the SQLAlchemy engine
        table_name = 'Breakbeam_Data_Table'
        df.to_sql(table_name, engine, schema='dbo', if_exists='append', index=False)
        print('CSV File Appended Successfully')
    except SQLAlchemyError as e:
        print(f'Error appending Data: {e}')

# Call the function
sql_append()