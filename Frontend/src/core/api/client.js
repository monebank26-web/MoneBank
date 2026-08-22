const BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const apiClient = {
  get: async (endpoint) => {
    const token = localStorage.getItem('mb_token');
    const res = await fetch(`${BASE_URL}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` }),
      },
    });
    if (!res.ok) {
      let msg;
      try { const b = await res.json(); msg = b.message || b.detail || JSON.stringify(b); } catch { msg = await res.text(); }
      throw new Error(msg);
    }
    return res.json();
  },

  post: async (endpoint, body) => {
    const token = localStorage.getItem('mb_token');
    const res = await fetch(`${BASE_URL}${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` }),
      },
      body: JSON.stringify(body),
    });
    if (!res.ok) {
      let msg;
      try { const b = await res.json(); msg = b.message || b.detail || JSON.stringify(b); } catch { msg = await res.text(); }
      throw new Error(msg);
    }
    return res.json();
  },

  put: async (endpoint, body) => {
    const token = localStorage.getItem('mb_token');
    const res = await fetch(`${BASE_URL}${endpoint}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` }),
      },
      body: JSON.stringify(body),
    });
    if (!res.ok) {
      let msg;
      try { const b = await res.json(); msg = b.message || b.detail || JSON.stringify(b); } catch { msg = await res.text(); }
      throw new Error(msg);
    }
    return res.json();
  },

  delete: async (endpoint) => {
    const token = localStorage.getItem('mb_token');
    const res = await fetch(`${BASE_URL}${endpoint}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` }),
      },
    });
    if (!res.ok) {
      let msg;
      try { const b = await res.json(); msg = b.message || b.detail || JSON.stringify(b); } catch { msg = await res.text(); }
      throw new Error(msg);
    }
    return res.json();
  },
};
