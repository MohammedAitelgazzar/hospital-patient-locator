import axios from 'axios';

// Base URL of your backend API
const apiUrl = 'http://localhost:8082/api';

// Fetch user details by username
export const getUserDetails = async (username) => {
  if (!username) {
    throw new Error('Username is not available');
  }
  const response = await axios.get(`${apiUrl}/user/${username}`);
  return response.data;
};

// Fetch all localisations
export const getLocalisations = async () => {
    const response = await axios.get(`${apiUrl}/localisations/last`);
    console.log("Last localisation:", response.data);
    return response.data; // Expecting a single object
  };
