const API_BASE = '/api';

class API {
    static async request(endpoint, options = {}) {
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers,
            },
            ...options,
        };

        try {
            const response = await fetch(`${API_BASE}${endpoint}`, config);
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || `API error (${response.status})`);
            }
            return await response.json();
        } catch (err) {
            console.error(`API Error on ${endpoint}:`, err);
            throw err;
        }
    }

    static getProfile() {
        return this.request('/profile');
    }

    static updateProfile(data) {
        return this.request('/profile', {
            method: 'PUT',
            body: JSON.stringify(data),
        });
    }

    static getActivities() {
        return this.request('/activity');
    }

    static addActivity(data) {
        return this.request('/activity', {
            method: 'POST',
            body: JSON.stringify(data),
        });
    }

    static getMedications() {
        return this.request('/medications');
    }

    static addMedication(data) {
        return this.request('/medications', {
            method: 'POST',
            body: JSON.stringify(data),
        });
    }

    static toggleMedication(id) {
        return this.request(`/medications/${id}/toggle`, {
            method: 'PUT',
        });
    }

    static getAppointments() {
        return this.request('/appointments');
    }

    static addAppointment(data) {
        return this.request('/appointments', {
            method: 'POST',
            body: JSON.stringify(data),
        });
    }

    static getRecommendation() {
        return this.request('/recommendations');
    }

    static screenRisk(data) {
        return this.request('/risk/screen', {
            method: 'POST',
            body: JSON.stringify(data),
        });
    }

    static sendAIChat(question) {
        return this.request('/ai/chat', {
            method: 'POST',
            body: JSON.stringify({ question }),
        });
    }
}
