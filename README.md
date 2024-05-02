#Instructions on Running Project

-  From the terminal run docker compose up in the smart_park directory
-  cd into the backend\src directory and run the populate.py file
-  Then in the backend\src directory run the endpoints.py file
-  Go to the frontend directory run npm install and then npm start
-  Finally go to the ProxyServer folder and run node gmap.js

#Port References

-  The flask service layer runs on port 5000
-  Frontend runs on port 3000
-  Proxy server runs on port 2000 (it checks to see if the user is on a street when they click the park button)
-  Database is in port 5432, username is user, password is password, and database is called smart_park_db
