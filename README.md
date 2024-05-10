# Welcome To Smart Park!

For our final project, we have developed Smart Park, an app designed to simplify the often frustrating task of finding nearby available parking spots. Urban parking can be a nightmare, but with our app, users can skip the stress of endlessly circling for a spot. Instead, Smart Park recommends parking locations based on proximity and availability.
What sets Smart Park apart from other parking apps is its adaptive learning feature. When initially deployed, the app doesn't rely on preexisting map data. Instead, it learns from user behavior, noting where users successfully parked as potential spots it can recommend to other users in the future. As a result of this, our app is adaptable to virtually any location worldwide and can be used to find free parking. Our tech stack uses PostgreSQL with PostGIS for database, Python and flask for our ORM and API, and react.js for our frontend. 


#  Instructions on Running Project

-  From the terminal run docker compose up in the smart_park directory
-  cd into the backend\src directory and run the populate.py file
-  Then in the backend\src directory run the endpoints.py file
-  Go to the frontend directory run npm install and then npm start
-  Finally go to the ProxyServer folder and run node gmap.js

#  Port References

-  The flask service layer runs on port 5000
-  Frontend runs on port 3000
-  Proxy server runs on port 2000 (it checks to see if the user is on a street when they click the park button)
-  Database is in port 5432, username is user, password is password, and database is called smart_park_db
