import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Document API
export const documentAPI = {
    upload: async (file) => {
        const formData = new FormData();
        formData.append('file', file);

        const response = await api.post('/api/documents/upload', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    },

    list: async () => {
        const response = await api.get('/api/documents/');
        return response.data;
    },

    delete: async (filename) => {
        const response = await api.delete(`/api/documents/${filename}`);
        return response.data;
    },

    getInfo: async () => {
        const response = await api.get('/api/documents/info');
        return response.data;
    },
};

// Chat API
export const chatAPI = {
    sendMessage: async (query, chatHistory = [], topK = 5, developerMode = false) => {
        const response = await api.post('/api/chat/', {
            query,
            chat_history: chatHistory,
            top_k: topK,
        }, {
            params: {
                developer_mode: developerMode,
            },
        });
        return response.data;
    },

    healthCheck: async () => {
        const response = await api.get('/api/chat/health');
        return response.data;
    },
};

export default api;
