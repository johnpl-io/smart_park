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
