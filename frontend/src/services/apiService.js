import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export const createScan = async (scanData) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/scan`, scanData);
    return response.data;
  } catch (error) {
    console.error('Error creating scan:', error);
    throw error;
  }
};

export const getScanResults = async (scanId) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/scan/${scanId}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching scan results:', error);
    throw error;
  }
};
