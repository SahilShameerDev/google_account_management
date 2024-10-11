import React, { useState, useEffect } from 'react';
import axios from 'axios';


function Profile() {
  const [isAdmin, setIsAdmin] = useState(false);
  const [message, setMessage] = useState('');
  const[users, setUsers] = useState([]);

  useEffect(()=>{
    const userData = JSON.parse(localStorage.getItem('user'));
    const userId = userData ? userData.user.id : null;
  })

  useEffect(() => {
    const userData = JSON.parse(localStorage.getItem('user'));
    const user_id = userData ? userData.user.id : null;

    // Call the check_admin API when the profile page loads
    const checkAdminStatus = async () => {
      try {
        const response = await axios.post('http://localhost:5000/check_admin', { user_id });
        setIsAdmin(response.data.is_admin);
      } catch (error) {
        setMessage('Error: ' + error.response.data.message);
      }
    };

    checkAdminStatus();
  }, []);

  return (
    <div className="profile-container">
      <h2>User Profile</h2>
      {/* Display a message if there's any */}
      {message && <p>{message}</p>}

      {/* Conditionally render the admin button if the user is an admin */}
      {isAdmin && (
        <button className="admin-btn">Go to Admin Dashboard</button>
      )}
    </div>
  );
}

export default Profile;
