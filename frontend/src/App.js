import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './pages/Home';
import Register from './pages/Register';
import Login from './pages/Login';
import Profile from './pages/Profile';
import Admin from './pages/Admin';
import './App.css';
import Settings from './pages/Settings';
import Service from './pages/Service';
import UserDetailsPage from './pages/UserDetailsPage';
import NewService from './pages/NewService';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route exact path="/" element={<Home/>} />
          <Route path="/register" element={<Register/>} />
          <Route path="/login" element={<Login/>} />
          <Route path="/profile" element={<Profile/>} />
          <Route path="/admin" element={<Admin/>} />
          <Route path="/settings" element={<Settings/>} />
          <Route path="/service" element={<Service/>} />
          <Route path="/admin/:userId/details" element={<UserDetailsPage/>}/>
          <Route path='/admin/add_new_services' element={<NewService/>}/>
        </Routes>
      </div>
    </Router>
  );
}

export default App;