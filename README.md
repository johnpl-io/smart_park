# Welcome To Smart Park!

For our final project, we have developed Smart Park, an app designed to simplify the often frustrating task of finding nearby available parking spots. Urban parking can be a nightmare, but with our app, users can skip the stress of endlessly circling for a spot. Instead, Smart Park recommends parking locations based on proximity and availability.
What sets Smart Park apart from other parking apps is its adaptive learning feature. When initially deployed, the app doesn't rely on preexisting map data. Instead, it learns from user behavior, noting where users successfully parked as potential spots it can recommend to other users in the future. As a result of this, our app is adaptable to virtually any location worldwide and can be used to find free parking. Our tech stack uses PostgreSQL with PostGIS for database, Python and flask for our ORM and API, and react.js for our frontend. 



https://github.com/johnpl-io/smart_park/assets/63315701/461741bc-b849-41be-bc92-1611f09f5380


#  Instructions on Running Project

-  From the terminal run docker compose up in the smart_park directory
-  cd into the Backend/src install proper requirements and run the populate.py
- 
-  Then in the Backend/src directory run the app.py file
- Download images of cars from https://drive.google.com/drive/folders/1semOhx2VbV_6dMk1OklQsQdu-raN2LHL?usp=sharing
and put the images folder as Frontend/public/images
- Install nyc_streets from https://postgis.net/workshops/postgis-intro/about_data into a new database called under smart_park_db/nyc.
This can be done using QGIS.
-  Go to the Frontend directory run npm install and then npm start
- Make sure GMAP_API_KEY='API_KEY' in your environement variables.
-  Finally go to the ProxyServer folder and run node gmap.js 

#  Port References

-  The flask service layer runs on port 5000
-  Frontend runs on port 3000
-  Proxy server runs on port 2000 (it checks to see if the user is on a street when they click the park button)
-  Database is in port 5432, username is user, password is password, and database is called smart_park_db
