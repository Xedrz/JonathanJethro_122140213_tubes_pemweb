import React, { useState } from 'react';

const BookForm = ({ initialValues = {}, onSubmit }) => {
  const [formData, setFormData] = React.useState({
    title: '',
    author: '',
    published_date: '',
    cover_url: '',
    description: '',
    pages: '',
    status: 'UNREAD',
    rating: 0,
    notes: '',
    ...initialValues
  });

  const [coverPreview, setCoverPreview] = useState(initialValues.cover_url || '');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setCoverPreview(reader.result);
      };
      reader.readAsDataURL(file);
      setFormData(prev => ({ ...prev, cover_file: file }));
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    const submitData = new FormData();
    
    // Tambahkan semua field ke FormData
    Object.keys(formData).forEach(key => {
      if (key === 'cover_file' && formData[key]) {
        submitData.append('file', formData[key]);
      } else {
        submitData.append(key, formData[key]);
      }
    });
    
    onSubmit(submitData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4" encType="multipart/form-data">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="col-span-full">
          <label className="block text-sm font-medium text-gray-700">Cover Buku</label>
          <div className="mt-1 flex items-center">
            {coverPreview ? (
              <img 
                src={coverPreview} 
                alt="Preview Cover" 
                className="h-32 w-24 object-cover rounded-md mr-4"
              />
            ) : (
              <div className="h-32 w-24 bg-gray-200 rounded-md flex items-center justify-center text-gray-500 mr-4">
                No Cover
              </div>
            )}
            <input
              type="file"
              name="cover_file"
              onChange={handleFileChange}
              accept="image/*"
              className="p-2 border rounded-md"
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Judul*</label>
          <input
            name="title"
            value={formData.title}
            onChange={handleChange}
            required
            className="mt-1 p-2 w-full border rounded-md"
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700">Penulis*</label>
          <input
            name="author"
            value={formData.author}
            onChange={handleChange}
            required
            className="mt-1 p-2 w-full border rounded-md"
          />
        </div>

        <div className="col-span-full">
          <label className="block text-sm font-medium text-gray-700">Deskripsi</label>
          <textarea
            name="description"
            value={formData.description}
            onChange={handleChange}
            rows="4"
            className="mt-1 p-2 w-full border rounded-md"
            placeholder="Masukkan deskripsi buku..."
          />
        </div>
      </div>
      
      <button 
        type="submit" 
        className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition-colors"
      >
        Simpan
      </button>
    </form>
  );
};

export default BookForm;