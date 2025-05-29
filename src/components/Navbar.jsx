import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import ThemeToggle from './ThemeToggle';
import { useEffect, useState } from 'react';

const Navbar = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    setIsLoggedIn(!!localStorage.getItem('token'));
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <nav className="bg-white dark:bg-gray-900 text-black dark:text-white shadow px-4 py-3 flex justify-between items-center">
      <div className="font-bold text-lg">
        <NavLink to="/" className="hover:underline">Bukuku</NavLink>
      </div>
      <div className="flex gap-4 items-center">
        {isLoggedIn ? (
          <>
            
            <button onClick={handleLogout} className="hover:underline">Logout</button>
          </>
        ) : (
          <>
            <NavLink to="/login" className={({ isActive }) => isActive ? 'underline' : 'hover:underline'}>
              Login
            </NavLink>
            <NavLink to="/register" className={({ isActive }) => isActive ? 'underline' : 'hover:underline'}>
              Register
            </NavLink>
          </>
        )}
        <ThemeToggle />
      </div>
    </nav>
  );
}

export default Navbar;