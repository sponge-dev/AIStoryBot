# 🤖 AI Storyteller

A powerful web application for creating and continuing stories using local AI models through Ollama. Generate engaging narratives with complete control over content, token limits, and model selection.

## ✨ Features

### 🎯 Core Functionality
- **Story Generation**: Create stories from custom prompts using local AI models
- **Story Continuation**: Seamlessly continue existing stories with additional direction
- **Real-time Streaming**: Watch stories generate word-by-word with live updates
- **Token Control**: Precise control over story length with adjustable token limits
- **Stop Generation**: Halt story generation at any time and continue later

### 🔓 Model Support
- **Standard Models**: Llama2, Mistral, Phi, CodeLlama with built-in safety filters
- **Uncensored Models**: Complete range from 7B to 70B+ parameters
- **Large Models**: Support for powerful models like Llama 3.1, Mixtral, and Qwen
- **GPU Acceleration**: Optimized for GPU usage with multi-threading support

### 📁 File Management
- **Automatic Saving**: Stories are automatically saved to the output directory
- **File Browser**: Browse, load, and download previously generated stories
- **Story Continuation**: Append new content to existing story files
- **File Organization**: Timestamped files with descriptive names

### 🎨 User Interface
- **Modern Design**: Clean, responsive interface with dark/light themes
- **Two-Column Layout**: Sidebar for controls, main area for story display
- **Tabbed Interface**: Separate tabs for story generation and file management
- **Token Tracker**: Real-time display of generated tokens vs. limit
- **Progress Indicators**: Clear status updates during generation

### ⚙️ Advanced Controls
- **Model Selection**: Choose from available Ollama models
- **Token Slider**: Adjustable token limit from 100 to 4000 tokens
- **Editable Content**: Direct editing of story content in the interface
- **Copy/Download**: Easy export of stories to clipboard or files

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Ollama installed and running
- At least one AI model downloaded

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-storyteller
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install and setup Ollama**
   ```bash
   python install_ollama.py
   ```
   This script will:
   - Install Ollama if not present
   - Start the Ollama service
   - Download your choice of AI models

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## 📚 Model Setup

### Automatic Setup
Run the setup script to automatically install models:
```bash
python install_ollama.py
```

### Manual Setup
1. **Install Ollama**: Download from [ollama.ai](https://ollama.ai)
2. **Start Ollama**: Run `ollama serve`
3. **Download Models**: Use `ollama pull <model-name>`

### Recommended Models

#### Standard Models (Beginner)
- `llama2:7b` - Fast, reliable, good for basic stories
- `mistral:7b` - Balanced performance and quality
- `phi:2.7b` - Very fast, works on most computers

#### Uncensored Models (Advanced)
- **Small (7B)**: `llama2-uncensored:7b`, `dolphin-phi:2.7b`
- **Medium (13B)**: `dolphin-llama2:13b`, `nous-hermes:13b`
- **Large (30B+)**: `llama2-uncensored:70b`, `dolphin-llama2:70b`
- **Mixtral (8x7B)**: `dolphin-mixtral:8x7b`, `mixtral-uncensored:8x7b`

## 🎮 Usage Guide

### Creating a Story
1. Select an AI model from the dropdown
2. Adjust the token limit using the slider
3. Enter your story prompt
4. Click "Generate Story"
5. Watch the story generate in real-time
6. Use "Stop Generation" to halt at any point

### Continuing a Story
1. After generating or loading a story, the continuation form appears
2. Enter additional direction (optional - can be left empty)
3. Click "Continue Story" to add more content
4. The new content is automatically appended to the original file

### Managing Files
1. Click the "Files" tab to browse generated stories
2. Use "Load" to open a story in the editor
3. Use "Download" to save stories locally
4. Stories are automatically saved with timestamps

### Token Management
- **Token Slider**: Set maximum tokens (100-4000)
- **Token Tracker**: Shows current tokens vs. limit
- **Hard Limit**: Generation stops exactly at the token limit
- **Stop Sequences**: Natural endings with proper formatting

## ⚠️ Important Notes

### Uncensored Models
- Uncensored models can generate explicit, violent, or controversial content
- Use responsibly and ensure compliance with local laws
- These models have no content restrictions or safety filters

### System Requirements
- **Small Models (7B)**: 8GB RAM minimum
- **Medium Models (13B)**: 16GB RAM recommended
- **Large Models (30B+)**: 32GB RAM and good GPU
- **Mixtral Models**: 64GB RAM recommended

### Performance Tips
- Use GPU acceleration for faster generation
- Smaller models are faster but less detailed
- Larger models provide better quality but slower generation
- Token limits help control generation time and cost

## 🔧 Configuration

### Environment Variables
Create a `.env` file for custom configuration:
```env
OLLAMA_BASE_URL=http://localhost:11434
DEFAULT_MODEL=llama2:7b
```

### Custom Models
Add your own models to the `UNCENSORED_MODELS` list in `app.py`:
```python
UNCENSORED_MODELS = [
    "your-custom-model:7b",
    "another-model:13b"
]
```

## 📁 Project Structure

```
ai-storyteller/
├── app.py                 # Main Flask application
├── install_ollama.py      # Ollama setup script
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── GETTING_STARTED.md    # Detailed setup guide
├── .gitignore           # Git ignore rules
├── templates/
│   └── index.html       # Web interface
└── output/              # Generated story files
```

## 🛠️ Development

### Running in Development
```bash
python app.py
```
The app runs in debug mode with auto-reload enabled.

### Production Deployment
For production, use a WSGI server like Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source. Please use responsibly and ensure compliance with local laws regarding AI-generated content.

## 🆘 Troubleshooting

### Common Issues

**Ollama not running**
- Ensure Ollama is installed and running: `ollama serve`
- Check if the service is accessible: `curl http://localhost:11434/api/tags`

**No models available**
- Download models: `ollama pull llama2:7b`
- Check available models: `ollama list`

**Slow generation**
- Use smaller models for faster generation
- Ensure GPU acceleration is enabled
- Check system resources (RAM, CPU)

**Token limit not working**
- Ensure you're using the latest version
- Check that the token count is being tracked properly
- Verify the model supports the specified token limit

## 🔗 Links

- [Ollama Official Site](https://ollama.ai)
- [Ollama Documentation](https://ollama.ai/docs)
- [Model Library](https://ollama.ai/library)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

**Disclaimer**: This application uses AI models that can generate content without restrictions. Users are responsible for ensuring all generated content complies with applicable laws and regulations. Use responsibly. 
