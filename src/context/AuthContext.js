// context/AuthContext.js
import React, { createContext, useState, useContext } from 'react';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(localStorage.getItem('token') || null);  // Ambil token dari localStorage

  const value = {
    token,
    setToken: (newToken) => {
      setToken(newToken);
      localStorage.setItem('token', newToken); // Menyimpan token di localStorage
    }
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
