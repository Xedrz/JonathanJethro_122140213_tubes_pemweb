// src/context/BookContext.js
import React, { createContext, useState, useContext, useEffect } from 'react';

const BookContext = createContext();

export const useBooks = () => {
  return useContext(BookContext);
};

export const BookProvider = ({ children }) => {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    fetch('http://localhost:6543/api/books')
      .then((response) => response.json())
      .then((data) => {
        setBooks(data.books);
        setLoading(false);
      })
      .catch((err) => {
        setError('Failed to fetch books');
        setLoading(false);
      });
  }, []);

  return (
    <BookContext.Provider value={{ books, loading, error }}>
      {children}
    </BookContext.Provider>
  );
};
