import React, { useEffect, useRef } from 'react';
import './Map.css';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

const MapComponent = () => {
    const mapRef = useRef(null);
    const dotRef = useRef(null);
    const checkIfOnStreetRef = useRef(null);

    useEffect(() => {
        mapRef.current = L.map('map', {
            center: [51.505, -0.09],
            zoom: 13,
            layers: [
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    maxZoom: 30,
                    attribution: '© OpenStreetMap'
                })
            ]
        });

        dotRef.current = L.circleMarker([51.505, -0.09], {
            radius: 10,
            fillColor: "#ff7800",
            color: "#000",
            weight: 1,
            opacity: 1,
            fillOpacity: 0.8
        }).addTo(mapRef.current);

        checkIfOnStreetRef.current = (latlng, callback) => {
            
            fetch(`http://localhost:2000/api/places?lat=${latlng.lat}&lng=${latlng.lng}`)
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    if (data.status === 'OK' && data.results.length > 0) {
                        var isOnStreet = data.results.some(place => place.types.includes('route'));
                        callback(isOnStreet);
                    } else {
                        callback(false);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    callback(false);
                });
            };

        let speed = 1e-6; // Initial speed factor for movement
        const handleKeyDown = (e) => {
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
            mapRef.current.panTo(currentPos);
        };
        document.addEventListener('keydown', handleKeyDown);
        return () => {
            document.removeEventListener('keydown', handleKeyDown);
            mapRef.current.remove();
        };
    }, []);

    const handleParkButtonClick = () => {
        const dotLatLng = dotRef.current.getLatLng();
        checkIfOnStreetRef.current(dotLatLng, (isOnStreet) => {
            if (isOnStreet) {
                alert("You can park here!");
            } else {
                alert("You're not on a street!");
            }
        });
    };

    return (
        <div>
            <div id="map"></div>
            <button id="parkButton" onClick={handleParkButtonClick}>Check Parking</button>
        </div>
    );
};

export default MapComponent;
