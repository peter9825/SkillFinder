# SkillFinder

Python application that retrieves candidate data from a remote API, stores it in an SQLite database and provides an interactive GUI 
for filtering and displaying candidate information. It is designed to help users quickly identify candidates based on specific criteria 
such as minimum years of experience and college graduate status.


# Features
- API Data Retrieval:
  retrieves candidate entries from a specified API endpoint.

- Local Database Storage:
  Stores candidate data in an SQLite database, clearing previous data on each run to ensure fresh updates.

- Filtering Functionality:
  Allows users to filter candidate records by minimum years of experience and college graduate status.

- User-Friendly GUI:
  Interactive interface with options to apply filters and view
  detailed candidate information in a scrollable text area.

- Automated Testing:
  Includes pytest tests to verify API connectivity and data integrity.
  

# Requirements
- Python 3.x 
- Tkinter 
- SQLite 
- IDE (PyCharm)
- Pytest (pip install pytest)
- Requests (pip install requests)
- Personal Wufoo API Key


# Running the Application
- Clone the Repository
- Install the required Python packages using pip: pip install requests pytest
- Configure the API Key: Create a file named secret.txt in the project directory and add your API key.
  This key is used for authenticating the API call.
- run main.py

  
