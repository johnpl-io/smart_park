import React, { useState, useEffect, useRef } from 'react';
import './BrowseCars.css';
import $ from 'jquery';
import 'jquery-ui/ui/widgets/autocomplete'; 
import { FaInfoCircle, FaCar, FaSignOutAlt, FaSearch, FaCog, FaPlayCircle } from 'react-icons/fa';
import {getAuth, signOut} from "firebase/auth";
import { useNavigate } from 'react-router-dom';

const CarBrowser = () => {
    const [query, setQuery] = useState('');
    const [cars, setCars] = useState([]);
    const [suggestions, setSuggestions] = useState([]);
    const searchRef = useRef(null);

    const [sidebarOpen, setSidebarOpen] = useState(true);
    const auth = getAuth();
    const navigate = useNavigate();

    const handleLogout = (event) => {       
    
        event.preventDefault();
        signOut(auth).then(() => {
        // Sign-out successful.
            navigate("/");
            console.log("Signed out successfully")
        }).catch((error) => {
        // An error happened.
        });
    }

    const toggleSidebar = () => {
        setSidebarOpen(!sidebarOpen);
    };

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
            console.log(response);
            if (response.ok) {
                alert('Car registered successfully to your collection!');
            } else {
                
                alert('You already registered this car!');
            }
        } catch (error) {
            
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

            <div className={`sidebar ${sidebarOpen ? 'open' : ''}`}>
                    <div className="menu">
                    <ul className="menu-list">
                        <li><button onClick={() => { window.location.href = "/AboutUs"; }}><FaInfoCircle /> About Us</button></li>
                        <li><button onClick={() => { window.location.href = "/UserProfile"; }}><FaCog /> Account Settings</button></li> {/* Changed icon to FaCog */}
                        <li><button onClick={() => { window.location.href = "/Garage"; }}><FaCar /> Garage</button></li>
                        <li><button onClick={() => { window.location.href = "/BrowseCars"; }}><FaSearch /> Browse Cars</button></li> {/* Changed icon to FaSearch */}
                        <li><button onClick={() => { window.location.href = "/"; }}><FaPlayCircle /> Start Driving</button></li> {/* Changed icon to FaSearch */}
                        <li><button onClick={(e) => handleLogout(e)}><FaSignOutAlt /> Logout</button></li>
                    </ul>
                    </div>
            </div>
            
            <button className={`toggle-button ${sidebarOpen ? 'open' : ''}`} onClick={toggleSidebar}>
                <span></span>
            </button>
        </div>
    );
};

export default CarBrowser;






