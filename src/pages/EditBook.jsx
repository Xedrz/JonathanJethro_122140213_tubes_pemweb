// src/pages/EditBook.jsx
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';  // Ganti useHistory dengan useNavigate
import { updateBook } from '../services/api'; // Pastikan updateBook diimpor dengan benar

const EditBook = () => {
  const { bookId } = useParams();
  const navigate = useNavigate();  // Ganti useHistory dengan useNavigate
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

  useEffect(() => {
    // Fetch book data by ID and populate form
    const fetchBook = async () => {
      const response = await fetch(`http://localhost:6543/api/books/${bookId}`);
      const data = await response.json();
      setBookData(data.book);
    };
    fetchBook();
  }, [bookId]);

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
      const result = await updateBook(bookId, bookData);
      alert('Buku berhasil diperbarui!');
      navigate('/'); // Redirect ke halaman utama atau daftar buku
    } catch (error) {
      alert('Gagal memperbarui buku.');
      console.error(error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* Form fields for bookData */}
      <button type="submit">Update Book</button>
    </form>
  );
};

export default EditBook;
