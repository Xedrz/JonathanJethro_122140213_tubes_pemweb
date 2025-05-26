import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { getBookById } from '../services/api';

const BookDetail = () => {
  const { id } = useParams();
  const [book, setBook] = useState(null);

  useEffect(() => {
    const fetchBookDetail = async () => {
      const data = await getBookById(id);
      setBook(data);
    };
    fetchBookDetail();
  }, [id]);

  if (!book) return <div>Loading...</div>;

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <div className="flex items-center mb-6">
        <img src={book.coverImage} alt={book.title} className="w-48 h-72 object-cover rounded-md" />
        <div className="ml-6">
          <h2 className="text-3xl font-semibold">{book.title}</h2>
          <p className="text-lg text-gray-700">{book.author}</p>
          <div className="mt-4">
            <span className="text-yellow-500">★ {book.rating}</span>
            <span className="ml-4 text-gray-600">{book.status}</span>
          </div>
          <p className="mt-6 text-gray-800">{book.description}</p>
        </div>
      </div>
    </div>
  );
};

export default BookDetail;
