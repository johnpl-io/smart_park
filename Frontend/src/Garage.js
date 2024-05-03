import React, { useState, useEffect } from 'react';
import backgroundImage from './Garage.jpg';
import './Garage.css';
const CarsDisplay = () => {
    const [cars, setCars] = useState([]);
    const [currentIndex, setCurrentIndex] = useState(0);

    useEffect(() => {
        const fetchCars = async () => {
            const user_id = localStorage.getItem("user_id");
            const response = await fetch(`http://localhost:5000/get-cars?user_id=${user_id}`);
            console.log(response);
            const data = await response.json();
            console.log(data);
            setCars(data["cars"]);
        };

        fetchCars();
    }, []);

    const handlePrev = () => {
        setCurrentIndex((prevIndex) => (prevIndex > 0 ? prevIndex - 1 : 0));
    };

    const handleNext = () => {
        setCurrentIndex((prevIndex) => (prevIndex < cars.length - 1 ? prevIndex + 1 : prevIndex));
    };

    const handleSelectCar = () => {
        localStorage.setItem('car_id', cars[currentIndex].car_id)
    };

    // Display content
    return (
        <div className="garage-container">
    {cars.length > 0 && (
        <div className="car-display">
            <div className="image-container">
                <img src={cars[currentIndex].image_path} alt={cars[currentIndex].name} className="car-image" />
            </div>
            <div className="navigation-buttons">
                <button className="navigate-button left" onClick={handlePrev}>←</button>
                <button className="navigate-button right" onClick={handleNext}>→</button>
            </div>
        </div>
    )}
    {cars.length > 0 && (
        <div className="car-info">
            <div className="car-info-box">
                <h2>{cars[currentIndex].name}</h2>
                <p>Model: {cars[currentIndex].model}</p>
                <p>Location: {cars[currentIndex].location || 'Not Currently Parked'}</p>
            </div>
            <button className="select-button" onClick={handleSelectCar}>Select This Car</button>
        </div>
    )}
</div>

    );
};

export default CarsDisplay;
