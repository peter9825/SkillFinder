import sqlite3
import requests
from requests.auth import HTTPBasicAuth
import tkinter as tk
from tkinter import ttk


def call_api():
    # Fetch data from the API and return the list of entries
    url = 'https://joeyp96.wufoo.com/api/v3/forms/employee-complaint-form/entries.json'
    with open('secret.txt', 'r') as file:
        api_key = file.read().strip()
    response = requests.get(url, auth=HTTPBasicAuth(api_key, 'pass'))
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("API Connection Successful")
        data = response.json()
        return data.get('Entries', [])  # Return the list of entries
    elif response.status_code == 404:
        print("Error 404")
    else:
        print(f"Error: Received status code {response.status_code}")
    return []


def create_database():
    # Connecting to the database
    conn = sqlite3.connect("candidates.db")
    cursor = conn.cursor()
    # Creating table with Wufoo fields
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            date_of_birth TEXT,
            phone_number TEXT,
            desired_field_of_work TEXT,
            years_of_experience INTEGER,
            website TEXT,
            college_graduate TEXT
        )
    ''')
    conn.commit()
    cursor.execute("DELETE FROM candidates")  # Clears the table for fresh data
    return conn


def fetch_data(experience_filter, college_filter):
    # Fetch data from the database and filter based on experience and college graduate status
    conn = sqlite3.connect("candidates.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM candidates")
    data = cursor.fetchall()
    formatted_data = []
    for row in data:
        # Grabs data from sqlite database and formats it into a tuple to be stored into a list
        id = int(row[0])
        name = row[1]
        email = row[2]
        birth = row[3]
        phone_number = row[4]
        field_of_work = row[5]
        experience = int(row[6])
        website = row[7]
        college = row[8]
        if college_filter == 'Both':
            # To allow the college graduate filter to work without restricting results
            if experience >= experience_filter:
                candidate = (id, name, email, birth, phone_number, field_of_work, experience, website, college)
                formatted_data.append(candidate)
        else:
            if experience >= experience_filter and college == college_filter:
                # Filters candidates based on experience and college graduate status
                candidate = (id, name, email, birth, phone_number, field_of_work, experience, website, college)
                formatted_data.append(candidate)
    conn.close()
    return formatted_data


def filter_candidates():
    # Reads filter inputs, retrieves data, and updates the UI with the results
    try:
        min_experience = int(experience_entry.get())
    except ValueError:
        min_experience = 0
    college_filter = college_var.get()

    candidates = fetch_data(min_experience, college_filter)
    display_text.delete('1.0', tk.END)  # Clear the display

    # Add headers with fixed width for each column
    headers = f"{'Name':<30}{'Email':<40}{'DOB':<15}{'Phone':<15}{'Field':<25}{'Exp':<10}{'Website':<50}{'College':<10}\n"
    display_text.insert(tk.END, headers)
    display_text.insert(tk.END, "-" * 195 + "\n")

    # Add candidate rows with fixed width formatting
    for candidate in candidates:
        row = f"{candidate[1]:<30}{candidate[2]:<40}{candidate[3]:<15}{candidate[4]:<15}{candidate[5]:<25}{candidate[6]:<10}{candidate[7]:<50}{candidate[8]:<10}\n"
        display_text.insert(tk.END, row)



def build_gui():
    # Creates the layout of the GUI, which creates text boxes to display user data and input our filters
    root = tk.Tk()
    root.title("Skill Finder")
    root.geometry("1280x720")

    # Dark theme styles
    root.configure(bg="#1e1e1e")
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TLabel", background="#1e1e1e", foreground="#ffffff")
    style.configure("TButton",
                    background="#2e2e2e", foreground="#ffffff",  # Normal state
                    borderwidth=1, relief="flat")
    style.map("TButton",
              background=[("active", "#3e3e3e")],  # Hover state
              foreground=[("active", "#ffffff")])
    style.configure("TEntry", fieldbackground="#3e3e3e", foreground="#ffffff")
    style.configure("TOptionMenu", background="#2e2e2e", foreground="#ffffff")
    style.configure("TFrame", background="#1e1e1e")

    # Filter inputs
    filter_frame = ttk.Frame(root, style="TFrame")
    filter_frame.pack(pady=10, padx=10, fill=tk.X)

    ttk.Label(filter_frame, text="Minimum Years of Experience: ").pack(side=tk.LEFT, padx=5)
    global experience_entry
    experience_entry = ttk.Entry(filter_frame, width=5)
    experience_entry.pack(side=tk.LEFT, padx=5)

    ttk.Label(filter_frame, text="College Graduate: ").pack(side=tk.LEFT, padx=5)
    global college_var
    college_var = tk.StringVar(value="Both")
    college_dropdown = ttk.OptionMenu(filter_frame, college_var, "Both", "Yes", "No")
    college_dropdown.pack(side=tk.LEFT, padx=5)

    filter_button = ttk.Button(filter_frame, text="Apply Filter", command=filter_candidates)
    filter_button.pack(side=tk.LEFT, padx=10)

    # Display area for candidate data
    global display_text
    display_text = tk.Text(root, wrap=tk.NONE, font=("Courier", 10), height=30, bg="#1e1e1e", fg="#ffffff")
    display_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Scrollbars
    x_scroll = ttk.Scrollbar(root, orient=tk.HORIZONTAL, command=display_text.xview)
    x_scroll.pack(side=tk.BOTTOM, fill=tk.X)
    display_text.config(xscrollcommand=x_scroll.set)

    root.mainloop()




def filter_and_insert_data(entries, conn):
    # Inserts filtered API data into the database
    cursor = conn.cursor()
    for entry in entries:
        # Mapping the fields from the form
        candidate_data = (
            entry.get('Field1'),  # Candidate name
            entry.get('Field24'),  # Email
            entry.get('Field7'),  # Date of birth
            entry.get('Field5'),  # Phone
            entry.get('Field2'),  # Desired field of work
            int(entry.get('Field23', 0)),  # Years of experience
            entry.get('Field31'),  # Website
            entry.get('Field3')  # College graduate (y/n)
        )
        # Inserting filtered data into the database
        cursor.execute('''
            INSERT INTO candidates (
                name, email, date_of_birth, phone_number,
                desired_field_of_work, years_of_experience,
                website, college_graduate
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', candidate_data)
    conn.commit()


if __name__ == '__main__':
    # Fetch data from API
    entries = call_api()
    if entries:
        # Create the database and table by calling function
        conn = create_database()

        # Filter and insert data by calling function
        filter_and_insert_data(entries, conn)

        conn.close()

        # Print statement to verify if db was created successfully
        print("Data successfully inserted into the database.")
    else:
        print("No data to insert.")

    # Launch the GUI
    build_gui()
