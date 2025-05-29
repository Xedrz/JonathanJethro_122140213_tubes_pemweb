// src/pages/Home.jsx
import React, { useState, useEffect, useCallback } from 'react';
import { getBooks, addBook, deleteBook, updateBook } from '../services/api';
import BookCard from '../components/BookCard';
import Navbar from '../components/Navbar';
import debounce from 'lodash.debounce';
import BookForm from '../components/BookForm';

const Home = () => {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [newBook, setNewBook] = useState({ title: '', author: '', rating: 0, status: '' });

  const fetchBooks = useCallback(async (query = '') => {
    setLoading(true);
    setErrorMessage('');
    try {
      const response = await getBooks(query);
      if (response && response.success) {
        setBooks(response.books || []);
      } else {
        setErrorMessage(response?.message || 'Failed to load books');
      }
    } catch (err) {
      setErrorMessage(err.message || 'Network error occurred');
      console.error('Fetch error:', err);
    } finally {
      setLoading(false);
    }
  }, []);

    // Debounced search
    const debouncedSearch = useCallback(
      debounce((query) => fetchBooks(query), 500),
      []
    );

    useEffect(() => {
      fetchBooks();
    }, [fetchBooks]);

  const handleSearchChange = (e) => {
    const query = e.target.value;
    setSearchQuery(query);
    debouncedSearch(query);
  };
const handleDelete = async (bookId) => {
  if (!bookId) {
    console.error('Invalid book ID');
    setErrorMessage('Invalid book ID');
    return;
  }

  try {
    await deleteBook(bookId);
    setBooks(books.filter((book) => book.id !== bookId));
  } catch (err) {
    console.error('Error deleting book:', err);
    setErrorMessage('Gagal menghapus buku');
  }
};
const handleAddBook = async () => {
  try {
    setLoading(true);
    setErrorMessage('');
    
    const bookData = {
      title: newBook.title,
      author: newBook.author,
      description: '', 
      status: 'UNREAD',
      rating: 0
    };

    const res = await addBook(bookData);
    if (res.success) {
      setBooks([...books, res.book]);
      setNewBook({ title: '', author: '', rating: 0, status: '' });
      setErrorMessage('');
    } else {
      setErrorMessage(res.message || 'Gagal menambahkan buku.');
    }
  } catch (err) {
    console.error('Error adding book:', err);
    setErrorMessage(err.message || 'Terjadi kesalahan saat menambahkan buku.');
  } finally {
    setLoading(false);
  }
};


const handleUpdateBook = async (bookId, updatedData) => {
  if (!bookId) {
    console.error('Invalid book ID');
    setErrorMessage('Invalid book ID');
    return;
  }

  try {
    console.log('Updating book:', bookId, 'with data:', updatedData);
    const res = await updateBook(bookId, updatedData);
    if (res.success) {
      setBooks(books.map(book => 
        book.id === bookId ? { ...book, ...res.book } : book
      ));
    } else {
      console.error('Update failed:', res.message);
      setErrorMessage(res.message || 'Failed to update book');
    }
  } catch (err) {
    console.error('Update error details:', err.response?.data || err.message);
    setErrorMessage(err.response?.data?.message || 'Failed to update book');
  }
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
  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 px-4 sm:px-6 lg:px-8">
    {books.length > 0 ? (
      books
        .sort((a, b) => a.title.localeCompare(b.title))
        .map((book) => (
          <BookCard
            key={book.id}
            book={book}
            onDelete={handleDelete}
            onUpdate={handleUpdateBook}
          />
        ))
          ) : !loading ? (
            <div className="col-span-full text-center py-10">
              <p className="text-gray-400 text-lg">Buku belum ditambahkan.</p>
              <button 
                onClick={() => fetchBooks()} 
                className="mt-4 px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition-colors"
              >
                Muat Ulang
              </button>
            </div>
          ) : null}
      </div>
    </div>
  );
};

export default Home;
