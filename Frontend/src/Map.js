import React, { useEffect, useRef, useState } from 'react';
import './Map.css';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

const MapComponent = () => {
    const mapRef = useRef(null);
    const dotRef = useRef(null);
    const [isParked, setIsParked] = useState(false);
    const [dotPosition, setDotPosition] = useState([51.505, -0.09]); // Default position
    const [zoomLevel, setZoomLevel] = useState(13); // Default zoom level


    useEffect(() => {
        mapRef.current = L.map('map', {
            center: dotPosition, // Initialize map center with dot position
            zoom: zoomLevel,
            layers: [
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    maxZoom: 30,
                    attribution: '© OpenStreetMap'
                })
            ]
        });

        dotRef.current = L.circleMarker(dotPosition, {
            radius: 10,
            fillColor: "#ff7800",
            color: "#000",
            weight: 1,
            opacity: 1,
            fillOpacity: 0.8
        }).addTo(mapRef.current);

        mapRef.current.on('zoomend', () => {
            setZoomLevel(mapRef.current.getZoom());
        });

        let speed = 1e-6; // Initial speed factor for movement
        const handleKeyDown = (e) => {
            if (isParked) return; // Ignore key presses when parked
            let currentPos = dotRef.current.getLatLng();
            switch (e.key) {
                case "ArrowUp":    currentPos.lat += speed; break;
                case "ArrowDown":  currentPos.lat -= speed; break;
                case "ArrowLeft":  currentPos.lng -= speed; break;
                case "ArrowRight": currentPos.lng += speed; break;
                case "w": case "W": // Increase speed
                    speed = Math.min(1e-3, speed + 5e-6);
                    break;
                case "s": case "S": // Decrease speed
                    speed = Math.max(1e-8, speed - 5e-6);
                    break;
                default: return; // Exit this handler for other keys
            }
            dotRef.current.setLatLng(currentPos);
            setDotPosition([currentPos.lat, currentPos.lng]);
            mapRef.current.panTo(currentPos);
        };
        document.addEventListener('keydown', handleKeyDown);
        return () => {
            document.removeEventListener('keydown', handleKeyDown);
            mapRef.current.off('zoomend');
            mapRef.current.remove(); // Safely remove the map
        };
    }, [isParked]); // Depend on isParked to rebind the event listener when the parking status changes


    useEffect(() => {
        const fetchParkedStatus = async () => {
            // Assume user_id and car_id are somehow determined (hardcoded here for simplicity)
            const user_id = 1;
            const car_id = 1;
            const url = `http://localhost:5000/check-parked?user_id=${user_id}&car_id=${car_id}`;

            const response = await fetch(url, {
                method: "GET",
                headers: { "Content-Type": "application/json" },
            });

        
            const data = await response.json();
            console.log(data);
            if (response.ok) {
                setIsParked(data.isParked);
                if (data.isParked && data.location) {
                    setDotPosition([data.location[0], data.location[1]]);
                }
            }
        };
        fetchParkedStatus();
    }, []);

    const handleParkButtonClick = async () => {
        const dotLatLng = dotRef.current.getLatLng();
        const response = await fetch("http://localhost:5000/park", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                user_id: 1, // Example user ID
                car_id: 1, // Example car ID
                location: [dotLatLng.lat, dotLatLng.lng] // Using the current position
            })
        });

        if (response.ok) {
            setIsParked(true);
            setDotPosition([dotLatLng.lat, dotLatLng.lng]);
            alert("Successfully parked!");
        } else {
            alert("Failed to park. Please try again.");
        }
    };

    const handleUnparkButtonClick = async () => {
        const response = await fetch("http://localhost:5000/leave", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                user_id: 1,
                car_id: 1
            })
        });

        if (response.ok) {
            setIsParked(false);
            alert("Successfully unparked! You can start driving now.");
        } else {
            alert("Failed to unpark. Please try again.");
        }
    };

    return (
        <div>
            <div id="map"></div>
            <button id="parkButton" onClick={handleParkButtonClick} disabled={isParked}>Park Here</button>
            <button id="UnparkButton" onClick={handleUnparkButtonClick} disabled={!isParked}>Leave Park</button>
        </div>
    );
};

export default MapComponent;
