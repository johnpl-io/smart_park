import React, { useEffect, useRef, useState } from 'react';
import './Map.css';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet-routing-machine';


const MapComponent = () => {
    const mapRef = useRef(null);
    const dotRef = useRef(null);
    const [isParked, setIsParked] = useState(false);
    const [parkingSpots, setParkingSpots] = useState([]);
    const [selectedSpot, setSelectedSpot] = useState(null);
    const routingControlRef = useRef(null);
    const [dotPosition, setDotPosition] = useState([40.76, -73.93]);
    const [zoomLevel, setZoomLevel] = useState(13); // Default zoom level
    const [showHeatmap, setShowHeatmap] = useState(false);
    const heatmapImageRef = useRef(null);
    const checkIfOnStreetRef = useRef(null);


    useEffect(() => {
        if (selectedSpot && mapRef.current) {
            if (routingControlRef.current) {
                // Update the existing routing control instead of creating a new one
                routingControlRef.current.setWaypoints([
                    L.latLng(40.76, -73.93),  // Your dynamic starting point
                    L.latLng(selectedSpot.lat, selectedSpot.lng)
                ]);
            } else {
                // Create the routing control if it does not exist
                routingControlRef.current = L.Routing.control({
                    waypoints: [
                        L.latLng(40.76, -73.93),
                        L.latLng(selectedSpot.lat, selectedSpot.lng)
                    ],
                    routeWhileDragging: true,
                    show: false  // Set to false to prevent automatic UI display
                }).addTo(mapRef.current);
            }
        }
    }, [selectedSpot]);
    
    useEffect(() => {
        const map = L.map('map', {
            center: dotPosition,
            zoom: zoomLevel,
            layers: [
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    maxZoom: 30,
                    attribution: '© OpenStreetMap'
                })
            ]
        });
        


        mapRef.current = map;

        
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
            }
        



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
            //map.off('moveend', fetchAndDisplayHeatmapData);
            mapRef.current.remove(); // Safely remove the map
        };
    }, [isParked]); // Depend on isParked to rebind the event listener when the parking status changes


    const generateParkingSpots = () => {
        const spots = Array.from({ length: 10 }, () => ({
            lat: 40.7 + Math.random() * 0.1 - 0.05,  // Latitude around Manhattan
            lng: -73.98 + Math.random() * 0.1 - 0.05  // Longitude around Manhattan
        }));
        setParkingSpots(spots);
        console.log(parkingSpots);
    };

    
    useEffect(() => {
        const fetchParkedStatus = async () => {
            const user_id = 1;
            const car_id = 1;
            const url = `http:localhost:5000/check-parked?user_id=${user_id}&car_id=${car_id}`;

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

        checkIfOnStreetRef.current(dotLatLng, async (isOnStreet) => {
            if (isOnStreet) {
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
        }
            else {
                alert("You're not on a street!");
            }
        });
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
    
    const toggleHeatmapVisibility = () => {
        if (!showHeatmap) {
            fetchAndDisplayHeatmapData();
        } else {
            if (heatmapImageRef.current) {
                mapRef.current.removeLayer(heatmapImageRef.current);
                heatmapImageRef.current = null;
                setShowHeatmap(false);
            }
        }
    };

    const fetchAndDisplayHeatmapData = async () => {
        const bounds = mapRef.current.getBounds();
        const response = await fetch(`http://localhost:5000/get-parked-cars?sw_lat=${bounds.getSouthWest().lat}&sw_lon=${bounds.getSouthWest().lng}&ne_lat=${bounds.getNorthEast().lat}&ne_lon=${bounds.getNorthEast().lng}`);
        if (!response.ok) {
            console.error('Failed to fetch heatmap data');
            return;
        }

        const data = await response.json()
        const imageUrl = `data:image/png;base64,${data.image}`;
        console.log(imageUrl);

        if (heatmapImageRef.current) {
            mapRef.current.removeLayer(heatmapImageRef.current);
        }

        heatmapImageRef.current = L.imageOverlay(imageUrl, bounds).addTo(mapRef.current);
        setShowHeatmap(true);
    };



    return (
        <div>
            <div id="map">
                <div className="select-container">
                    {parkingSpots.length > 0 && (
                        <select onChange={(e) => setSelectedSpot(parkingSpots[parseInt(e.target.value, 10)])}>
                            <option value="">Select a parking spot</option>
                            {parkingSpots.map((spot, index) => (
                                <option key={index} value={index}>
                                    {`Lat: ${spot.lat.toFixed(3)}, Lng: ${spot.lng.toFixed(3)}`}
                                </option>
                            ))}
                        </select>
                    )}
                </div>
            </div>
            <button id="parkButton" onClick={handleParkButtonClick} disabled={isParked}>Park Here</button>
            <button id="UnparkButton" onClick={handleUnparkButtonClick} disabled={!isParked}>Leave Park</button>
            <button id="findParkingButton" onClick={generateParkingSpots}>Find Parking</button>
            <button id="toggleHeatmapButton" onClick={toggleHeatmapVisibility}>{showHeatmap ? 'Hide Heatmap' : 'Show Heatmap'}</button>
        </div>
    );
}
        
    

export default MapComponent;
