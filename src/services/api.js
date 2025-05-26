import axios from 'axios';

const API_URL = 'http://localhost:6543/api';

export const registerUser = async ({ username, email, password }) => {
  try {
    const res = await axios.post(`${API_URL}/register`, {
      username, email, password,
    });
    return { success: true, message: res.data.message };
  } catch (err) {
    return {
      success: false,
      message: err.response?.data?.error || 'Registration failed',
    };
  }
};

export const loginUser = async ({ identifier, password }) => {
  try {
    const res = await axios.post(`${API_URL}/login`, {
      username: identifier, // bisa username atau email
      password,
    });
    return { success: true, token: res.data.token };
  } catch (err) {
    return {
      success: false,
      message: err.response?.data?.error || 'Login failed',
    };
  }
};


// Mengambil daftar buku berdasarkan query pencarian
export const getBooks = async (searchQuery = '') => {
  try {
    const response = await axios.get(`${API_URL}/books`, {
      params: {
        query: searchQuery,  // Menambahkan query parameter untuk pencarian
      },
    });
    return {
      success: true,
      books: response.data,  // Menyimpan data buku yang didapat
    };
  } catch (error) {
    console.error('Error fetching books:', error);
    return {
      success: false,
      message: 'Gagal mengambil data buku',
    };
  }
};

export const getBookById = async (id) => {
  try {
    const response = await axios.get(`/api/books/${id}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching book by id:', error);
    throw error;
  }
};


export const addBook = async (bookData) => {
  try {
    const response = await fetch('http://localhost:6543/api/books', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(bookData),
    });

    if (!response.ok) {
      throw new Error('Failed to add book');
    }

    return await response.json();
  } catch (error) {
    console.error('Error adding book:', error);
    throw error;
  }
};

// Fungsi untuk memperbarui buku
export const updateBook = async (bookId, bookData) => {
  try {
    const response = await fetch(`http://localhost:6543/api/books/${bookId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(bookData),
    });

    if (!response.ok) {
      throw new Error('Failed to update book');
    }

    return await response.json();
  } catch (error) {
    console.error('Error updating book:', error);
    throw error;
  }
};

export const deleteBook = (bookId) => {
  return axios
    .delete(`${API_URL}/books/${bookId}`)
    .then((response) => response.data)
    .catch((error) => {
      throw error;
    });
};