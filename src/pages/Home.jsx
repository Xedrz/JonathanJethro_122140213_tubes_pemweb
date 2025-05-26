// src/pages/Home.jsx
import React, { useState, useEffect, useCallback } from 'react';
import { getBooks, addBook, deleteBook, updateBook } from '../services/api';
import BookCard from '../components/BookCard';
import Navbar from '../components/Navbar';
import debounce from 'lodash.debounce';

const Home = () => {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [newBook, setNewBook] = useState({ title: '', author: '', rating: 0, status: '' });

  // Debounced fetch function
  const fetchBooks = useCallback(
    debounce((query) => {
      setLoading(true);
      setErrorMessage('');
      getBooks(query)
        .then((res) => {
          if (res.success) {
            setBooks(res.books);
          } else {
            setErrorMessage(res.message || 'Data tidak ditemukan');
            setBooks([]);
          }
          setLoading(false);
        })
        .catch((err) => {
          console.error('Error fetching books:', err);
          setErrorMessage('Gagal mengambil data buku');
          setLoading(false);
        });
    }, 500),
    []
  );

  useEffect(() => {
    fetchBooks(searchQuery);
  }, [searchQuery, fetchBooks]);

  const handleSearchChange = (e) => {
    setSearchQuery(e.target.value);
  };

  const handleDelete = (bookId) => {
    deleteBook(bookId)
      .then(() => {
        setBooks(books.filter((book) => book.id !== bookId));
      })
      .catch((err) => {
        console.error('Error deleting book:', err);
        setErrorMessage('Gagal menghapus buku');
      });
  };

  const handleAddBook = () => {
    if (!newBook.title || !newBook.author) {
      setErrorMessage('Judul dan penulis tidak boleh kosong.');
      return;
    }

    addBook(newBook)
      .then((res) => {
        if (res.success) {
          setBooks([...books, res.book]);
          setNewBook({ title: '', author: '', rating: 0, status: '' });
          setErrorMessage('');
        } else {
          setErrorMessage(res.message || 'Gagal menambahkan buku.');
        }
      })
      .catch((err) => {
        console.error('Error adding book:', err);
        setErrorMessage('Terjadi kesalahan saat menambahkan buku.');
      });
  };

  const handleUpdateRating = (id, rating) => {
    updateBook(id, { rating })
      .then(() => {
        setBooks((prev) =>
          prev.map((b) => (b.id === id ? { ...b, rating } : b))
        );
      })
      .catch((err) => {
        console.error('Error updating rating:', err);
        setErrorMessage('Gagal memperbarui rating.');
      });
  };

  const handleUpdateStatus = (id, status) => {
    updateBook(id, { status })
      .then(() => {
        setBooks((prev) =>
          prev.map((b) => (b.id === id ? { ...b, status } : b))
        );
      })
      .catch((err) => {
        console.error('Error updating status:', err);
        setErrorMessage('Gagal memperbarui status.');
      });
  };

  return (
    <div className="min-h-screen bg-gradient-to-r from-gray-800 via-gray-900 to-black p-4">
      <Navbar />

      <h1 className="text-3xl font-bold text-center text-white mb-6">Daftar Buku</h1>

      <div className="mb-6 flex justify-center">
        <input
          type="text"
          value={searchQuery}
          onChange={handleSearchChange}
          placeholder="Cari buku berdasarkan judul atau penulis..."
          className="border p-3 rounded-lg w-full sm:w-3/4 lg:w-1/2 text-white bg-gray-800 placeholder-gray-400"
        />
      </div>

      <div className="mb-6 flex flex-col items-center gap-3">
        <input
          type="text"
          placeholder="Judul Buku"
          value={newBook.title}
          onChange={(e) => setNewBook({ ...newBook, title: e.target.value })}
          className="border p-3 rounded-lg w-full sm:w-3/4 lg:w-1/2 text-white bg-gray-800 placeholder-gray-400"
        />
        <input
          type="text"
          placeholder="Penulis Buku"
          value={newBook.author}
          onChange={(e) => setNewBook({ ...newBook, author: e.target.value })}
          className="border p-3 rounded-lg w-full sm:w-3/4 lg:w-1/2 text-white bg-gray-800 placeholder-gray-400"
        />
        <button
          onClick={handleAddBook}
          className="p-3 bg-green-500 text-white rounded-lg w-full sm:w-3/4 lg:w-1/2"
        >
          Tambah Buku
        </button>
      </div>

      {loading && <p className="text-center text-white text-lg mb-4">Loading...</p>}
      {errorMessage && <div className="text-center text-red-500 mb-4">{errorMessage}</div>}

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {books.length > 0 ? (
          books.map((book) => (
            <BookCard
              key={book.id}
              book={book}
              onDelete={handleDelete}
              onUpdateRating={handleUpdateRating}
              onUpdateStatus={handleUpdateStatus}
            />
          ))
        ) : !loading ? (
          <p className="text-gray-500 text-center col-span-full">
            Tidak ada buku yang ditemukan.
          </p>
        ) : null}
      </div>
    </div>
  );
};

export default Home;
