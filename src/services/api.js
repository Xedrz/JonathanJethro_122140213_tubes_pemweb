import axios from 'axios';

export const API_URL = 'http://localhost:6543/api'; 

export const registerUser = async ({ username, email, password }) => {
  try {
    const res = await axios.post(`${API_URL}/register`, {
      username, email, password,
    }, {
      headers: {
        'Content-Type': 'application/json',
      },
      withCredentials: true,
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
      username: identifier,
      password,
    }, {
      headers: {
        'Content-Type': 'application/json',
      },
      withCredentials: true, 
    });
    return { success: true, token: res.data.token };
  } catch (err) {
    console.error('Login error:', err);
    return {
      success: false,
      message: err.response?.data?.error || 'Login failed',
    };
  }
};



// Update getAuthHeaders
// Pastikan headers auth selalu disertakan
export const getAuthHeaders = () => {
  const token = localStorage.getItem('token');
  return {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    withCredentials: true
  };
};

// Update axios instance
const api = axios.create({
  baseURL: 'http://localhost:6543/api',
  withCredentials: true,
});

api.interceptors.response.use(
  response => response,
  error => {
    if (error.code === 'ERR_NETWORK') {
      return Promise.reject({ 
        success: false, 
        message: 'Network error. Please check your connection.' 
      });
    }
    return Promise.reject(error);
  }
);

// Contoh implementasi yang lebih robust untuk getBooks
export const getBooks = async (query = '') => {
  try {
    const params = {};
    if (query) {
      params.query = query;
    }
    const res = await axios.get(`${API_URL}/books`, {
      ...getAuthHeaders(),
      params
    });
    if (res.data && res.data.success) {
      return res.data;
    }
    throw new Error(res.data?.message || 'Failed to load books');
  } catch (err) {
    console.error('Error fetching books:', err);
    throw err;
  }
};

export const getBookById = async (id) => {
  try {
    const res = await axios.get(`${API_URL}/books/${id}`, getAuthHeaders());
    if (res.data && res.data.book) {
      return res.data;
    }
    throw new Error('Book data not found in response');
  } catch (err) {
    console.error('Error fetching book by id:', err);
    throw new Error(err.response?.data?.error || 'Failed to fetch book details');
  }
};

export const addBook = async (bookData) => {
  try {
    const headers = {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    };

    // Jika ada file cover, gunakan FormData dan content-type multipart
    let data = bookData;
    if (bookData instanceof FormData) {
      // Tidak perlu set Content-Type secara manual untuk FormData
    } else {
      headers['Content-Type'] = 'application/json';
    }

    const res = await axios.post(`${API_URL}/books/add`, data, {
      headers,
      withCredentials: true
    });
    return { success: true, book: res.data.book };
  } catch (err) {
    console.error('Error adding book:', err);
    return {
      success: false,
      message: err.response?.data?.error || 'Failed to add book',
    };
  }
};


export const updateBook = async (id, bookData) => {
  try {
    const response = await axios.put(`${API_URL}/books/${id}`, bookData, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
        'Content-Type': 'application/json'
      },
      withCredentials: true
    });
    return response.data;
  } catch (error) {
    console.error('API Error:', error.response?.data || error.message);
    throw error;
  }
};

export const uploadBookCover = async (bookId, file) => {
  try {
    const formData = new FormData();
    formData.append('file', file);

    const response = await axios.post(`${API_URL}/books/${bookId}/cover`, formData, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
        'Content-Type': 'multipart/form-data',
      },
      withCredentials: true
    });
    return response.data;
  } catch (error) {
    console.error('Error uploading cover:', error);
    throw error;
  }
};

export const deleteBook = async (bookId) => {
  try {
    const response = await axios.delete(`${API_URL}/books/${bookId}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
        'Content-Type': 'application/json'
      },
      withCredentials: true
      
    });
    return response.data;
  } catch (error) {
    console.error('API Error:', error.response?.data || error.message);
    throw error;
  }
};

