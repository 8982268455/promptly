# Promptly 🧠💬

[![Python](https://img.shields.io/badge/python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/)  
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)  
[![GitHub stars](https://img.shields.io/github/stars/8982268455/promptly?style=social)](https://github.com/8982268455/promptly)  
[![GitHub forks](https://img.shields.io/github/forks/8982268455/promptly?style=social)](https://github.com/8982268455/promptly/network/members)  
[![GitHub issues](https://img.shields.io/github/issues/8982268455/promptly)](https://github.com/8982268455/promptly/issues)  

> **Promptly** — A lightweight web-based chat application that allows multiple users to interact with an AI model in real-time with Markdown rendering and syntax-highlighted code blocks.

---

## 🌟 Features

- ✅ Real-time streaming of AI responses  
- ✅ Multiple chat sessions with persistent history  
- ✅ SQLite storage of sessions and messages  
- ✅ Token-aware message pruning  
- ✅ Markdown + syntax-highlighted code rendering  
- ✅ Fully configurable GPT-4 parameters via `config.yaml`  

---

## 📂 Project Structure

| Script / File | Description |
|---------------|-------------|
| 🏁`main.py` | Entry point to start the chat server. Opens browser automatically. |
| ⚡`server/run_server.py` | Starts multi-threaded HTTP server and handles graceful shutdown. |
| 🌐`server/chat.py` | Handles HTTP requests, manages sessions, and streams AI responses. |
| 🤖`server/chat_service.py` | Core service for chat session management and AI response streaming. |
| 📝`server/message_manager.py` | Adds, retrieves, prunes, and updates messages with token limits. |
| 🗂️`server/session_manager.py` | Creates, deletes, and initializes chat sessions with system prompts. |
| 📂`server/static_handler.py` | Serves static files (HTML, CSS, JS) with correct MIME types. |
| ⚡`ai/streaming.py` | Sends messages to GPT API and streams responses line by line. |
| 💾`db/connection.py` | Manages SQLite connection and auto-creates tables for sessions/messages. |
| ⚙️`config/config_loader.py` | Reads and provides access to `config.yaml` settings. |
| 🔢`tokenizer/tokenizer_utils.py` | Loads tokenizer and counts tokens for chat messages. |
| 🌐`utils/network.py` | Retrieves local LAN IP address for browser access. |
| 🖥️`static/js/chat.js` | Frontend logic for chat UI, Markdown rendering, and session handling. |
| 🎨`static/js/prism.js` | Syntax highlighting library for code blocks. |
| 📜`static/js/markdown-it.min.js` | Markdown parser library for AI responses. |
| 🎨`static/css/style.css` | Styling for chat interface: messages, input, buttons, responsive layout. |
| 💻`static/css/prism.css` | Syntax highlighting CSS for code blocks. |
| 🏗️`templates/index.html` | HTML layout for chat interface with sidebar, chat panel, and input area. |

> ⚠️ **Note:** `data/sessions.db` is auto-generated when you first run the server and stores chat history. Do not delete unless you want to reset all chat sessions.

---

## Installation & Setup

1. **Clone the repository**

```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

2. **Create a virtual environment**

```bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```
3. **Install dependencies**

```bash
pip install -r requirements.txt
```
4. **Configure config file**
Edit config/config.yaml to add your model API credentials, generation parameters and system prompt (By setting system prompt, decide behave of promptly).
## 🚨 Important
**Promptly supports OpenAI-type LLMs**

5. **start the server**
```bash
python main.py
```
- The server will open your browser automatically with the local/LAN URL.
- Chat sessions are stored in data/sessions.db ⚠️ (auto-generated).

---
> ## Don't have OpenAI API? Run small LLMs (LLaMA 2, Mistral 7B, etc.) with Ollama
> - Download the Ollama executable from [ollama.ai](https://ollama.ai)
> - Install the executable on your machine (minimum: 16 GB RAM, 4–8 GB VRAM; NVIDIA GPU recommended)
> - Pull and run model weights (e.g., `ollama pull llama2` then `ollama run llama2`)
> - Ollama hosts the model locally on default API endpoints:
>   - `http://localhost:11434/api/chat` (chat-style interactions → `stream = true`)
>   - `http://localhost:11434/api/generate` (single-shot generation → `stream = false`)
> - We support `stream = true` by default. If you want `stream = false`, use the appropriate API and modify `ai/streamming.py` (`build_payload` and `call_ai_api_stream`)
> - Configure your `config/config.yaml` file accordingly (no auth required since it runs locally)
> - Add additional functions in `config/config_loader.py` if you introduce new parameters in `config.yaml`
> - Modify the payload in `ai/streamming.py` with appropriate generation parameters and keys
---

## Usage
- Open the URL provided by the server in your browser.
- Start a new chat session or continue an existing one.
- Messages and AI responses are streamed in real time.
- Markdown and code blocks are rendered with syntax highlighting.

---

## Contributing
- Fork the repository.
- Create a feature branch: git checkout -b feature/my-feature.
- Commit your changes: git commit -m "Add feature".
- Push your branch: git push origin feature/my-feature.
- Open a pull request for review.

---

## Support
If you enjoy Promptly, please ⭐ the repository and share it with others working on AI chat applications.

---

## License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
. See LICENSE for details.



