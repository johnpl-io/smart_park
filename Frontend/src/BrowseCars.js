import React, { useState, useEffect, useRef } from 'react';
import './BrowseCars.css';
import $ from 'jquery';
import 'jquery-ui/ui/widgets/autocomplete'; 

const CarBrowser = () => {
    const [query, setQuery] = useState('');
    const [cars, setCars] = useState([]);
    const [suggestions, setSuggestions] = useState([]);
    const searchRef = useRef(null);

    useEffect(() => {
        // Fetch car model names from the backend
        fetch(`http://localhost:5000/get-models`)
            .then(response => response.json())
            .then(data => {
                // Convert data to the format required by jQuery Autocomplete
                const models = data.car_models;
                console.log(models);
                setSuggestions(models);
            })
            .catch(error => console.error('Failed to load car models:', error));
        }, []);
    

    useEffect(() => {
        // Initialize jQuery Autocomplete
        $(searchRef.current).autocomplete({
            source: suggestions,
            select: function(event, ui) {
                setQuery(ui.item.value);
            }
        });
    }, [suggestions]);

    const handleSearch = async () => {
        const response = await fetch(`http://localhost:5000/search-cars?search_term=${encodeURIComponent(query)}`);
        const data = await response.json();
        console.log(data);
        setCars(data["cars"]);
    };

    const handleInputChange = (event) => {
        setQuery(event.target.value);
    };

    const registerCar = async (car_id) => {
        try {
            const response = await fetch(`http://localhost:5000/register-car`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ user_id: localStorage.getItem('user_id'), car_id: car_id })
            });
            if (response.ok) {
                alert('Car registered successfully to your collection!');
            } else {
                alert('Failed to register car. Please try again.');
            }
        } catch (error) {
            console.error('Error registering car:', error);
            alert('An error occurred. Please try again.');
        }
    };

    return (
        <div className = "container">
            <div className="search-box">
                <input
                    type="text"
                    ref={searchRef}
                    value={query}
                    onChange={handleInputChange}
                    className="search-input"
                    placeholder="Search for a car model"
                />
                <button onClick={handleSearch} className="search-button">Search</button>
            </div>
            <div>
                {cars.map(car => (
                    <div key={car.car_id} className="car-card">
                        <img src={car.image_path} alt={car.model} />
                        <h2>{car.model}</h2>
                        <button onClick={() => registerCar(car.car_id)} className="register-button">Register</button>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default CarBrowser;






