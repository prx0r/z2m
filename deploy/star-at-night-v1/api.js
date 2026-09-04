// Star at Night API Client
const API_BASE = 'http://localhost:3000';

const api = {
  // Upload photo
  async uploadPhoto(file) {
    const formData = new FormData();
    formData.append('photo', file);
    
    const res = await fetch(`${API_BASE}/api/photos`, {
      method: 'POST',
      body: formData
    });
    return res.json();
  },

  // Create session
  async createSession(data) {
    const res = await fetch(`${API_BASE}/api/sessions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return res.json();
  },

  // Generate products
  async generateProducts(sessionId) {
    const res = await fetch(`${API_BASE}/api/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ sessionId })
    });
    return res.json();
  },

  // Get session
  async getSession(id) {
    const res = await fetch(`${API_BASE}/api/sessions/${id}`);
    return res.json();
  },

  // Get products
  async getProducts(sessionId) {
    const res = await fetch(`${API_BASE}/api/sessions/${sessionId}/products`);
    return res.json();
  }
};

window.StarAtNightAPI = api;
