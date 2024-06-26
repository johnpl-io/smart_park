import React, { useEffect, useRef, useState } from 'react';
import './Map.css';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet-routing-machine';
import { FaInfoCircle, FaCar, FaSignOutAlt, FaSearch, FaCog, FaPlayCircle } from 'react-icons/fa';
import {getAuth, signOut} from "firebase/auth";
import { useNavigate } from 'react-router-dom';


delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
    iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
    iconUrl: require('leaflet/dist/images/marker-icon.png'),
    shadowUrl: require('leaflet/dist/images/marker-shadow.png')
});

const MapComponent = () => {
    const mapRef = useRef(null);
    const dotRef = useRef(null);
    const [isParked, setIsParked] = useState(false);
    const [parkingSpots, setParkingSpots] = useState([]);
    const [selectedSpot, setSelectedSpot] = useState(null);
    const routingControlRef = useRef(null);
    const [dotPosition, setDotPosition] = useState([40.7281, -73.9916]);
    const [zoomLevel, setZoomLevel] = useState(13); // Default zoom level
    const [showHeatmap, setShowHeatmap] = useState(false);
    const heatmapImageRef = useRef(null);
    const checkIfOnStreetRef = useRef(null);
    const [loading, setLoading] = useState(false);

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

    const handleReserveSpotClick = async () => {
        const dotLatLng = dotRef.current ? dotRef.current.getLatLng() : null;

        /*
        checkIfOnStreetRef.current(dotLatLng, async (isOnStreet) => {
            if (!isOnStreet) {
                alert("You're not on a street! Please move the street to reserve a spot!.");
                return;
            }
    */
        if (selectedSpot && mapRef.current && dotLatLng) {

            const user_id = localStorage.getItem("user_id");
            const car_id = localStorage.getItem("car_id");
        

            const response = await fetch(`http://localhost:5000/get-hold?user_id=${user_id}&car_id=${car_id}&spot_id=${selectedSpot.spot_id}`)

            if (response.status == 300) {
                alert("You already have a hold on that spot!")
                return
            }
            if (!response.ok) {
                alert("Failed to reserve parking spot!")
                return;
            }
            else{
                alert("Successfully reserved parking spot!");
            }
            if (routingControlRef.current) {
                try {
                    routingControlRef.current.setWaypoints([
                        L.latLng(dotLatLng.lat, dotLatLng.lng),
                        L.latLng(selectedSpot.location[0], selectedSpot.location[1])
                    ]);
                } catch (error) {
                    console.error("Error updating waypoints:", error);
                }
            } else {
                routingControlRef.current = L.Routing.control({
                    waypoints: [
                        L.latLng(dotLatLng.lat, dotLatLng.lng),
                        L.latLng(selectedSpot.location[0], selectedSpot.location[1])
                    ],
                    routeWhileDragging: false,
                    show: false,
                    addWaypoints: false,
                    lineOptions: {
                        styles: [{color: '#6FA1EC', weight: 4}]
                    }
                }).addTo(mapRef.current);
            }
        } else {
            console.error("Please select one of the recommended parking spots!");
            alert('Please select one of the recommended spots!');
        }
    //})
    };
    
    
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
        }, {zoomAnimation:false});
        


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


    const generateParkingSpots = async () => {

        setLoading(true);
        try {
            const user_id = localStorage.getItem("user_id");
            const car_id = localStorage.getItem("car_id");

            if(car_id == null){
                alert("Please first select a car in the garage!");
                return;
            }
            let currentPos = dotRef.current.getLatLng();

            const response = await fetch(`http://localhost:5000/find-closest-free-spot?user_id=${user_id}&car_id=${car_id}&lon=${currentPos.lng}&lat=${currentPos.lat}`);
            if (!response.ok) {
                throw new Error('Failed to fetch parking spots');
            }
            const spots = await response.json();
            setParkingSpots(spots);
        } catch (error) {
            console.error('Error fetching parking spots:', error);
            alert('Failed to load parking spots. Please try again.');
        } finally {
            setLoading(false);
        }
    };
    

    
    useEffect(() => {
        const fetchParkedStatus = async () => {
            
            const user_id = localStorage.getItem('user_id');
            const car_id = localStorage.getItem('car_id');

            if (car_id != null) {

                console.log(user_id);
                console.log(car_id);
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
            }
        };
        fetchParkedStatus();
    }, []);

    const handleParkButtonClick = async () => {

        const dotLatLng = dotRef.current.getLatLng();

        const user_id = localStorage.getItem('user_id');
        const car_id = localStorage.getItem('car_id');
        
        console.log(user_id);
        console.log(car_id);
        if (car_id == null) {
            alert("Please first select a car in the garage!");
            return;
        }

        checkIfOnStreetRef.current(dotLatLng, async (isOnStreet) => {
            if (isOnStreet) {
                const response = await fetch("http://localhost:5000/park", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    user_id: user_id,
                    car_id: car_id,
                    location: [dotLatLng.lat, dotLatLng.lng] // Using the current position
                })
            });
           
            if (response.ok) {
                setIsParked(true);
                setDotPosition([dotLatLng.lat, dotLatLng.lng]);
                alert("Successfully parked!");
                
            } else if (response.status == 300) {
                alert("Someone is already parked here!");
                
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
        
        const user_id = localStorage.getItem('user_id');
        const car_id = localStorage.getItem('car_id');

        if (car_id == null) {
            alert("Please first select a car in the garage!");
            return;
        }

        const response = await fetch("http://localhost:5000/leave", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                user_id: user_id,
                car_id: car_id
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

        setLoading(true);
        disableMapInteractions(); 
        const bounds = mapRef.current.getBounds();

        const response = await fetch(`http://localhost:5000/get-parked-cars?sw_lat=${bounds.getSouthWest().lat}&sw_lon=${bounds.getSouthWest().lng}&ne_lat=${bounds.getNorthEast().lat}&ne_lon=${bounds.getNorthEast().lng}`);
        if (!response.ok) {
            console.error('Failed to fetch heatmap data');
            setLoading(false);
            return;
        }

        const data = await response.json()

        if (data.image == null)
        {
            setLoading(false);
            alert('No parked cars found!');
            return;

        }
        const imageUrl = `data:image/png;base64,${data.image}`;

        if (heatmapImageRef.current) {
            mapRef.current.removeLayer(heatmapImageRef.current);
        }
        const customBounds =  L.latLngBounds(
            L.latLng(data.bounds["min_lat"], data.bounds["min_lon"]),
            L.latLng(data.bounds["max_lat"], data.bounds["max_lon"])
        );
        
        heatmapImageRef.current = L.imageOverlay(imageUrl, customBounds, { opacity: 0.6 }).addTo(mapRef.current);
        setShowHeatmap(true);

        setLoading(false);
        enableMapInteractions();
    };

    const disableMapInteractions = () => {
        mapRef.current.dragging.disable();
        mapRef.current.touchZoom.disable();
        mapRef.current.doubleClickZoom.disable();
        mapRef.current.scrollWheelZoom.disable();
        mapRef.current.boxZoom.disable();
        mapRef.current.keyboard.disable();
        if (mapRef.current.tap) mapRef.current.tap.disable(); // for mobile devices
    }
    
    const enableMapInteractions = () => {
        mapRef.current.dragging.enable();
        mapRef.current.touchZoom.enable();
        mapRef.current.doubleClickZoom.enable();
        mapRef.current.scrollWheelZoom.enable();
        mapRef.current.boxZoom.enable();
        mapRef.current.keyboard.enable();
        if (mapRef.current.tap) mapRef.current.tap.enable(); // for mobile devices
    }





    return (
        <div className="map-container">
            <div className={`sidebar ${sidebarOpen ? 'open' : ''}`}>
                <div className="menu">
                    <ul className="menu-list">
                        <li><button onClick={() => { window.location.href = "/AboutUs"; }}><FaInfoCircle /> About Us</button></li>
                        <li><button onClick={() => { window.location.href = "/UserProfile"; }}><FaCog /> Account Settings</button></li>
                        <li><button onClick={() => { window.location.href = "/Garage"; }}><FaCar /> Garage</button></li>
                        <li><button onClick={() => { window.location.href = "/BrowseCars"; }}><FaSearch /> Browse Cars</button></li>
                        <li><button onClick={() => { window.location.href = "/"; }}><FaPlayCircle /> Start Driving</button></li>
                        <li><button onClick={(e) => handleLogout(e)}><FaSignOutAlt /> Logout</button></li>
                    </ul>
                </div>
            </div>

            <button className={`toggle-button ${sidebarOpen ? 'open' : ''}`} onClick={toggleSidebar}>
                <span></span>
            </button>
            <div id="map" className={`map ${sidebarOpen ? 'shifted' : ''}`}>
                <div className="select-container">
                    {parkingSpots.length > 0 && (
                        <>
                            <h3 className="dropdown-title">Recommended Parking Spaces</h3>
                            <select className="parking-dropdown" onChange={(e) => setSelectedSpot(parkingSpots[parseInt(e.target.value, 10)])}>
                                <option value="">Select a parking spot</option>
                                {parkingSpots.map((spot, index) => (
                                    <option key={index} value={index}>
                                        {`Lat: ${spot.location[0].toFixed(3)}, Lng: ${spot.location[1].toFixed(3)}, Last Occupied: ${convertToLocalTime(spot.time_left)}, ${Math.round(parseFloat(spot.distance))} meters away`}
                                    </option>
                                ))}
                            </select>
                        </>
                    )}
                </div>
            </div>

            {loading && <div className="loading-spinner">Loading...</div>}
            <button id="parkButton" onClick={handleParkButtonClick} disabled={isParked}>Park Here</button>
            <button id="UnparkButton" onClick={handleUnparkButtonClick} disabled={!isParked}>Leave Park</button>
            <button id="findParkingButton" onClick={generateParkingSpots}>Find Parking</button>
            <button id="toggleHeatmapButton" onClick={toggleHeatmapVisibility}>{showHeatmap ? 'Hide Heatmap' : 'Show Heatmap'}</button>
            <button id="reserveSpotButton" onClick={handleReserveSpotClick}>Reserve Spot</button>
        </div>
    );

    function convertToLocalTime(time) {
        const userTimeZone = Intl.DateTimeFormat().resolvedOptions().timeZone 
        const utcTime = new Date(time);
        const localTime = new Date(utcTime.toLocaleString("en-US", { timeZone: userTimeZone }));
        return localTime.toLocaleString();
    }
}
        
    

export default MapComponent;
