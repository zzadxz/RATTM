
# RATTM

**RATTM** Rage Against the Turing Machine X Cash App

## CI/CD, Backend, & Frontend Services
Backend (PaaS) on [Heroku](https://github.com/jnnchi/rattm-backend) \
Frontend on [Vercel](https://vercel.com/)

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

- Create a `backend/django-api/Rattm/rattm-cred-firebase.json` file. This will store your Firebase credentials. Paste into the file the JSON in [this Discord message](https://discord.com/channels/1281256285618307082/1283811324018556938/1291457826463678505). This file should not be committed to the repository.

- Create a `.env` file (in the root directory). The file should be of this format:

    ```bash
    FIREBASE_CREDENTIAL_PATH="[root project path]/backend/django-api/RattmWeb/rattm-cred-firebase.json"
    MOCK_JSON_PATH="[root project path]/backend/django-api/resources/mockdata.json"
    ```

... where `[root project path]` is the absolute path to the root. You can find this by entering `pwd` into the terminal from the root directory.

Alternatively, you could navigate to `rattm-cred-firebase.json` and `mockdata.json` in the VS code file tree, right click on them, and click "Copy Path" to get the absolute paths to these files.

### 5. Install Next.js Dependencies

Navigate to the `frontend` directory and install the necessary packages:

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

This will run the backend on `http://localhost:8000` (unless there's a port conflict, in which case the console will tell you otherwise)

### 7. Run the Frontend (Next.js)

Open a new terminal window or tab, navigate to the frontend directory, and start the Next.js server:

```bash
cd frontend
npm run dev
```

The frontend will be served on `http://localhost:3000` (unless the console says otherwise).

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
