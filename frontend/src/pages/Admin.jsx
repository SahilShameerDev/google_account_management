import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Admin.css'; 
import { useNavigate } from 'react-router-dom';

function Admin() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const history = useNavigate();
  const user_id = JSON.parse(localStorage.getItem("user")).user_id;

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await axios.post('http://localhost:5000/get_users', { user_id: user_id });
        setUsers(response.data.users);
        setLoading(false);
      } catch (err) {
        setError('Failed to load users. Please try again later.');
        setLoading(false);
      }
    };

    fetchUsers();
  }, [user_id]);
  const handleMoreDetails = (userId) => {
    // Navigate to the More Details page for the user
    history(`/admin/${userId}/details`);
  };

  if (loading) {
    return <div>Loading users...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }


  return (
    <div className="admin-container">
      <h2>Admin Dashboard</h2>
      <table>
        <thead>
          <tr>
            <th>User ID</th>
            <th>Username</th>
            <th>Email</th>
          </tr>
        </thead>
        <tbody>
          {users.map(user => (
            <tr key={user.user_id}>
              <td>{user.user_id}</td>
              <td>{user.username}</td>
              <td>{user.email}</td>
              <button onClick={() => handleMoreDetails(user.user_id)}>
              View More Details
            </button>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Admin;
