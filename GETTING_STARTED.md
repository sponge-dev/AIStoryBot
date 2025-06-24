# 🚀 Getting Started - AI Storyteller

## Quick Start (3 Steps)

### 1. Run the Setup Script
```bash
python setup_ollama.py
```
This will:
- Install Python dependencies
- Download and install Ollama (if not already installed)
- Start the Ollama service
- Download a default AI model (llama2)

### 2. Start the Application
```bash
python app.py
```
Or simply double-click `start.bat` on Windows.

### 3. Open Your Browser
Go to: **http://localhost:5000**

## What You'll Get

- 🤖 **Local AI Storytelling**: All processing happens on your computer
- 🎨 **Beautiful Interface**: Modern, responsive web design
- 📚 **Creative Stories**: Generate unique stories from your prompts
- ⚡ **Fast Performance**: No internet required after setup

## Example Story Prompts

Try these creative prompts:
- "A young wizard discovers a magical library hidden in the clouds"
- "A robot learns to paint and finds its true purpose"
- "A time traveler accidentally brings a dinosaur to modern day"
- "A chef who can taste emotions through food"

## System Requirements

- **Windows 10/11, macOS, or Linux**
- **4GB+ RAM** (8GB recommended)
- **2-8GB free disk space** (depending on model)
- **Python 3.7+**

## Troubleshooting

**If Ollama isn't starting:**
- Run `ollama serve` manually
- Check if port 11434 is available

**If no models appear:**
- Run `ollama pull llama2` to download a model
- Or try `ollama pull mistral` for a faster model

**If the web app won't start:**
- Make sure port 5000 is free
- Try `python app.py --port 5001` to use a different port

## Need Help?

- Check the full [README.md](README.md) for detailed instructions
- Visit [Ollama.ai](https://ollama.ai) for Ollama documentation
- The app will show setup instructions if Ollama isn't running

---

**Happy Storytelling! 📚✨** 