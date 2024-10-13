    import React, { useState, useEffect } from 'react';
    import axios from 'axios';
    import { useParams, useNavigate } from 'react-router-dom'; // Add useNavigate for navigation
    import './UserDetailsPage.css'; // Assuming custom styles for the page

    const UserDetailsPage = () => {
    const { userId } = useParams(); // Extract userId from URL
    const [services, setServices] = useState([]);
    const [allServices, setAllServices] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [newServiceId, setNewServiceId] = useState('');
    const navigate = useNavigate(); // Use useNavigate for redirection

    useEffect(() => {
        const fetchUserServices = async () => {
        try {
            const response = await axios.post('http://localhost:5000/get_services', { user_id: userId });
            setServices(response.data.services);
        } catch (err) {
            setError('Failed to load user services.');
        } finally {
            setLoading(false);
        }
        };

        const fetchAllServices = async () => {
        try {
            const response = await axios.get('http://localhost:5000/services'); // Fetch all available services
            setAllServices(response.data.services);
        } catch (err) {
            setError('Failed to load available services.');
        }
        };

        fetchUserServices();
        fetchAllServices();
    }, [userId]);

    const handleAddService = async () => {
        if (!newServiceId) {
        setError('Please select a service to add.');
        return;
        }

        try {
        const response = await axios.post('http://localhost:5000/assign_privilege', {
            user_id: userId,
            service_id: newServiceId,
        });

        if (response.status === 200) {
            setServices([...services, response.data.service]); // Add the new service to the list
            setError(''); // Clear any existing errors
        }
        } catch (err) {
        setError('Failed to add service. The service may already exist.');
        }
    };

    // Handle redirection to /admin/add_new_services
    const handleNavigateToAddService = () => {
        navigate('/admin/add_new_services');
    };

    if (loading) {
        return <div className="loading">Loading user services...</div>;
    }

    if (error) {
        return <div className="error">{error}</div>;
    }

    return (
        <div className="user-details-page">
        <h2 className="page-title">User Services</h2>

        {services.length > 0 ? (
            <ul className="service-list">
            {services.map((service) => (
                <li key={service.service_id} className="service-item">
                {service.service_name}
                </li>
            ))}
            </ul>
        ) : (
            <p>No services available for this user.</p>
        )}

        <div className="add-service-section">
            <h3 className="section-title">Add Service</h3>
            <div className="service-dropdown">
            <select
                onChange={(e) => setNewServiceId(e.target.value)}
                value={newServiceId}
                className="service-select"
            >
                <option value="">Select a service</option>
                {allServices.map((service) => (
                <option key={service.service_id} value={service.service_id}>
                    {service.service_name}
                </option>
                ))}
            </select>
            </div>
            <button className="add-service-btn" onClick={handleAddService}>
            Add Service
            </button>
        </div>

        {/* Round floating button */}
        <button className="floating-button" onClick={handleNavigateToAddService}>
            +
        </button>
        </div>
    );
    };

    export default UserDetailsPage;
