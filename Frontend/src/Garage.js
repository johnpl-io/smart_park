import React, { useState, useEffect } from 'react';
import backgroundImage from './Garage.jpg';
import './Garage.css';
import { FaInfoCircle, FaCar, FaSignOutAlt, FaSearch, FaCog, FaCheckCircle} from 'react-icons/fa';

const CarsDisplay = () => {
    const [cars, setCars] = useState([]);
    const [currentIndex, setCurrentIndex] = useState(0);
    const [sidebarOpen, setSidebarOpen] = useState(true);
    const [carId, setCarID] = useState(localStorage.getItem('car_id'));

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
        setCarID(cars[currentIndex].car_id);
    };


    const toggleSidebar = () => {
        setSidebarOpen(!sidebarOpen);
    };

    return (
        <div className="garage-container">
            <div className={`sidebar ${sidebarOpen ? 'open' : ''}`}>
                    <div className="menu">
                    <ul className="menu-list">
                        <li><button onClick={() => { window.location.href = "/AboutUs"; }}><FaInfoCircle /> About Us</button></li>
                        <li><button onClick={() => { window.location.href = "/UserProfile"; }}><FaCog /> Account Settings</button></li> {/* Changed icon to FaCog */}
                        <li><button onClick={() => { window.location.href = "/Garage"; }}><FaCar /> Garage</button></li>
                        <li><button onClick={() => { window.location.href = "/BrowseCars"; }}><FaSearch /> Browse Cars</button></li> {/* Changed icon to FaSearch */}
                        <li><button onClick={() => { window.location.href = "/Logout"; }}><FaSignOutAlt /> Logout</button></li>
                    </ul>
                    </div>
            </div>
            <button className={`toggle-button ${sidebarOpen ? 'open' : ''}`} onClick={toggleSidebar}>
                <span></span>
            </button>
    {cars.length > 0 && (
        <div className="car-display">
        <div className="image-container">
            {cars[currentIndex].car_id == carId && (
                <div className="selected-indicator">
                    <FaCheckCircle />
                </div>
            )}
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
