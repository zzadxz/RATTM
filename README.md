# **RATTM X Cash App: Eco Score Calculator**

## **Authors**
- **Authors**: Jennifer Chiou, Ben Henderson, Yoyo Liu, Kiarash Soutoudeh, Gabriel Thompson, Chong Wan
---

## **Table of Contents**
1. [About the Project](#about-the-project)
4. [Features](#features)
5. [Installation](#installation)
6. [Usage](#usage)
9. [License](#license)
10. [Feedback](#feedback)
11. [Contributions](#contributions)

---

## **About the Project**
Our **Eco-Score Calculator** empowers users to make sustainable choices by quantifying the environmental impact of their daily spending. Our technology 

### **Why We Built This**
With climate change worsening year after year, young people are becoming increasingly concerned about the environment. Despite this, most people are entirely unaware of the climate impacts that their daily purchases have. Even if they want to learn more about sustainability, there is a lack of accessible tools that track the emissions tied to daily spending. This leaves people uninformed and unable to make eco-conscious choices.

RATTM bridges this gap by providing easily accessible and actionable metrics that quantify the environmental impact of their daily spending. By analyzing simulated user transaction data, we’ve developed an algorithm to calculate eco-scores using transaction amounts and ESG ratings of the companies they buy from. The user can compare changes in their ecoscore over time, and make small adjustments in their purchasing habits as they see fit.

### **What This Project Does**
- Analyzes transaction data to calculate an **Environmental Friendliness Score**.
- Displays eco-scores over time on an interactive dashboard.
- Visualizes transactions on a map to provide location-based insights.

---

## **Features**
- **Eco-Score Calculation**:
  - Measures the environmental impact of user spending using transaction amounts and ESG ratings.
  - Provides a simple score between 0 and 560, helping users track their sustainability progress.

- **Dashboard**:
  - Displays the user’s current EcoScore and number of green transactions, along with a graph of historical data of those metrics.
  - Contains pie chart of ESG tiers of company the user purchased from.
  - Contains table of the user’s most-purchased-from companies, and their respective ESG scores and amounts purchased from.

- **Transactions**:
  - Shows all of their transactions from their account in a table.
  - For each transaction, displays the company being purchased from, whether the transaction was approved, the ESG score of the company, and the amount and date of transaction.
  - Allows user to filter by whether the transaction was approved, the company name, and date of transaction.

- **Map**:
  - Displays markers on a map of the world, each representing the location of a purchase.
  - All markers are clickable. Upon clicking them, a popup appears showing the name and ESG rating of the company.

---

## **Installation**
Follow these steps to set up and run the project locally.

### **Prerequisites**
Ensure you have the following installed:

- **[Python](https://www.python.org/downloads/)** (Version 3.12 or above)
- **[Next.js](https://nextjs.org/docs/app/getting-started/installation)** with **npm** (Version 14 or above)
- **[Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)**
- **Environment Variables** in `.env` format (details below)

### **Steps**

#### Setting Up the Project
1. **Clone the Repository**:
 ```bash
   git clone https://github.com/zzadxz/RATTM.git
   cd RATTM
```

2. **Set Up a Virtual Environment**

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # MacOS/Linux
.venv\Scripts\activate     # Windows
```

3. **Install Requirements**
```bash
pip install -r requirements.txt
```

4. **Install Frontend Requirements**
```bash
cd frontend
npm install
```

#### Set Up `.env` File

Within the `backend/` directory, create a `.env` file with the following contents.
```
SECRET_KEY=[Heroku Secret Key]
FIREBASE_PRIVATE_KEY=[Firebase Private Key]
FIREBASE_PRIVATE_KEY_ID=[Firebase Private Key ID]
FIREBASE_CLIENT_EMAIL=[Firebase Client Email]
FIREBASE_CLIENT_ID=[Firebase Client ID]
FIREBASE_CERT_URL=[Firebase Cert URL]
```

#### Set Up `.env.local` File
Within the `frontend/` directory, create a file called `.env.local` with the following contents.
```
NEXT_PUBLIC_FIREBASE_API_KEY=[Firebase API Key]
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=[Firebase Auth Domain]
NEXT_PUBLIC_FIREBASE_PROJECT_ID=[Firebase Project ID]
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=[Firebase Storage Bucket]
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=[Firebase Messaging Sender ID]
NEXT_PUBLIC_FIREBASE_APP_ID=[Firebase App ID]
NEXT_PUBLIC_FIREBASE_MEASUREMENT_ID=[Firebase Measurement ID]
NEXT_PUBLIC_API_BASE_URL=rattm-f300025e7172.herokuapp.com/
NEXT_PUBLIC_MAPBOX_KEY=[Mapbox Key]
```

## Usage

### Run Frontend Locally
```bash
npm run dev
```
Open http://localhost:3000/ to view the locally hosted frontend.

### Run Backend Locally
Open a new terminal.
```bash
cd backend
heroku local:run python manage.py runserver
```
Open 127.0.0.1:8000/[endpoint_name] to view the locally hosted backend.

Available backend endpoints:
- /transaction
  - /get
  - /upload
- /map
  - /get_map_data
- /dashboard
  - /get_line_graph_data
  - /get_this_month_green_transactions
  - /get_total_green_transactions
  - /get_top_5_companies
  - /get_total_co2_score
  - /get_this_month_co2_score
  - /get_company_tiers
  - /get_co2_score_change
  - /get_green_transaction_change
- /esg
  - /get
- /login
  - /get_email (POST only)

Usage guide (instructions on how to use the software)

Examples or tutorials (videos, screenshots, or code snippets) are used to clarify how to use the software once it is downloaded

### Navigating the Website

From the root of the website, you can sign up/sign in by clicking the respective links on the navbar. Once signed in, you’ll be redirected to the dashboard. From here, you can click on any of the other navbar links (“About”, “Eco-Score Dashboard”, “Transactions”, “Map”) to view the respective pages. You can find a more detailed description of each of the pages under the “Features” section of this README.

## **License**

This project is licensed under the MIT License. You are free to use, modify, and distribute this project under the terms of the license. For full details, see the [LICENSE](LICENSE) file in the repository.

---

## **Feedback**

We welcome feedback to help improve this project. Here’s how you can provide feedback:

**GitHub Issues**:  
   - Navigate to the repository's [Issues section](https://github.com/zzadxz/RATTM/issues).  
   - Open a new issue describing the feedback or bug.
   - Include relevant details, such as steps to reproduce the issue or suggestions for improvement.

### Guidelines for Feedback:
- **What counts as valid feedback**:  
  - Suggestions for improving features or usability.
  - Bug reports with clear steps to reproduce the issue.
  - Requests for new features or functionality.

- **What to expect**:  
  - We aim to respond to all feedback within 5 business days.
  - Accepted suggestions may be added to our roadmap or addressed in upcoming updates.

---

## **Contributions**

At this time, we are not accepting contributions to this project. 

### Guidelines:
- If you encounter an issue or have feedback, please refer to the [Feedback](#feedback) section for instructions on how to share your thoughts.
- Contributions, including pull requests, will not be reviewed or merged at this time.

Thank you for your understanding!
