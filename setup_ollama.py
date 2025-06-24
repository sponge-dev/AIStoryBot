#!/usr/bin/env python3
"""
Setup script for Ollama AI Storyteller
This script helps install and configure Ollama for the AI Storyteller app.
"""

import os
import sys
import subprocess
import platform
import requests
import time
from pathlib import Path

def print_banner():
    """Print a nice banner"""
    print("=" * 60)
    print("🤖 AI Storyteller - Ollama Setup")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def install_python_dependencies():
    """Install Python dependencies"""
    print("📦 Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Python dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install Python dependencies")
        sys.exit(1)

def get_ollama_install_url():
    """Get the appropriate Ollama download URL for the current platform"""
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    # Get the latest version from Ollama's releases
    try:
        response = requests.get("https://api.github.com/repos/ollama/ollama/releases/latest")
        if response.status_code == 200:
            latest_version = response.json()["tag_name"]
        else:
            latest_version = "v0.1.29"  # Fallback version
    except:
        latest_version = "v0.1.29"  # Fallback version
    
    base_url = f"https://github.com/ollama/ollama/releases/download/{latest_version}"
    
    if system == "windows":
        return f"{base_url}/ollama-windows-amd64.exe"
    elif system == "darwin":  # macOS
        if "arm" in machine or "aarch64" in machine:
            return f"{base_url}/ollama-darwin-arm64"
        else:
            return f"{base_url}/ollama-darwin-amd64"
    elif system == "linux":
        if "arm" in machine or "aarch64" in machine:
            return f"{base_url}/ollama-linux-arm64"
        else:
            return f"{base_url}/ollama-linux-amd64"
    else:
        return None

def download_ollama():
    """Download Ollama binary"""
    url = get_ollama_install_url()
    if not url:
        print("❌ Unsupported platform. Please install Ollama manually from https://ollama.ai")
        return False
    
    print(f"📥 Downloading Ollama from {url}")
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # Determine filename
        if platform.system().lower() == "windows":
            filename = "ollama.exe"
        else:
            filename = "ollama"
        
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        # Make executable on Unix systems
        if platform.system().lower() != "windows":
            os.chmod(filename, 0o755)
        
        print(f"✅ Ollama downloaded as {filename}")
        return True
    except Exception as e:
        print(f"❌ Failed to download Ollama: {e}")
        print("\n📋 Please install Ollama manually:")
        print("1. Visit https://ollama.ai")
        print("2. Download the installer for your platform")
        print("3. Run the installer")
        print("4. Run this script again")
        return False

def check_ollama_installed():
    """Check if Ollama is already installed"""
    try:
        result = subprocess.run(["ollama", "--version"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ Ollama is already installed: {result.stdout.strip()}")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return False

def start_ollama():
    """Start Ollama service"""
    print("🚀 Starting Ollama service...")
    try:
        # Start Ollama in the background
        if platform.system().lower() == "windows":
            subprocess.Popen(["ollama", "serve"], 
                           creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            subprocess.Popen(["ollama", "serve"], 
                           stdout=subprocess.DEVNULL, 
                           stderr=subprocess.DEVNULL)
        
        # Wait a bit for Ollama to start
        print("⏳ Waiting for Ollama to start...")
        time.sleep(5)
        
        # Check if it's running
        for _ in range(10):
            try:
                response = requests.get("http://localhost:11434/api/tags", timeout=2)
                if response.status_code == 200:
                    print("✅ Ollama is running successfully")
                    return True
            except requests.exceptions.RequestException:
                time.sleep(2)
        
        print("⚠️  Ollama may not have started properly. Please start it manually with 'ollama serve'")
        return False
        
    except Exception as e:
        print(f"❌ Failed to start Ollama: {e}")
        return False

def download_model(model_name="llama2"):
    """Download a model"""
    print(f"📥 Downloading {model_name} model...")
    try:
        subprocess.check_call(["ollama", "pull", model_name])
        print(f"✅ {model_name} model downloaded successfully")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Failed to download {model_name} model")
        return False

def main():
    """Main setup function"""
    print_banner()
    
    # Check Python version
    check_python_version()
    
    # Install Python dependencies
    install_python_dependencies()
    
    # Check if Ollama is already installed
    if not check_ollama_installed():
        print("\n📋 Ollama is not installed. You have two options:")
        print("1. Download Ollama automatically (recommended)")
        print("2. Install Ollama manually from https://ollama.ai")
        
        choice = input("\nEnter your choice (1 or 2): ").strip()
        
        if choice == "1":
            if not download_ollama():
                print("\n❌ Automatic download failed. Please install Ollama manually.")
                print("Visit: https://ollama.ai")
                sys.exit(1)
        else:
            print("\n📋 Please install Ollama manually from https://ollama.ai")
            print("After installation, run this script again.")
            sys.exit(0)
    
    # Start Ollama
    if not start_ollama():
        print("\n⚠️  Please start Ollama manually with: ollama serve")
        print("Then run this script again to download models.")
        sys.exit(0)
    
    # Download default model
    print("\n📋 Which model would you like to download?")
    print("\n🔒 Standard Models (with safety filters):")
    print("1. llama2 (default, ~4GB) - General storytelling")
    print("2. mistral (faster, ~4GB) - Creative writing")
    print("3. codellama (good for code, ~7GB) - Technical stories")
    print("4. phi (smaller, ~2GB) - Quick stories")
    
    print("\n🔓 Uncensored Models (fewer restrictions):")
    print("5. llama2-uncensored (~4GB) - Unfiltered storytelling")
    print("6. mistral-uncensored (~4GB) - Unfiltered creative writing")
    print("7. dolphin-phi (~2GB) - Fast uncensored stories")
    print("8. airoboros (~4GB) - Uncensored creative content")
    print("9. openhermes (~4GB) - Uncensored general purpose")
    print("10. wizard-vicuna-uncensored (~4GB) - Uncensored roleplay")
    print("11. nous-hermes (~4GB) - Uncensored conversations")
    
    model_choice = input("\nEnter model name or number (default: llama2): ").strip()
    
    model_map = {
        "1": "llama2",
        "2": "mistral", 
        "3": "codellama",
        "4": "phi",
        "5": "llama2-uncensored",
        "6": "mistral-uncensored",
        "7": "dolphin-phi",
        "8": "airoboros",
        "9": "openhermes",
        "10": "wizard-vicuna-uncensored",
        "11": "nous-hermes"
    }
    
    model_name = model_map.get(model_choice, model_choice) or "llama2"
    
    # Show warning for uncensored models
    if any(uncensored in model_name.lower() for uncensored in ['uncensored', 'dolphin', 'airoboros', 'openhermes', 'wizard-vicuna', 'nous-hermes']):
        print(f"\n⚠️  WARNING: {model_name} is an uncensored model.")
        print("   It can generate content that may be inappropriate for all audiences.")
        print("   Use responsibly and ensure you're in an appropriate environment.")
        confirm = input("\nDo you want to continue? (y/N): ").strip().lower()
        if confirm not in ['y', 'yes']:
            print("Setup cancelled.")
            sys.exit(0)
    
    if download_model(model_name):
        print(f"\n🎉 Setup complete! {model_name} model is ready.")
    else:
        print(f"\n⚠️  Failed to download {model_name}. You can try again later with:")
        print(f"   ollama pull {model_name}")
    
    print("\n🚀 To start the AI Storyteller app, run:")
    print("   python app.py")
    print("\nThen open your browser to: http://localhost:5000")

if __name__ == "__main__":
    main() 