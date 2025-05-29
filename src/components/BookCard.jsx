import React, { useState } from 'react';
import { Link } from 'react-router-dom';

const BookCard = ({ book, onDelete, onUpdate }) => {
  const [editMode, setEditMode] = useState(false);
  const [editedRating, setEditedRating] = useState(book.rating || 0);
  const [editedStatus, setEditedStatus] = useState(book.status || '');
  const [editedDescription, setEditedDescription] = useState(book.description || '');
  const [error, setError] = useState('');

  const handleSave = () => {
    if (!book.id) {
      setError('Invalid book ID');
      return;
    }

    const ratingNumber = parseFloat(editedRating);
    
    if (isNaN(ratingNumber)) {
      setError('Rating must be a number');
      return;
    }

    const upperStatus = editedStatus.toUpperCase();
    if (!['UNREAD', 'READING', 'FINISHED'].includes(upperStatus)) {
      setError('Status must be UNREAD, READING, or FINISHED');
      return;
    }

    onUpdate(book.id, {
      status: upperStatus,
      rating: ratingNumber,
      description: editedDescription 
    });
    
    setEditMode(false);
    setError('');
  };

  const getStatusColor = (status) => {
    switch(status) {
      case 'READING': return 'bg-yellow-100 text-yellow-800';
      case 'FINISHED': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg overflow-hidden transition-transform hover:scale-105 hover:shadow-xl">
      {/* Cover dengan efek hover */}
      <Link to={`/books/${book.id}`} className="block relative group">
        <img
          src={book.cover_url ? `http://localhost:6543${book.cover_url}` : 'https://via.placeholder.com/300x450?text=No+Cover'}
          alt={book.title}
          className="w-full h-64 object-cover transition-opacity group-hover:opacity-90"
        />
        <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-20 transition-all duration-300 flex items-center justify-center">
          <span className="text-white opacity-0 group-hover:opacity-100 transition-opacity font-bold text-lg">
            Lihat Detail
          </span>
        </div>
      </Link>

      <div className="p-4">
        <Link to={`/books/${book.id}`} className="hover:underline">
          <h2 className="text-xl font-bold text-gray-800 mb-1 line-clamp-1">{book.title}</h2>
        </Link>
        <p className="text-gray-600 mb-2 line-clamp-1">{book.author}</p>
        
        {/* Deskripsi singkat */}
        {book.description && (
          <p className="text-gray-700 text-sm mb-3 line-clamp-2">
            {book.description}
          </p>
        )}
        {editMode && (
    <div className="col-span-full">
      <label className="block text-sm font-medium text-gray-700 mb-1">Deskripsi</label>
      <textarea
        value={editedDescription}
        onChange={(e) => setEditedDescription(e.target.value)}
        rows="3"
        className="w-full p-2 border rounded-md"
      />
    </div>
  )}
        {editMode ? (
          <div className="space-y-3">
            {error && <p className="text-red-500 text-sm">{error}</p>}
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
              <select
                value={editedStatus}
                onChange={(e) => setEditedStatus(e.target.value)}
                className="w-full p-2 border rounded-md"
              >
                <option value="UNREAD">Belum Dibaca</option>
                <option value="READING">Sedang Dibaca</option>
                <option value="FINISHED">Selesai Dibaca</option>
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Rating</label>
              <select
                value={editedRating}
                onChange={(e) => setEditedRating(e.target.value)}
                className="w-full p-2 border rounded-md"
              >
                {[0, 1, 2, 3, 4, 5].map(num => (
                  <option key={num} value={num}>{num} ⭐</option>
                ))}
              </select>
            </div>
            
            <div className="flex space-x-2 pt-2">
              <button 
                onClick={handleSave} 
                className="flex-1 bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 transition-colors"
              >
                Simpan
              </button>
              <button 
                onClick={() => setEditMode(false)} 
                className="flex-1 bg-gray-200 text-gray-800 py-2 rounded-md hover:bg-gray-300 transition-colors"
              >
                Batal
              </button>
            </div>
          </div>
        ) : (
          <div className="space-y-2">
            <div className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(book.status)}`}>
              {book.status === 'UNREAD' && 'Belum Dibaca'}
              {book.status === 'READING' && 'Sedang Dibaca'}
              {book.status === 'FINISHED' && 'Selesai Dibaca'}
            </div>
            
            <div className="flex items-center">
              <span className="text-gray-700 mr-1">Rating:</span>
              <div className="flex">
                {[...Array(5)].map((_, i) => (
                  <span key={i} className={`text-lg ${i < book.rating ? 'text-yellow-500' : 'text-gray-300'}`}>★</span>
                ))}
              </div>
              <span className="ml-1 text-gray-600">({book.rating})</span>
            </div>
            
            <div className="flex space-x-2 pt-2">
              <button 
                onClick={() => setEditMode(true)} 
                className="flex-1 bg-yellow-500 text-white py-1.5 rounded-md hover:bg-yellow-600 transition-colors text-sm"
              >
                Edit
              </button>
              <button 
                onClick={() => onDelete(book.id)} 
                className="flex-1 bg-red-500 text-white py-1.5 rounded-md hover:bg-red-600 transition-colors text-sm"
              >
                Hapus
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default BookCard;