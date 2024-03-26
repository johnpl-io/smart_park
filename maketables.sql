CREATE TABLE users (
    user_id SERIAL NOT NULL,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash BINARY(64) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    created_on TIMESTAMP NOT NULL,
    car_id int, 
    PRIMARY KEY (user_id)
);

CREATE TABLE taken_spots (
spot_id SERIAL NOT NULL UNIQUE, 
lon DECIMAL(9, 6) NOT NULL, 
lat  DECIMAL(9, 6) NOT NULL, 
time_arrived TIMESTAMP NOT NULL, 
-- time_left TIMESTAMP NULL, 


);


CREATE TABLE spot_history (

spot_id SERIAL NOT NULL UNIQUE, 
lon DECIMAL(9, 6) NOT NULL, 
lat  DECIMAL(9, 6) NOT NULL, 
time_arrived TIMESTAMP NOT NULL, 
time_left TIMESTAMP NOT NULL,
car_id INT NOT NULL,
);




CREATE TABLE user_park (
user_id INT NOT NULL,
spot_id INT NOT NULL,
FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE;
FOREIGN KEY (spot_id) REFERENCES cars(car_id) ON DELETE CASCADE, 
PRIMARY KEY(user_id, car_id)
);

    
CREATE TABLE cars (
car_id SERIAL NOT NULL UNIQUE,
height INT NOT NULL,
len INT NOT NULL,
PRIMARY KEY (car_id)

);



CREATE TABLE user_car (
    user_id INT NOT NULL,
    car_id INT NOT NULL,

    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE;
    FOREIGN KEY (car_id) REFERENCES cars(car_id) ON DELETE CASCADE, 
    PRIMARY KEY(user_id, car_id)
);
