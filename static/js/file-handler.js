/** File upload and handling. */
class FileHandler {
    constructor(onTextExtracted) {
        this.onTextExtracted = onTextExtracted;
        this.currentFile = null;
        this._setupDropZone();
        this._setupFileInput();
    }

    _setupDropZone() {
        const dropZone = document.getElementById('drop-zone');

        dropZone.addEventListener('click', () => {
            document.getElementById('file-input').click();
        });

        dropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropZone.classList.add('drag-over');
        });

        dropZone.addEventListener('dragleave', () => {
            dropZone.classList.remove('drag-over');
        });

        dropZone.addEventListener('drop', async (e) => {
            e.preventDefault();
            dropZone.classList.remove('drag-over');

            const file = e.dataTransfer.files[0];
            if (file) await this.processFile(file);
        });
    }

    _setupFileInput() {
        const fileInput = document.getElementById('file-input');
        fileInput.addEventListener('change', async () => {
            const file = fileInput.files[0];
            if (file) await this.processFile(file);
        });
    }

    async processFile(file) {
        const validTypes = ['.txt', '.pdf', '.docx', '.md'];
        const ext = '.' + file.name.split('.').pop().toLowerCase();

        if (!validTypes.includes(ext)) {
            this._showError(`不支持的文件类型: ${ext}。请上传 TXT, PDF, DOCX 或 MD 文件。`);
            return;
        }

        if (file.size > 10 * 1024 * 1024) {
            this._showError('文件太大，请上传小于 10MB 的文件。');
            return;
        }

        this.currentFile = file;
        this._showFileInfo(file);

        try {
            const result = await ApiClient.uploadFile(file);

            if (result.supported) {
                this.onTextExtracted(result.text, result.filename);
            } else {
                this._showError(`不支持的文件类型: ${file.name}`);
            }
        } catch (error) {
            this._showError(error.message);
        }
    }

    _showFileInfo(file) {
        const fileInfo = document.getElementById('file-info');
        const fileName = document.getElementById('file-name');
        const fileSize = document.getElementById('file-size');

        fileName.textContent = file.name;
        fileSize.textContent = this._formatFileSize(file.size);
        fileInfo.classList.remove('hidden');

        document.getElementById('drop-zone').classList.add('hidden');
    }

    _hideFileInfo() {
        const fileInfo = document.getElementById('file-info');
        fileInfo.classList.add('hidden');
        document.getElementById('drop-zone').classList.remove('hidden');
        this.currentFile = null;
        document.getElementById('file-input').value = '';
    }

    _formatFileSize(bytes) {
        if (bytes < 1024) return bytes + ' B';
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
        return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
    }

    _showError(message) {
        const errorDisplay = document.getElementById('error-display');
        const errorMessage = document.getElementById('error-message');
        errorMessage.textContent = message;
        errorDisplay.classList.remove('hidden');
    }

    clearError() {
        document.getElementById('error-display').classList.add('hidden');
    }

    clear() {
        this._hideFileInfo();
        this.clearError();
    }
}
