import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import BookForm from '../components/BookForm';
import { getBookById, updateBook } from '../services/api';

const EditBook = () => {
  const { bookId } = useParams();
  const navigate = useNavigate();
  const [bookData, setBookData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchBook = async () => {
      try {
        const res = await getBookById(bookId);
        setBookData(res.book);
      } catch (err) {
        console.error('Gagal mengambil data buku:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchBook();
  }, [bookId]);

  const handleUpdate = async (form) => {
    try {
      const result = await updateBook(bookId, form);
      if (result.success) {
        alert('Buku berhasil diperbarui');
        navigate('/books');
      } else {
        alert(result.message || 'Gagal memperbarui buku');
      }
    } catch (err) {
      console.error('Error updating book:', err);
      alert('Terjadi kesalahan saat memperbarui buku');
    }
  };

  if (loading) return <div>Loading...</div>;
  if (!bookData) return <div>Buku tidak ditemukan</div>;

  return (
    <div>
      <h2 className="text-xl font-bold">Edit Buku</h2>
      <BookForm onSubmit={handleUpdate} initialData={bookData} />
    </div>
  );
};

export default EditBook;