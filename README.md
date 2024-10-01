# RATTM
RATTM FTL project

## backend
**File Structure**\
django-api/\
    RattmWeb/ : project folder\
        asgi.py : asgi config (idk what this is)\
        firebase.py : loads firebase db\
        rattm-cred-firebase.json : firebase credentials file\
        settings.py : django settings\
        urls.py : project endpoints\
        views.py : return interfaces for endpoints\
        wsgi.py : wsgi config (idk what this is)\
    transaction/ : transaction app folder (i have no idea what's going on here)\
        view.py : functions to upload and fetch data from firestore\
        urls.py : transaction-specific endpoints that call the functions in view.py\
        many other files that i do not understand\
    manage.py : file that runs everything\
    routers.py : file i made following a tutorial (idk if we need it)\

**Running Code**
Go to `backend/django-api` folder\
Run `python3 manage.py runserver` \

This will run on `localhost:8000`\

## database
theoretically `localhost:8000/api/upload` will upload a row to firebase, but we need to create the database + enable firestore first\
and `localhost:8000/api/get` will load data from firebase\

## frontend
**File Structure**
src/app\
    modules/ : contains subpages (ex: transaction section within main page - we prob won't have that but just for now it's there)\
        transactions/ : formats transaction data\
            index.tsx\
            index.styles.tsx\
    pages/ : contains pages of the site\
        main-site/ : format main page of site (imports transactions)\
            index.tsx\
            index.styles.tsx\
    components/ : (not created yet) i think this can contain mobile vs desktop views for pages\
    fonts/ : idk what this does, i guess it has fonts\
    favicon.icon : our browser icon\
    globals.css : css styling for all pages\
    layout.tsx : layout for all pages (like if we have same header/footer for everything)\
    page.module.css : idk what this is for\
    page.tsx : main page at localhost:3000 (imports main-site)\

**Running Code**
Write `npm run dev` while in the frontend folder\

Access using `localhost:3000`
* The main page calls `localhost:8000/api/get` to display the transaction in the database on the frontend
* Currently displays nothing cuz there's no database


