import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getBookById, uploadBookCover } from '../services/api';
import Navbar from '../components/Navbar';

const BookDetail = () => {
  const { id } = useParams();
  const [book, setBook] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [coverPreview, setCoverPreview] = useState('');

  useEffect(() => {
    const fetchBook = async () => {
      try {
        const response = await getBookById(id);
        if (response && response.book) {
          setBook(response.book);
          setCoverPreview(response.book.cover_url || '');
        } else {
          setError('Buku tidak ditemukan');
        }
      } catch (err) {
        setError(err.message || 'Gagal memuat detail buku');
      } finally {
        setLoading(false);
      }
    };

    fetchBook();
  }, [id]);

  const handleCoverUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    try {
      // Preview gambar
      const reader = new FileReader();
      reader.onloadend = () => {
        setCoverPreview(reader.result);
      };
      reader.readAsDataURL(file);

      // Upload ke server
      const response = await uploadBookCover(id, file);
      if (response.success) {
        setBook(prev => ({ ...prev, cover_url: response.cover_url }));
      }
    } catch (err) {
      setError('Gagal mengupload cover');
    }
  };

  if (loading) return <div className="text-center py-10">Memuat...</div>;
  if (error) return <div className="text-center text-red-500 py-10">{error}</div>;
  if (!book) return <div className="text-center py-10">Buku tidak ditemukan</div>;

  return (
    <div className="min-h-screen bg-gradient-to-r from-gray-800 via-gray-900 to-black p-4">
      <Navbar />
      
      <div className="container mx-auto px-4 py-8 max-w-6xl">
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden">
          <div className="md:flex">
            {/* Cover Section */}
            <div className="md:w-1/3 p-6 flex flex-col items-center">
              <div className="relative group">
                <img
                  src={coverPreview ? `http://localhost:6543${coverPreview}` : 'https://via.placeholder.com/300x450?text=No+Cover'}
                  alt={book.title}
                  className="w-64 h-96 object-cover rounded-lg shadow-md"
                />
                <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-20 transition-all duration-300 flex items-center justify-center">
                  <label className="cursor-pointer opacity-0 group-hover:opacity-100 transition-opacity">
                    <span className="bg-gray-100 text-gray-800 px-3 py-1 rounded-md text-sm font-medium">
                      Ganti Cover
                    </span>
                    <input
                      type="file"
                      accept="image/*"
                      onChange={handleCoverUpload}
                      className="hidden"
                    />
                  </label>
                </div>
              </div>
              
              <div className="mt-4 text-center">
                <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
                  book.status === 'UNREAD' ? 'bg-gray-100 text-gray-800' :
                  book.status === 'READING' ? 'bg-yellow-100 text-yellow-800' :
                  'bg-green-100 text-green-800'
                }`}>
                  {book.status === 'UNREAD' && 'Belum Dibaca'}
                  {book.status === 'READING' && 'Sedang Dibaca'}
                  {book.status === 'FINISHED' && 'Selesai Dibaca'}
                </span>
                
                <div className="mt-2 flex justify-center items-center">
                  <div className="flex">
                    {[...Array(5)].map((_, i) => (
                      <span 
                        key={i} 
                        className={`text-2xl ${i < book.rating ? 'text-yellow-500' : 'text-gray-300'}`}
                      >
                        ★
                      </span>
                    ))}
                  </div>
                  <span className="ml-2 text-gray-600">({book.rating}/5)</span>
                </div>
              </div>
            </div>
            
            {/* Detail Section */}
            <div className="md:w-2/3 p-6">
              <h1 className="text-3xl font-bold text-gray-800 mb-2">{book.title}</h1>
              <p className="text-xl text-gray-600 mb-6">Oleh: {book.author}</p>
              
              <div className="mb-6">
                <h2 className="text-xl font-semibold text-gray-800 mb-2">Deskripsi</h2>
                <p className="text-gray-700 whitespace-pre-line">
                  {book.description || 'Tidak ada deskripsi.'}
                </p>
              </div>
              
              <div className="flex space-x-4 mt-8">
                <Link 
                  to="/home" 
                  className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition-colors"
                >
                  Kembali
                </Link>
                {/* Tambahkan tombol aksi lainnya jika diperlukan */}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BookDetail;