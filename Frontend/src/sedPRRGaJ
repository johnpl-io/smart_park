import React, { useState, useEffect } from 'react';
import './UserProfile.css';
import { getAuth, signOut } from "firebase/auth";
import { useNavigate } from 'react-router-dom';

const UserProfilePage = () => {
  const [userDetails, setUserDetails] = useState({ username: '', user_id: '', user_email: '', created_on: ''});
  const navigate = useNavigate();
  const auth = getAuth();

  useEffect(() => {
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
          created_on: userDetailsData.created_on

        });
      } catch (error) {
        console.error("Error fetching user details:", error);
      }
    };
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
      <h1>Welcome, {userDetails.username}</h1>
      <p>User_ID: {userDetails.user_id}</p>
      <p>User_Email: {userDetails.user_email}</p>
      <p>Created On: {userDetails.created_on}</p>
      <div className="button-container">
          <button onClick={handleLogout}>Logout</button>
          <button onClick={() => { window.location.href = "/"; }}>Back to Menu</button>
      </div>
    </div>
  );
};


export default UserProfilePage;