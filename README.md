
# RATTM

**RATTM** is a project that integrates Firebase Firestore as the database and a Django backend to handle transactions. The frontend is built using Next.js, and communicates with the backend API to fetch and display transaction data.

## Prerequisites

Before running the project, ensure you have the following:
- **Python** (Version 3.12 or above)
- **Next.js** (Version 14 or above)
- **npm** (Installed with Node.js)
- Firebase credentials in the form of a `.json` file (details below)
- An `.env` file with environment variables (details below)

## Steps to Run the Project

### 1. Clone the Repository

```bash
git clone https://github.com/zzadxz/RATTM.git
cd RATTM
```

### 2. Set Up a Virtual Environment

Create and activate a Python virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On MacOS/Linux
# For Windows use: .venv\Scripts\activate
```

### 3. Install Python Dependencies

With the virtual environment activated, install the required Python dependencies:

```bash
pip install -r requirements.txt
```

### 4. Add Firebase Credentials and Environment Variables

- You will need to add a `rattm-cred-firebase.json` file for Firebase credentials. This file should not be committed to the repository. Ensure it is added locally and properly referenced in your `.env` file.

- Example `.env` file:

    ```bash
    FIREBASE_CREDENTIAL_PATH="backend/django-api/RattmWeb/rattm-cred-firebase.json"
    MOCK_JSON_PATH="backend/django-api/resources/mockdata.csv"
    ```

- Your `.env` file should also contain necessary Firebase configurations and other secrets (like API keys). Be sure to reference this `.env` in your Python scripts for loading environment variables.

### 5. Install Next.js Dependencies

Navigate to the frontend directory and install the necessary packages:

```bash
cd frontend
npm install
```

### 6. Run the Backend (Django API)

Go to the `backend/django-api` folder and run the Django development server:

```bash
cd backend/django-api
python manage.py runserver
```

This will run the backend on `http://localhost:8000`.

### 7. Run the Frontend (Next.js)

Open a new terminal window or tab, navigate to the frontend directory, and start the Next.js server:

```bash
cd frontend
npm run dev
```

The frontend will be served on `http://localhost:3000`.

## File Structure

### Backend (Django API)

```plaintext
django-api/
├── RattmWeb/                # Project folder
│   ├── asgi.py              # ASGI config (for async support)
│   ├── firebase.py          # Loads Firebase DB
│   ├── rattm-cred-firebase.json  # Firebase credentials file (not committed)
│   ├── settings.py          # Django settings
│   ├── urls.py              # Project endpoints
│   ├── views.py             # Return interfaces for endpoints
│   ├── wsgi.py              # WSGI config (for web server)
├── transaction/             # Transaction app folder
│   ├── view.py              # Functions to upload and fetch data from Firestore
│   ├── urls.py              # Transaction-specific endpoints
├── manage.py                # File that runs everything
├── routers.py               # Router setup (potentially not needed)
```

### Frontend (Next.js)

```plaintext
frontend/
├── src/
│   ├── app/
│   │   ├── modules/             # Contains subpages (ex: transaction section)
│   │   │   └── transactions/    # Formats transaction data
│   │   │       ├── index.tsx
│   │   │       ├── index.styles.tsx
│   ├── pages/
│   │   └── main-site/           # Main page of the site
│   │       ├── index.tsx
│   │       ├── index.styles.tsx
│   ├── components/              # (Not created yet) Mobile/Desktop views
│   ├── fonts/                   # Fonts
│   ├── favicon.icon             # Browser icon
│   ├── globals.css              # Global styling
│   ├── layout.tsx               # Layout for all pages (header/footer)
│   ├── page.module.css          # Unclear purpose
│   ├── page.tsx                 # Main page at localhost:3000
```

## Database Endpoints

- `localhost:8000/api/upload` — Uploads data to Firestore
- `localhost:8000/api/get` — Fetches and shows data from Firestore

You can view the Firestore project by going to:
[Firestore Console](https://console.cloud.google.com/firestore/databases/-default-/data/panel/transactions/1LpRig3D7NipgPG67P3O?project=rattm-tli)