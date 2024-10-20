# RATTM
RATTM FTL project

rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if false;
    }
  }
}

## backend
**File Structure**\
backend/\
&nbsp;&nbsp;RattmWeb/ : project folder\
&nbsp;&nbsp;&nbsp;&nbsp;asgi.py : asgi config (idk what this is)\
&nbsp;&nbsp;&nbsp;&nbsp;firebase.py : loads firebase db\
&nbsp;&nbsp;&nbsp;&nbsp;rattm-cred-firebase.json : firebase credentials file\
&nbsp;&nbsp;&nbsp;&nbsp;settings.py : django settings\
&nbsp;&nbsp;&nbsp;&nbsp;urls.py : project endpoints\
&nbsp;&nbsp;&nbsp;&nbsp;views.py : return interfaces for endpoints\
&nbsp;&nbsp;&nbsp;&nbsp;wsgi.py : wsgi config (idk what this is)\
&nbsp;&nbsp;transaction/ : transaction app folder (i have no idea what's going on here)\
&nbsp;&nbsp;&nbsp;&nbsp;view.py : functions to upload and fetch data from firestore\
&nbsp;&nbsp;&nbsp;&nbsp;urls.py : transaction-specific endpoints that call the functions in view.py\
&nbsp;&nbsp;&nbsp;&nbsp;many other files that i do not understand\
&nbsp;&nbsp;manage.py : file that runs everything\
&nbsp;&nbsp;routers.py : file i made following a tutorial (idk if we need it)\

**Running Code**
Go to `backend` folder\
Run `python3 manage.py runserver` \

This will run on `localhost:8000`\

## database
`localhost:8000/api/upload` will upload data to firebase\
`localhost:8000/api/get` will show data in firebase\
`https://console.cloud.google.com/firestore/databases/-default-/data/panel/transactions/1LpRig3D7NipgPG67P3O?project=rattm-tli` This is the link to the firestore project\

## frontend
**File Structure**\
src/app\
&nbsp;&nbsp;modules/ : contains subpages (ex: transaction section within main page - we prob won't have that but just for now it's there)\
&nbsp;&nbsp;&nbsp;&nbsp;transactions/ : formats transaction data\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;index.tsx\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;index.styles.tsx\
&nbsp;&nbsp;pages/ : contains pages of the site\
&nbsp;&nbsp;&nbsp;&nbsp;main-site/ : format main page of site (imports transactions)\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;index.tsx\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;index.styles.tsx\
&nbsp;&nbsp;components/ : (not created yet) i think this can contain mobile vs desktop views for pages\
&nbsp;&nbsp;fonts/ : idk what this does, i guess it has fonts\
&nbsp;&nbsp;favicon.icon : our browser icon\
&nbsp;&nbsp;globals.css : css styling for all pages\
&nbsp;&nbsp;layout.tsx : layout for all pages (like if we have same header/footer for everything)\
&nbsp;&nbsp;page.module.css : idk what this is for\
&nbsp;&nbsp;page.tsx : main page at localhost:3000 (imports main-site)\

**Running Code**\
Write `npm run dev` while in the frontend folder\

Access using `localhost:3000`
* The main page calls `localhost:8000/api/get` to display the transaction in the database on the frontend
* Currently displays nothing cuz there's no database


