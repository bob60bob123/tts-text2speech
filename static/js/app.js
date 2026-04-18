/** Main application logic. */
(function() {
    // DOM Elements
    const textInput = document.getElementById('text-input');
    const charCount = document.getElementById('char-count');
    const voiceSelect = document.getElementById('voice-select');
    const speedSelect = document.getElementById('speed-select');
    const convertBtn = document.getElementById('convert-btn');
    const playerSection = document.getElementById('player-section');
    const engineUsed = document.getElementById('engine-used');
    const voiceUsed = document.getElementById('voice-used');
    const playBtn = document.getElementById('play-btn');
    const downloadBtn = document.getElementById('download-btn');
    const clearFileBtn = document.getElementById('clear-file');
    const dismissErrorBtn = document.getElementById('dismiss-error');
    const shutdownBtn = document.getElementById('shutdown-btn');
    const serverStatus = document.getElementById('server-status');
    const convertProgressSection = document.getElementById('convert-progress-section');
    const convertProgressFill = document.getElementById('convert-progress-fill');
    const convertProgressText = document.getElementById('convert-progress-text');

    // Current audio ID for download
    let currentAudioId = null;
    let progressInterval = null;

    // Initialize components
    const audioPlayer = new AudioPlayer(document.getElementById('audio-player'));
    const fileHandler = new FileHandler((text, filename) => {
        textInput.value = text;
        charCount.textContent = text.length;
    });

    // Event Listeners
    textInput.addEventListener('input', () => {
        charCount.textContent = textInput.value.length;
    });

    convertBtn.addEventListener('click', handleConvert);
    playBtn.addEventListener('click', handlePlayPause);
    downloadBtn.addEventListener('click', handleDownload);
    clearFileBtn.addEventListener('click', () => {
        fileHandler.clear();
        textInput.value = '';
        charCount.textContent = '0';
    });
    dismissErrorBtn.addEventListener('click', () => fileHandler.clearError());
    shutdownBtn.addEventListener('click', handleShutdown);

    speedSelect.addEventListener('change', () => {
        audioPlayer.setSpeed(speedSelect.value);
    });

    // Handlers
    async function handleConvert() {
        const text = textInput.value.trim();

        if (!text) {
            showError('请输入要转换的文本或上传文件。');
            return;
        }

        if (text.length < 1) {
            showError('文本太短，无法转换。');
            return;
        }

        setLoading(true);
        hideError();
        startConversionProgress();

        try {
            const voice = voiceSelect.value;
            const speed = parseFloat(speedSelect.value);

            const result = await ApiClient.tts(text, 'edge', speed, voice);

            currentAudioId = result.audio_id;
            engineUsed.textContent = `引擎: ${result.engine_used}`;
            voiceUsed.textContent = `音色: ${getVoiceDisplayName(voice)}`;
            playerSection.classList.remove('hidden');
            audioPlayer.setSpeed(speed);

            await audioPlayer.play(result.audio_id);
        } catch (error) {
            showError(error.message);
        } finally {
            setLoading(false);
            stopConversionProgress();
        }
    }

    async function handlePlayPause() {
        if (!currentAudioId) {
            showError('请先转换文本');
            return;
        }
        audioPlayer.toggle(currentAudioId);
    }

    function handleDownload() {
        if (!currentAudioId) {
            showError('请先转换文本');
            return;
        }
        // Trigger download via link
        const link = document.createElement('a');
        link.href = ApiClient.getAudioUrl(currentAudioId);
        link.download = `tts_${currentAudioId}.mp3`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    async function handleShutdown() {
        if (!confirm('确定要关闭服务器吗？')) return;

        try {
            await ApiClient.shutdown();
            serverStatus.textContent = '● 服务已关闭';
            serverStatus.className = 'server-status offline';
            shutdownBtn.disabled = true;
            shutdownBtn.textContent = '已关闭';
        } catch (error) {
            showError('关闭失败: ' + error.message);
        }
    }

    function getVoiceDisplayName(voiceId) {
        const voiceNames = {
            'zh-CN-XiaoxiaoNeural': '晓晓 (女声-年轻)',
            'zh-CN-XiaoyiNeural': '小艺 (女声-童年)',
            'zh-CN-YunxiaNeural': '云夏 (女声-年轻)',
            'zh-CN-YunxiNeural': '云希 (男声-年轻)',
            'zh-CN-YunyangNeural': '云扬 (男声-中年)',
            'zh-CN-YunjianNeural': '云健 (男声-年轻)',
            'en-US-AriaNeural': 'Aria (女声-美式)',
            'en-US-GuyNeural': 'Guy (男声-美式)',
            'en-US-JennyNeural': 'Jenny (女声-美式)',
            'en-GB-SoniaNeural': 'Sonia (女声-英式)',
            'en-GB-RyanNeural': 'Ryan (男声-英式)',
        };
        return voiceNames[voiceId] || voiceId;
    }

    // Conversion Progress Animation
    function startConversionProgress() {
        convertProgressSection.classList.remove('hidden');
        let progress = 0;
        const stages = [15, 30, 50, 70, 85, 95]; // Simulated progress stages

        progressInterval = setInterval(() => {
            if (progress < stages.length) {
                progress++;
                const percent = stages[progress - 1];
                convertProgressFill.style.width = `${percent}%`;
                convertProgressText.textContent = `${percent}%`;
            } else {
                // Keep at 95% until done
                convertProgressFill.style.width = '95%';
                convertProgressText.textContent = '95%';
            }
        }, 300);
    }

    function stopConversionProgress() {
        if (progressInterval) {
            clearInterval(progressInterval);
            progressInterval = null;
        }
        // Complete the progress bar
        convertProgressFill.style.width = '100%';
        convertProgressText.textContent = '100%';
        // Hide after a short delay
        setTimeout(() => {
            convertProgressSection.classList.add('hidden');
            convertProgressFill.style.width = '0%';
            convertProgressText.textContent = '0%';
        }, 500);
    }

    // UI Helpers
    function setLoading(loading) {
        const btnText = convertBtn.querySelector('.btn-text');
        const btnLoading = convertBtn.querySelector('.btn-loading');

        if (loading) {
            btnText.classList.add('hidden');
            btnLoading.classList.remove('hidden');
            convertBtn.disabled = true;
        } else {
            btnText.classList.remove('hidden');
            btnLoading.classList.add('hidden');
            convertBtn.disabled = false;
        }
    }

    function showError(message) {
        const errorDisplay = document.getElementById('error-display');
        const errorMessage = document.getElementById('error-message');
        errorMessage.textContent = message;
        errorDisplay.classList.remove('hidden');
    }

    function hideError() {
        document.getElementById('error-display').classList.add('hidden');
    }
})();
