const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const predictUrl = async (url) => {
  try {
    const response = await fetch(`${API_BASE_URL}/predict`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url }),
    });

    if (!response.ok) {
      throw new Error(`Server returned ${response.status}: Temporary failure or invalid request.`);
    }

    return await response.json();
  } catch (err) {
    throw new Error(err.message || 'Network error occurred while reaching the server.');
  }
};
