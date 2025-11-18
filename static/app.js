class KuczynskiChat {
    constructor() {
        this.messageContainer = document.getElementById('messages');
        this.userInput = document.getElementById('user-input');
        this.sendButton = document.getElementById('submit-btn');
        this.uploadButton = document.getElementById('upload-btn');
        this.fileInput = document.getElementById('file-input');
        this.userStatus = document.getElementById('user-status');
        this.providerSelect = document.getElementById('provider-select');
        this.modelSelect = document.getElementById('model-select');
        this.modeSelect = document.getElementById('mode-select');
        this.clearChatBtn = document.getElementById('clear-chat-btn');
        this.downloadFullChatBtn = document.getElementById('download-full-chat-btn');
        
        this.providers = [];
        this.currentEventSource = null;
        this.conversationHistory = [];
        this.setupEventListeners();
        this.loadProviders();
        this.checkSession();
        this.showWelcomeMessage();
    }
    
    setupEventListeners() {
        this.sendButton.addEventListener('click', () => this.sendMessage());
        
        this.userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        this.userInput.addEventListener('input', () => {
            this.autoExpandTextarea();
        });
        
        this.uploadButton.addEventListener('click', () => {
            this.fileInput.click();
        });
        
        this.fileInput.addEventListener('change', (e) => {
            if (e.target.files[0]) {
                this.handleFileUpload(e.target.files[0]);
            }
        });
        
        this.providerSelect.addEventListener('change', () => {
            this.updateModelDropdown();
        });
        
        this.clearChatBtn.addEventListener('click', () => this.clearChat());
        this.downloadFullChatBtn.addEventListener('click', () => this.downloadFullChat());
    }
    
    async loadProviders() {
        try {
            const response = await fetch('/api/providers');
            const data = await response.json();
            this.providers = data.providers;
            this.updateProviderDropdown();
        } catch (error) {
            console.error('Failed to load providers:', error);
            this.providerSelect.innerHTML = '<option value="">No providers available</option>';
        }
    }
    
    updateProviderDropdown() {
        if (this.providers.length === 0) {
            this.providerSelect.innerHTML = '<option value="">No providers configured</option>';
            return;
        }
        
        this.providerSelect.innerHTML = this.providers.map(p => 
            `<option value="${p.id}">${p.name}</option>`
        ).join('');
        
        this.updateModelDropdown();
    }
    
    updateModelDropdown() {
        const selectedProvider = this.providers.find(p => p.id === this.providerSelect.value);
        if (!selectedProvider) {
            this.modelSelect.innerHTML = '<option value="">Default</option>';
            return;
        }
        
        this.modelSelect.innerHTML = '<option value="">Default</option>' + 
            selectedProvider.models.map(m => 
                `<option value="${m}">${m}</option>`
            ).join('');
    }
    
    autoExpandTextarea() {
        this.userInput.style.height = 'auto';
        const newHeight = Math.min(this.userInput.scrollHeight, 400);
        this.userInput.style.height = newHeight + 'px';
    }
    
    async checkSession() {
        try {
            const response = await fetch('/api/check-session');
            const data = await response.json();
            if (data.logged_in) {
                this.updateUserStatus(data.username);
            } else {
                this.updateUserStatus(null);
            }
        } catch (error) {
            console.error('Session check failed:', error);
        }
    }
    
    updateUserStatus(username) {
        if (username) {
            this.userStatus.innerHTML = `
                Welcome, ${username} | 
                <button class="btn-link" onclick="chat.logout()">Logout</button>
            `;
        } else {
            this.userStatus.innerHTML = `
                <button class="btn-link" onclick="chat.showLoginModal()">Login</button>
            `;
        }
    }
    
    showLoginModal() {
        const modal = document.getElementById('login-modal');
        const usernameInput = document.getElementById('username-input');
        const submitBtn = document.getElementById('login-submit-btn');
        const cancelBtn = document.getElementById('login-cancel-btn');
        
        modal.style.display = 'flex';
        usernameInput.value = '';
        usernameInput.focus();
        
        const handleSubmit = async () => {
            const username = usernameInput.value.trim();
            if (username) {
                try {
                    const response = await fetch('/api/login', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({username})
                    });
                    if (response.ok) {
                        modal.style.display = 'none';
                        this.updateUserStatus(username);
                    }
                } catch (error) {
                    console.error('Login failed:', error);
                }
            }
        };
        
        submitBtn.onclick = handleSubmit;
        cancelBtn.onclick = () => modal.style.display = 'none';
        usernameInput.onkeypress = (e) => {
            if (e.key === 'Enter') handleSubmit();
        };
    }
    
    async logout() {
        try {
            await fetch('/api/logout', {method: 'POST'});
            this.updateUserStatus(null);
        } catch (error) {
            console.error('Logout failed:', error);
        }
    }
    
    async handleFileUpload(file) {
        const formData = new FormData();
        formData.append('file', file);
        
        this.uploadButton.disabled = true;
        this.uploadButton.textContent = '⏳ Processing...';
        
        try {
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            if (data.text) {
                this.userInput.value = data.text;
                this.autoExpandTextarea();
                this.userInput.focus();
            } else if (data.error) {
                alert('Error: ' + data.error);
            }
        } catch (error) {
            alert('Error uploading file: ' + error.message);
        } finally {
            this.uploadButton.disabled = false;
            this.uploadButton.textContent = '📎 Upload File';
            this.fileInput.value = '';
        }
    }
    
    showWelcomeMessage() {
        if (this.messageContainer.children.length === 0) {
            const welcomeDiv = document.createElement('div');
            welcomeDiv.className = 'empty-state';
            welcomeDiv.innerHTML = `
                <h2>Welcome to Ask a Philosopher</h2>
                <p>Ask J.-M. Kuczynski about epistemology, logic, philosophy of mind, or any philosophical topic.</p>
                <p style="margin-top: 20px; font-size: 0.9em;">
                    You can type your question, paste text, or upload a PDF/Word document.
                </p>
            `;
            this.messageContainer.appendChild(welcomeDiv);
        }
    }
    
    async sendMessage() {
        const question = this.userInput.value.trim();
        if (!question) return;
        
        const welcomeMsg = this.messageContainer.querySelector('.empty-state');
        if (welcomeMsg) {
            welcomeMsg.remove();
        }
        
        this.addMessage('user', question);
        this.userInput.value = '';
        this.userInput.style.height = 'auto';
        
        this.sendButton.disabled = true;
        this.uploadButton.disabled = true;
        
        const responseDiv = this.addMessage('assistant', '💭 Thinking...', true);
        const textDiv = responseDiv.querySelector('.message-text');
        const sourcesDiv = responseDiv.querySelector('.message-sources');
        let firstToken = true;
        
        try {
            const provider = this.providerSelect.value || 'anthropic';
            const model = this.modelSelect.value || '';
            const mode = this.modeSelect.value || 'basic';
            
            const response = await fetch('/api/ask', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    question,
                    provider,
                    model,
                    mode
                })
            });
            
            if (!response.ok) {
                throw new Error('Failed to get response from server');
            }
            
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let buffer = '';
            
            while (true) {
                const {done, value} = await reader.read();
                if (done) break;
                
                buffer += decoder.decode(value, {stream: true});
                const lines = buffer.split('\n');
                buffer = lines.pop();
                
                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        try {
                            const data = JSON.parse(line.slice(6));
                            
                            if (data.type === 'token') {
                                if (firstToken) {
                                    textDiv.textContent = '';
                                    firstToken = false;
                                }
                                textDiv.textContent += data.data;
                                this.scrollToBottom();
                            } else if (data.type === 'sources') {
                                sourcesDiv.textContent = '📚 Sources: ' + data.data.join(', ');
                            } else if (data.type === 'done') {
                                const finalText = textDiv.textContent;
                                const finalSources = sourcesDiv.textContent;
                                this.conversationHistory.push({
                                    role: 'assistant',
                                    content: finalText,
                                    timestamp: new Date().toISOString(),
                                    sources: finalSources
                                });
                                this.addDownloadButton(responseDiv, question);
                            }
                        } catch (e) {
                            console.error('Error parsing SSE data:', e);
                        }
                    }
                }
            }
        } catch (error) {
            textDiv.textContent = 'Error: ' + error.message;
        } finally {
            this.sendButton.disabled = false;
            this.uploadButton.disabled = false;
        }
    }
    
    addMessage(role, content, isStreaming = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message message-${role}`;
        
        const label = document.createElement('div');
        label.className = 'message-label';
        label.textContent = role === 'user' ? 'YOU' : 'KUCZYNSKI';
        
        const textDiv = document.createElement('div');
        textDiv.className = 'message-text';
        textDiv.textContent = content;
        
        messageDiv.appendChild(label);
        messageDiv.appendChild(textDiv);
        
        if (role === 'assistant') {
            const sourcesDiv = document.createElement('div');
            sourcesDiv.className = 'message-sources';
            messageDiv.appendChild(sourcesDiv);
        }
        
        this.messageContainer.appendChild(messageDiv);
        this.scrollToBottom();
        
        if (!isStreaming) {
            this.conversationHistory.push({
                role: role,
                content: content,
                timestamp: new Date().toISOString(),
                sources: ''
            });
        }
        
        return messageDiv;
    }
    
    addDownloadButton(messageDiv, userQuestion) {
        const buttonContainer = document.createElement('div');
        buttonContainer.className = 'download-buttons';
        
        const downloadMdBtn = document.createElement('button');
        downloadMdBtn.className = 'download-btn';
        downloadMdBtn.textContent = '💾 Download as Markdown';
        downloadMdBtn.onclick = () => this.downloadExchange(messageDiv, userQuestion, 'md');
        
        const downloadTxtBtn = document.createElement('button');
        downloadTxtBtn.className = 'download-btn';
        downloadTxtBtn.textContent = '💾 Download as TXT';
        downloadTxtBtn.onclick = () => this.downloadExchange(messageDiv, userQuestion, 'txt');
        
        buttonContainer.appendChild(downloadMdBtn);
        buttonContainer.appendChild(downloadTxtBtn);
        messageDiv.appendChild(buttonContainer);
    }
    
    downloadExchange(messageDiv, userQuestion, format = 'md') {
        const assistantText = messageDiv.querySelector('.message-text').textContent;
        const sources = messageDiv.querySelector('.message-sources').textContent;
        
        const date = new Date().toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
        
        let content, mimeType, extension;
        
        if (format === 'txt') {
            content = `CONVERSATION WITH KUCZYNSKI
Date: ${date}

================================================================================

USER:
${userQuestion}

--------------------------------------------------------------------------------

KUCZYNSKI:
${assistantText}

--------------------------------------------------------------------------------

${sources}

================================================================================

Generated by Ask a Philosopher - J.-M. Kuczynski AI Assistant
`;
            mimeType = 'text/plain';
            extension = 'txt';
        } else {
            content = `# Conversation with Kuczynski
Date: ${date}

## Exchange

**User:** ${userQuestion}

**Kuczynski:** ${assistantText}

**${sources}**

---

*Generated by Ask a Philosopher - J.-M. Kuczynski AI Assistant*
`;
            mimeType = 'text/markdown';
            extension = 'md';
        }
        
        const blob = new Blob([content], {type: mimeType});
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `kuczynski-conversation-${Date.now()}.${extension}`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
    
    scrollToBottom() {
        this.messageContainer.scrollTop = this.messageContainer.scrollHeight;
    }
    
    clearChat() {
        if (confirm('Are you sure you want to clear all messages?')) {
            this.messageContainer.innerHTML = '';
            this.conversationHistory = [];
            this.showWelcomeMessage();
        }
    }
    
    downloadFullChat() {
        if (this.conversationHistory.length === 0) {
            alert('No conversation to download');
            return;
        }
        
        const format = prompt('Choose format:\n1 - Markdown (.md)\n2 - Plain Text (.txt)', '1');
        
        if (!format || (format !== '1' && format !== '2')) {
            return;
        }
        
        const isMarkdown = format === '1';
        const date = new Date().toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
        
        let content = '';
        
        if (isMarkdown) {
            content = `# Complete Conversation with Kuczynski\nDate: ${date}\n\n`;
            content += `Total Exchanges: ${this.conversationHistory.length}\n\n`;
            content += `---\n\n`;
            
            this.conversationHistory.forEach((msg, index) => {
                if (msg.role === 'user') {
                    content += `## Exchange ${Math.floor(index / 2) + 1}\n\n`;
                    content += `**USER:**\n${msg.content}\n\n`;
                } else {
                    content += `**KUCZYNSKI:**\n${msg.content}\n\n`;
                    if (msg.sources) {
                        content += `**${msg.sources}**\n\n`;
                    }
                    content += `---\n\n`;
                }
            });
            
            content += `\n*Generated by Ask a Philosopher - J.-M. Kuczynski AI Assistant*\n`;
        } else {
            content = `COMPLETE CONVERSATION WITH KUCZYNSKI\n`;
            content += `Date: ${date}\n`;
            content += `Total Exchanges: ${this.conversationHistory.length}\n\n`;
            content += `${'='.repeat(80)}\n\n`;
            
            this.conversationHistory.forEach((msg, index) => {
                if (msg.role === 'user') {
                    content += `EXCHANGE ${Math.floor(index / 2) + 1}\n\n`;
                    content += `USER:\n${msg.content}\n\n`;
                    content += `${'-'.repeat(80)}\n\n`;
                } else {
                    content += `KUCZYNSKI:\n${msg.content}\n\n`;
                    if (msg.sources) {
                        content += `${msg.sources}\n\n`;
                    }
                    content += `${'='.repeat(80)}\n\n`;
                }
            });
            
            content += `\nGenerated by Ask a Philosopher - J.-M. Kuczynski AI Assistant\n`;
        }
        
        const mimeType = isMarkdown ? 'text/markdown' : 'text/plain';
        const extension = isMarkdown ? 'md' : 'txt';
        
        const blob = new Blob([content], {type: mimeType});
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `kuczynski-full-conversation-${Date.now()}.${extension}`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
}

let chat;
document.addEventListener('DOMContentLoaded', () => {
    chat = new KuczynskiChat();
});
