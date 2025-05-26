// src/pages/AddBook.jsx
import React, { useState } from 'react';
import { addBook } from '../services/api'; // Pastikan addBook diimpor dengan benar

const AddBook = () => {
  const [bookData, setBookData] = useState({
    title: '',
    author: '',
    published_date: '',
    cover_url: '',
    description: '',
    pages: '',
    status: '',
    rating: '',
    notes: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setBookData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const result = await addBook(bookData);
      alert('Buku berhasil ditambahkan!');
      console.log(result);
    } catch (error) {
      alert('Gagal menambahkan buku.');
      console.error(error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* Form fields for bookData */}
      <button type="submit">Add Book</button>
    </form>
  );
};

export default AddBook;
