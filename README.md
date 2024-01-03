# ETL-Project
Space to share and display programs and other information related to an ETL Project I am working on. 

Includes:

  Sample Webscraper Script

  Sample FTP File Pull Script
  
  Sample File to SQL Server Script

  Sample Weather API Call Script


General Overview: I wrote each of these scripts / programs (underwent several iterations and lots of troubleshooting) to get them to the point where I could make them executables, and then have either task-scheduler run them, or have Apache Nifi run them. 

Data Movement Details:

Using Apache Nifi, I was able to reference each of these executables and run them at a set schedule, before setting up Get and Put files for physical file movement from folder to folder, along with creating flow files for internal ETL Movement. 
  
