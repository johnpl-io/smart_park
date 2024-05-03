import React, { useState, useEffect } from 'react';

const CarsDisplay = () => {
    const [cars, setCars] = useState([]);
    const [currentIndex, setCurrentIndex] = useState(0);

    // Fetching the cars from the API on component mount
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

    // Handler functions for previous and next buttons
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
                    <button className="navigate-button left" onClick={handlePrev}>←</button>
                    <img src={cars[currentIndex].image_path} alt={cars[currentIndex].name} className="car-image" />
                    <button className="navigate-button right" onClick={handleNext}>→</button>
                    <div className="car-info">
                        <h2>{cars[currentIndex].name}</h2>
                        <p>Model: {cars[currentIndex].model}</p>
                        <p>Location: {cars[currentIndex].location || 'Not Currently Parked'}</p>
                        <button className="select-button" onClick={handleSelectCar}>Select This Car</button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default CarsDisplay;
