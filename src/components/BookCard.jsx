import React, { useState } from 'react';

const BookCard = ({ book, onDelete, onUpdate }) => {
  const [editMode, setEditMode] = useState(false);
  const [editedRating, setEditedRating] = useState(book.rating || 0);
  const [editedStatus, setEditedStatus] = useState(book.status || '');

  const handleSave = () => {
    onUpdate(book.id, {
      ...book,
      rating: editedRating,
      status: editedStatus,
    });
    setEditMode(false);
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-4">
      <img src={book.coverImage || 'https://via.placeholder.com/150'} alt={book.title} className="w-full h-40 object-cover mb-4 rounded" />
      <h2 className="text-lg font-bold">{book.title}</h2>
      <p className="text-gray-700">{book.author}</p>
      <p className="text-sm text-gray-600 mb-2">{book.description}</p>

      {editMode ? (
        <>
          <div className="mb-2">
            <label className="text-sm">Status:</label>
            <input
              type="text"
              value={editedStatus}
              onChange={(e) => setEditedStatus(e.target.value)}
              className="border p-1 rounded w-full"
            />
          </div>
          <div className="mb-2">
            <label className="text-sm">Rating:</label>
            <input
              type="number"
              min="0"
              max="5"
              value={editedRating}
              onChange={(e) => setEditedRating(e.target.value)}
              className="border p-1 rounded w-full"
            />
          </div>
          <button onClick={handleSave} className="bg-blue-500 text-white px-3 py-1 rounded mr-2">Simpan</button>
          <button onClick={() => setEditMode(false)} className="text-gray-600">Batal</button>
        </>
      ) : (
        <>
          <p className="font-semibold">Status: {book.status}</p>
          <p className="flex items-center gap-1">
            Rating: {book.rating} ⭐
          </p>
          <div className="mt-2 flex gap-2">
            <button onClick={() => setEditMode(true)} className="bg-yellow-500 text-white px-3 py-1 rounded">Edit</button>
            <button onClick={() => onDelete(book.id)} className="bg-red-500 text-white px-3 py-1 rounded">Hapus</button>
          </div>
        </>
      )}
    </div>
  );
};

export default BookCard;
