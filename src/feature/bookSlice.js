// src/features/books/bookSlice.js

import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

// Thunk untuk fetch buku
export const fetchBooks = createAsyncThunk('books/fetchBooks', async (searchQuery) => {
  const response = await fetch(`/api/books?search=${searchQuery}`);
  const data = await response.json();
  return data;
});

// Thunk untuk mengupdate status
export const updateBookStatus = createAsyncThunk('books/updateBookStatus', async ({ id, status }) => {
  const response = await fetch(`/api/books/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ status }),
  });
  return response.json();
});

// Thunk untuk mengupdate rating
export const updateBookRating = createAsyncThunk('books/updateBookRating', async ({ id, rating }) => {
  const response = await fetch(`/api/books/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ rating }),
  });
  return response.json();
});

// Thunk untuk menghapus buku
export const deleteBook = createAsyncThunk('books/deleteBook', async (id) => {
  await fetch(`/api/books/${id}`, {
    method: 'DELETE',
  });
  return id;
});

const booksSlice = createSlice({
  name: 'books',
  initialState: {
    books: [],
    loading: false,
    error: null,
  },
  reducers: {
    setBooks: (state, action) => {
      state.books = action.payload;
    },
    setError: (state, action) => {
      state.error = action.payload;
    },
    setLoading: (state, action) => {
      state.loading = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchBooks.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchBooks.fulfilled, (state, action) => {
        state.loading = false;
        state.books = action.payload;
      })
      .addCase(fetchBooks.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      })
      .addCase(updateBookStatus.fulfilled, (state, action) => {
        const updatedBook = action.payload;
        const index = state.books.findIndex((book) => book.id === updatedBook.id);
        if (index !== -1) {
          state.books[index] = updatedBook;
        }
      })
      .addCase(updateBookRating.fulfilled, (state, action) => {
        const updatedBook = action.payload;
        const index = state.books.findIndex((book) => book.id === updatedBook.id);
        if (index !== -1) {
          state.books[index] = updatedBook;
        }
      })
      .addCase(deleteBook.fulfilled, (state, action) => {
        state.books = state.books.filter((book) => book.id !== action.payload);
      });
  },
});

export const { setBooks, setError, setLoading } = booksSlice.actions;

export default booksSlice.reducer;
