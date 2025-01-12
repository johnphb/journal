# Journal App
Welcome to the Journal App, your personal space for capturing thoughts, ideas, and daily reflections. With the Journal App, you can:

- **Create Entries:** Easily write and save your journal entries, capturing your thoughts and experiences.
- **Edit and Manage:** Update your entries as your thoughts evolve and manage them with ease.
- **Track Progress:** View all your entries in a calendar format, helping you track your journaling habit over time.

Start journaling today and keep your memories organized with the Journal App!

# Deployed Website
-   https://journal-4ggn.onrender.com
    
If you follow the link, keep in mind that it might take some time for the website to load for the first time.

## System Requirements
The below requirements need to be installed on the system to run the project.

-   Python 3 (`3.13.0`)

## Running the project
This project is built using Python, and utilizes the Flask framework. You can use SQLAlchemy while running the project in development mode, but a Postgrasql database is needed for production.

Install all system requirements (see above)

Set up a python virtual environment 
    
    $ python3 -m venv venv
    
Activate the virtual environment

    - macOS/Linux: $ source venv/bin/Activate
    - Windows: $ venv\Scripts\activate.bat
    
Install the python requirements 

    $ python3 -m pip install -r requirements.txt

Dublicate the .env.example file, and name the dublicate file .env
        
    - You need to populate the .env file now
    - SECRET_KEY=' random string '
    - DATABASE_URL=' Your actual database url (for production) '
    - FLASK_APP=run.py
    
Run the project using 

    $ python run.py

When you stop working on the project you need to deactivate the virtual environment

    $ deactivate