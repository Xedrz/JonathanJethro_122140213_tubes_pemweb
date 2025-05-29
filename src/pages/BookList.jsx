// src/pages/BookList.jsx
import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchBooks, updateBookStatus, updateBookRating, deleteBook } from '../feature/bookSlice';
import BookCard from '../components/BookCard';

const BookList = () => {
  const dispatch = useDispatch();
  const books = useSelector((state) => state.books.books);  // Ambil buku dari state Redux
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    dispatch(fetchBooks(searchQuery));  // Panggil fetchBooks untuk mendapatkan daftar buku
  }, [searchQuery, dispatch]);

  const handleStatusChange = (bookId, status) => {
    dispatch(updateBookStatus({ id: bookId, status }));
  };

  const handleRatingChange = (bookId, rating) => {
    dispatch(updateBookRating({ id: bookId, rating }));
  };

  const handleDelete = (bookId) => {
    dispatch(deleteBook(bookId));  // Panggil aksi deleteBook
  };

  return (
    <div className="p-6">
      <input
        type="text"
        placeholder="Cari buku..."
        className="p-2 border rounded-md mb-4"
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}  // Perbarui query pencarian
      />
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {books.map((book) => (
          <BookCard 
            key={book.id} 
            book={book} 
            onStatusChange={handleStatusChange} 
            onRatingChange={handleRatingChange}
            onDelete={handleDelete} // Menambahkan fungsi delete
          />
        ))}
      </div>
    </div>
  );
};

export default BookList;
