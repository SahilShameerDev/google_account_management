import React, { useState, useEffect } from "react";
import axios from "axios";
import { Link, useNavigate } from "react-router-dom";
import './Profile.css';

function Profile() {
  const [isAdmin, setIsAdmin] = useState(false);
  const [message, setMessage] = useState("");
  const [user, setUser] = useState("");
  const  navigate  = useNavigate();

  useEffect(() => {
    const userData = JSON.parse(localStorage.getItem("user"));

    if (!userData) {
      navigate("/"); // If user data is not found, redirect to homepage
      return;
    }

    const user_id = userData.user_id;
    setUser(userData.username);

    const checkAdminStatus = async () => {
      try {
        const response = await axios.post("http://localhost:5000/check_admin", { user_id });
        setIsAdmin(response.data.is_admin);
      } catch (error) {
        setMessage("Error: " + error.response.data.message);
      }
    };

    checkAdminStatus();
  }, [navigate]);

   // Function to handle logout
   const handleLogout = () => {
    // Clear all local storage data
    localStorage.clear();
    // Redirect to the homepage
    navigate("/");
  };

  return (
    <div className="profile-container">
      <button className="logout-btn" onClick={handleLogout}>
        Logout
      </button>

      <h2>User Profile</h2>
      {user && <p>Welcome, {user}!</p>}
      {message && <p className="error-message">{message}</p>}
      <Link className="service-btn" to="/service">
        Go to Services
      </Link>
      <br />
      <br />
      {isAdmin && (
        <Link className="admin-btn" to="/admin">
          Go to Admin Dashboard
        </Link>
      )}
    </div>
  );
}

export default Profile;
