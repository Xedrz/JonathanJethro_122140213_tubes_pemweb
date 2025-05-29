import React from 'react';
import { useNavigate } from 'react-router-dom';
import { addBook } from '../services/api';
import BookForm from '../components/BookForm';

const AddBook = () => {
  const navigate = useNavigate();

  const handleSubmit = async (bookData) => {
    try {
      await addBook(bookData);
      navigate('/');
    } catch (error) {
      alert(error.message || 'Failed to add book');
    }
  };

  return (
    <div>
      <h2>Add New Book</h2>
      <BookForm onSubmit={handleSubmit} />
    </div>
  );
};

export default AddBook;