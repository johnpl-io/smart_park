import React, { useState, useEffect } from 'react';
import './UserProfile.css';
import { getAuth, signOut } from "firebase/auth";
import { useNavigate } from 'react-router-dom';

const UserProfilePage = () => {
  const [userDetails, setUserDetails] = useState({ username: '', user_id: '', user_email:'',
  created_on: '', car_id: ''});
  const [carDetails, setCarDetails] = useState([]);
  const navigate = useNavigate();
  const auth = getAuth();

  useEffect(() => {
    const fetchCarDetails = async () => {
          const user_id = localStorage.getItem("user_id");
          try {
            const carDetailsResponse = await fetch(`http://localhost:5000/find-car-by-user-id?user_id=${user_id}`);
            if (!carDetailsResponse.ok) throw new Error('Failed to fetch car details');
            const carDetailsData = await carDetailsResponse.json();
            setCarDetails(carDetailsData);
          } catch (error) {
            console.error("Error fetching car details:", error);
          }
        };

    const fetchUserDetails = async () => {
      const user_id = localStorage.getItem("user_id");
      console.log("user_id:", user_id);
      try {
        const userDetailsResponse = await fetch(`http://localhost:5000/find-user-by-user-id?user_id=${user_id}`);
        if (!userDetailsResponse.ok) throw new Error('Failed to fetch user details');
        const userDetailsData = await userDetailsResponse.json();

        console.log("User Details Data:", userDetailsData);
        setUserDetails({
          username: userDetailsData.username,
          user_id: userDetailsData.user_id,
          user_email: userDetailsData.email,
          created_on: userDetailsData.created_on,
          car_id: userDetailsData.car_id

        });
      } catch (error) {
        console.error("Error fetching user details:", error);
      }
    };
    fetchCarDetails();
    fetchUserDetails();
  }, []);




  const formatDate = (timestamp) => {
    const [month, day, year] = timestamp.split('/');
    const date = new Date(`${year}-${month}-${day}`);
    return date.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' });
  };

  const handleLogout = () => {
    signOut(auth).then(() => {
      console.log("Signed out successfully");
      navigate("/");
    }).catch((error) => {
      console.error("Sign-out error:", error);
    });
  };

  return (
    <div className="user-profile">
      <div className="top-right">
        <button onClick={handleLogout}>Logout</button>
      </div>
      <div className="top-left">
        <button onClick={() => { window.location.href = "/"; }}>Back to Map</button>
      </div>
      <h1>Welcome, {userDetails.username}</h1>
      <p>User ID: {userDetails.user_id}</p>
      <p>Email Address: {userDetails.user_email}</p>
      <p>Joined on: {userDetails.created_on}</p>
      <div className="car-details">
        <h2>Your Cars</h2>
        <ul>
          {carDetails.map(car => (
            <li key={car.car_id}>
              <strong>Car Model:</strong> {car.car_model}<br />
              <strong>Width:</strong> {car.width}<br />
              <strong>Length:</strong> {car.len}<br />
              <strong>Height:</strong> {car.height}
              <div className="car-image-container">

              <img src={car.image_path} alt={`Car ${car.car_id}`} className="car-image" />
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};


export default UserProfilePage;