
# RATTM

**RATTM** Rage Against the Turing Machine X Cash App

Click for: [Frontend Project and Detailed Readme](https://github.com/zzadxz/RATTM)

## Prerequisites

Before running the project, ensure you have the following:
- **Python** (Version 3.12 or above)
- Firebase credentials in the form of a `.json` file (details below)
- An `.env` file with environment variables (details below)

## Steps to Run the Project

### 1. Clone the Repository

```bash
git clone https://github.com/jnnchi/rattm-backend.git
```

The folder you should be now in will later be referred to as "the root"

### 2. Set Up a Virtual Environment

Create and activate a Python virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On MacOS/Linux
# For Windows use: .venv\Scripts\activate
```

### 3. Install Python Dependencies

Staying in the root, with the virtual environment activated, install the required Python dependencies:

```bash
pip install -r requirements.txt
```

### 4. Add Firebase Credentials and Environment Variables

- Create a `backend/rattm-cred-firebase.json` file. This will store your Firebase credentials. Paste into the file the JSON in [this Discord message](https://discord.com/channels/1281256285618307082/1283811324018556938/1291457826463678505). This file should not be committed to the repository.

- Create a `.env` file (in the root directory). The file should be of this format:

    ```bash
    MOCK_JSON_PATH="[root project path]/resources/mockdata.json"
    SECRET_KEY="heroku secret key"
    FIREBASE_PRIVATE_KEY="firebase private key, with \n replaced with \\n"
    FIREBASE_PRIVATE_KEY_ID="firebase private key id"
    FIREBASE_CLIENT_EMAIL="firebase client email"
    FIREBASE_CLIENT_ID="firebace client id"
    FIREBASE_CERT_URL="https://www.googleapis.com/ url"
    ```

... where `[root project path]` is the absolute path to the root. You can find this by entering `pwd` into the terminal from the root directory.


### Backend (Django API)

```plaintext
[root]/
├── RattmWeb/                # Project folder
│   ├── asgi.py              # ASGI config (for async support)
│   ├── firebase.py          # Loads Firebase DB
│   ├── settings.py          # Django settings
│   ├── urls.py              # Project endpoints
│   ├── views.py             # Return interfaces for endpoints
│   ├── wsgi.py              # WSGI config (for web server)
├── transaction/             # Transaction app folder
│   ├── view.py              # Functions to upload and fetch data from Firestore
│   ├── urls.py              # Transaction-specific endpoints
├── manage.py                # File that runs everything
├── Procfile                 # File that specifies how heroku will run the project
├── app.json                 # Config file for Heroku CICD pipeline
```

## Database Endpoints & Heroku Hosting

- `https://rattm-f300025e7172.herokuapp.com/api/get/` — Fetches and shows data from Firestore
- `https://rattm-f300025e7172.herokuapp.com/api/upload/` — Uploads data to Firestore (not yet implemented on hosting)

You can view the Firestore project by going to:
[Firestore Console](https://console.cloud.google.com/firestore/databases/-default-/data/panel/transactions/1LpRig3D7NipgPG67P3O?project=rattm-tli)

You can view the Heroku project by going to: 
[Heroku Project](https://dashboard.heroku.com/apps/rattm)

You can view the Heroku CICD Pipeline by going to: 
[Heroku Production Pipeline](https://dashboard.heroku.com/pipelines/2bae1f11-094f-445a-83ed-b9a4d0511b7d)

### Heroku CLI Commands
Install: 

(On Ubuntu/WSL)
- `sudo apt-get install libpq-dev python-dev`
- `heroku`
- `python -m pip install django-heroku`
- Use 'heroku --version' to check if heroku is installed. Follow the command line to install heroku if needed. 

(On Mac) 
- `brew tap heroku/brew && brew install heroku`
- `pip install django-heroku`

Type `heroku` to see the help page. 

To check running apps: `heroku apps`

If we want to store data in environment variables: 
- "heroku config" command can be used to manage the environment variables
- for example, `heroku config:get ENV_VARIABLE_NAME`

Useful commands:
- Run Locally: `heroku local:run python manage.py runserver`
- Run Tests Locally: `heroku local:run python manage.py test`

Heroku debug: 
- if heroku local doesn't run -> check if .env file is updated with heroku secrete key 
- note: our .env file is in the RATTM repo, not the backend directory