/** API client for TTS backend. */
const ApiClient = {
    async tts(text, engine = 'edge', speed = 1.0, voice = null) {
        const body = { text, engine, speed };
        if (voice) body.voice = voice;

        const response = await fetch('/api/tts', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'TTS conversion failed');
        }

        return response.json();
    },

    async uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'File upload failed');
        }

        return response.json();
    },

    async checkHealth() {
        try {
            const response = await fetch('/api/health');
            return response.ok;
        } catch {
            return false;
        }
    },

    async shutdown() {
        const response = await fetch('/api/shutdown', { method: 'POST' });
        return response.json();
    },

    getAudioUrl(audioId) {
        return `/api/audio/${audioId}`;
    },
};
