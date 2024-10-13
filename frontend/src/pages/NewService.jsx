import React, { useState } from 'react';
import axios from 'axios';

const NewService = () => {
  const [serviceName, setServiceName] = useState('');
  const [description, setDescription] = useState('');
  const [url, setUrl] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const newService = {
      service_name: serviceName,
      description: description,
      url: url,
    };

    try {
      const response = await axios.post('http://localhost:5000/add_service', newService);
      setMessage(response.data.message);
      // Clear the form on success
      setServiceName('');
      setDescription('');
      setUrl('');
    } catch (error) {
      if (error.response) {
        setMessage(error.response.data.message);
      } else {
        setMessage('Error adding service');
      }
    }
  };

  return (
    <div>
      <h2>Add New Service</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Service Name:</label>
          <input
            type="text"
            value={serviceName}
            onChange={(e) => setServiceName(e.target.value)}
            required
          />
        </div>
        
        <div>
          <label>URL:</label>
          <input
            type="text"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
          />
        </div>
        <button type="submit">Add Service</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
};

export default NewService;
