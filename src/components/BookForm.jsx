import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { addBook } from '../services/bookService';

const BookForm = ({ bookData = null }) => {
  const [title, setTitle] = useState(bookData ? bookData.title : '');
  const [author, setAuthor] = useState(bookData ? bookData.author : '');
  const [rating, setRating] = useState(bookData ? bookData.rating : '');
  const [status, setStatus] = useState(bookData ? bookData.status : '');
  const [description, setDescription] = useState(bookData ? bookData.description : '');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    const book = { title, author, rating, status, description };
    if (bookData) {
      // Update book
      // Call API to update
    } else {
      // Add new book
      await addBook(book);
    }

    navigate('/books');
  };

  return (
    <div className="p-6 max-w-4xl mx-auto bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-semibold mb-4">{bookData ? 'Edit Buku' : 'Tambah Buku'}</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label htmlFor="title" className="block text-lg">Judul Buku</label>
          <input
            id="title"
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full p-2 mt-1 border rounded-md"
            required
          />
        </div>
        <div className="mb-4">
          <label htmlFor="author" className="block text-lg">Penulis</label>
          <input
            id="author"
            type="text"
            value={author}
            onChange={(e) => setAuthor(e.target.value)}
            className="w-full p-2 mt-1 border rounded-md"
            required
          />
        </div>
        <div className="mb-4">
          <label htmlFor="rating" className="block text-lg">Rating</label>
          <input
            id="rating"
            type="number"
            value={rating}
            onChange={(e) => setRating(e.target.value)}
            className="w-full p-2 mt-1 border rounded-md"
            min="1" max="5"
            required
          />
        </div>
        <div className="mb-4">
          <label htmlFor="status" className="block text-lg">Status</label>
          <select
            id="status"
            value={status}
            onChange={(e) => setStatus(e.target.value)}
            className="w-full p-2 mt-1 border rounded-md"
            required
          >
            <option value="Belum Dibaca">Belum Dibaca</option>
            <option value="Sedang Dibaca">Sedang Dibaca</option>
            <option value="Selesai Dibaca">Selesai Dibaca</option>
          </select>
        </div>
        <div className="mb-4">
          <label htmlFor="description" className="block text-lg">Deskripsi</label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full p-2 mt-1 border rounded-md"
            rows="4"
          />
        </div>
        <button type="submit" className="px-6 py-2 bg-blue-600 text-white rounded-lg">
          {bookData ? 'Update Buku' : 'Tambah Buku'}
        </button>
      </form>
    </div>
  );
};

export default BookForm;
