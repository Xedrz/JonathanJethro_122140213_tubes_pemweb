import axios from 'axios';

const API_URL = 'http://localhost:6543';

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
