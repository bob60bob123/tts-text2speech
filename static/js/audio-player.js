/** Audio player controller with draggable progress bar. */
class AudioPlayer {
    constructor(audioElement) {
        this.audio = audioElement;
        this.isPlaying = false;
        this.currentAudioId = null;
        this.isDragging = false;
        this._setupEventListeners();
        this._setupProgressDrag();
    }

    _setupEventListeners() {
        this.audio.addEventListener('ended', () => {
            this.isPlaying = false;
            this._updatePlayButton(false);
            this._resetProgress();
        });

        this.audio.addEventListener('timeupdate', () => {
            if (!this.isDragging) {
                this._updateProgress();
            }
        });

        this.audio.addEventListener('loadedmetadata', () => {
            this._updateTimeDisplay();
        });

        this.audio.addEventListener('play', () => {
            this.isPlaying = true;
            this._updatePlayButton(true);
        });

        this.audio.addEventListener('pause', () => {
            this.isPlaying = false;
            this._updatePlayButton(false);
        });
    }

    _setupProgressDrag() {
        const progressTrack = document.getElementById('audio-progress-track');
        const progressHandle = document.getElementById('audio-progress-handle');

        // Helper to calculate percent from clientX
        const getPositionPercent = (clientX) => {
            const rect = progressTrack.getBoundingClientRect();
            const percent = (clientX - rect.left) / rect.width;
            return Math.max(0, Math.min(1, percent));
        };

        // Helper to seek to a position
        const seekToPosition = (clientX) => {
            const percent = getPositionPercent(clientX);
            if (this.audio.duration) {
                this.audio.currentTime = percent * this.audio.duration;
                this._updateProgress();
            }
        };

        // Pointer down handler - starts drag
        const handlePointerDown = (e) => {
            e.preventDefault();
            const clientX = e.clientX || (e.touches && e.touches[0].clientX);
            this.isDragging = true;
            seekToPosition(clientX);
            this._lastDragX = clientX;
        };

        // Pointer move handler - updates during drag
        const handlePointerMove = (e) => {
            if (!this.isDragging) return;
            const clientX = e.clientX || (e.touches && e.touches[0].clientX);
            seekToPosition(clientX);
            this._lastDragX = clientX;
        };

        // Pointer up handler - ends drag
        const handlePointerUp = () => {
            this.isDragging = false;
            this._lastDragX = null;
        };

        // Attach listeners to the track (larger target)
        progressTrack.addEventListener('mousedown', handlePointerDown);
        progressTrack.addEventListener('touchstart', handlePointerDown, { passive: false });

        // Also attach to handle for easier grabbing
        progressHandle.addEventListener('mousedown', handlePointerDown);
        progressHandle.addEventListener('touchstart', handlePointerDown, { passive: false });

        // Document-level listeners for drag tracking
        document.addEventListener('mousemove', handlePointerMove);
        document.addEventListener('mouseup', handlePointerUp);
        document.addEventListener('touchmove', handlePointerMove, { passive: false });
        document.addEventListener('touchend', handlePointerUp);
        document.addEventListener('mouseleave', handlePointerUp);

        // Click on track (not drag) should also seek
        progressTrack.addEventListener('click', (e) => {
            if (this.isDragging) return;
            seekToPosition(e.clientX);
        });
    }

    async play(audioId) {
        if (this.currentAudioId !== audioId) {
            this.audio.src = ApiClient.getAudioUrl(audioId);
            this.currentAudioId = audioId;
            await this.audio.load();
        }
        await this.audio.play();
    }

    pause() {
        this.audio.pause();
    }

    toggle(audioId) {
        if (this.currentAudioId === audioId && this.isPlaying) {
            this.pause();
        } else {
            this.play(audioId);
        }
    }

    setSpeed(rate) {
        this.audio.playbackRate = parseFloat(rate);
    }

    seek(percent) {
        if (this.audio.duration) {
            this.audio.currentTime = percent * this.audio.duration;
            this._updateProgress();
        }
    }

    _updatePlayButton(playing) {
        const playIcon = document.querySelector('.play-icon');
        const pauseIcon = document.querySelector('.pause-icon');

        if (playing) {
            playIcon.classList.add('hidden');
            pauseIcon.classList.remove('hidden');
        } else {
            playIcon.classList.remove('hidden');
            pauseIcon.classList.add('hidden');
        }
    }

    _updateProgress() {
        const progressFill = document.getElementById('audio-progress-fill');
        const progressHandle = document.getElementById('audio-progress-handle');
        if (this.audio.duration) {
            const percent = (this.audio.currentTime / this.audio.duration) * 100;
            progressFill.style.width = `${percent}%`;
            progressHandle.style.left = `${percent}%`;
        }
        this._updateTimeDisplay();
    }

    _resetProgress() {
        const progressFill = document.getElementById('audio-progress-fill');
        const progressHandle = document.getElementById('audio-progress-handle');
        progressFill.style.width = '0%';
        progressHandle.style.left = '0%';
    }

    _updateTimeDisplay() {
        const timeDisplay = document.getElementById('time-display');
        const current = this._formatTime(this.audio.currentTime);
        const total = this._formatTime(this.audio.duration || 0);
        timeDisplay.textContent = `${current} / ${total}`;
    }

    _formatTime(seconds) {
        if (isNaN(seconds)) return '0:00';
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    }
}
