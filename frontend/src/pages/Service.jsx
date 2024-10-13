import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Service.css'; 

const Service = () => {
    const userId = JSON.parse(localStorage.getItem("user")).user_id;
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Fetch services available to the user on component mount
  useEffect(() => {
    const fetchServices = async () => {
      try {
        const response = await axios.post('http://localhost:5000/get_services', { user_id: userId });
        setServices(response.data.services);
        setLoading(false);
      } catch (err) {
        setError('Failed to load services. Please try again later.');
        setLoading(false);
      }
    };

    fetchServices();
  }, [userId]);

  if (loading) {
    return <div>Loading services...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div className="services-container">
      <h2>Available Services</h2>
      <div className="services-list">
        {services.length > 0 ? (
          services.map(service => (
            <div className="service-card" key={service.service_id}>
              <h3>{service.service_name}</h3>
              <p>{service.description}</p>
              <a href={service.url} target="_blank" rel="noopener noreferrer" className="service-link">
                Go to {service.service_name}
              </a>
            </div>
          ))
        ) : (
          <p>No services available for this user.</p>
        )}
      </div>
    </div>
  );
};

export default Service;
