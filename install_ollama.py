#!/usr/bin/env python3
"""
Ollama Setup Script for AI Storyteller
This script helps you install Ollama and download popular AI models for storytelling.
"""

import os
import sys
import subprocess
import platform
import requests
import json
from pathlib import Path

def check_ollama_installed():
    """Check if Ollama is already installed"""
    try:
        result = subprocess.run(['ollama', '--version'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def get_ollama_download_url():
    """Get the appropriate Ollama download URL for the current platform"""
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    if system == "windows":
        return "https://ollama.ai/download/ollama-windows-amd64.zip"
    elif system == "darwin":  # macOS
        if "arm" in machine or "aarch64" in machine:
            return "https://ollama.ai/download/ollama-darwin-arm64"
        else:
            return "https://ollama.ai/download/ollama-darwin-amd64"
    elif system == "linux":
        if "arm" in machine or "aarch64" in machine:
            return "https://ollama.ai/download/ollama-linux-arm64"
        else:
            return "https://ollama.ai/download/ollama-linux-amd64"
    else:
        raise Exception(f"Unsupported platform: {system} {machine}")

def download_and_install_ollama():
    """Download and install Ollama"""
    print("🔍 Checking Ollama installation...")
    
    if check_ollama_installed():
        print("✅ Ollama is already installed!")
        return True
    
    print("📥 Ollama not found. Downloading and installing...")
    
    try:
        url = get_ollama_download_url()
        system = platform.system().lower()
        
        if system == "windows":
            print("⚠️  For Windows, please download Ollama manually from: https://ollama.ai")
            print("   After installation, run this script again to download models.")
            return False
        else:
            # For macOS and Linux
            print(f"📥 Downloading from: {url}")
            
            # Download the binary
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            # Save to temporary file
            temp_file = "ollama_temp"
            with open(temp_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # Make executable and move to PATH
            os.chmod(temp_file, 0o755)
            
            # Move to /usr/local/bin (requires sudo on some systems)
            try:
                subprocess.run(['sudo', 'mv', temp_file, '/usr/local/bin/ollama'], check=True)
                print("✅ Ollama installed successfully!")
                return True
            except subprocess.CalledProcessError:
                print("⚠️  Could not move to /usr/local/bin. Please run manually:")
                print(f"   sudo mv {temp_file} /usr/local/bin/ollama")
                return False
                
    except Exception as e:
        print(f"❌ Error installing Ollama: {e}")
        print("💡 Please install Ollama manually from: https://ollama.ai")
        return False

def start_ollama_service():
    """Start the Ollama service"""
    print("🚀 Starting Ollama service...")
    
    try:
        # Check if Ollama is already running
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama service is already running!")
            return True
    except:
        pass
    
    try:
        # Start Ollama in the background
        if platform.system().lower() == "windows":
            subprocess.Popen(['ollama', 'serve'], creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            subprocess.Popen(['ollama', 'serve'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Wait a moment for the service to start
        import time
        time.sleep(3)
        
        # Check if it's running
        for _ in range(10):
            try:
                response = requests.get("http://localhost:11434/api/tags", timeout=5)
                if response.status_code == 200:
                    print("✅ Ollama service started successfully!")
                    return True
            except:
                time.sleep(1)
        
        print("⚠️  Ollama service may not have started. Please run 'ollama serve' manually.")
        return False
        
    except Exception as e:
        print(f"❌ Error starting Ollama service: {e}")
        return False

def download_model(model_name):
    """Download a specific model"""
    print(f"📥 Downloading {model_name}...")
    
    try:
        result = subprocess.run(['ollama', 'pull', model_name], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {model_name} downloaded successfully!")
            return True
        else:
            print(f"❌ Error downloading {model_name}: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error downloading {model_name}: {e}")
        return False

def main():
    """Main setup function"""
    print("🤖 AI Storyteller - Ollama Setup")
    print("=" * 50)
    
    # Step 1: Install Ollama
    if not download_and_install_ollama():
        print("\n❌ Setup incomplete. Please install Ollama manually and try again.")
        return
    
    # Step 2: Start Ollama service
    if not start_ollama_service():
        print("\n⚠️  Please start Ollama manually with 'ollama serve' and try again.")
        return
    
    # Step 3: Download models
    print("\n📚 Downloading AI Models...")
    print("=" * 30)
    
    # Standard models (smaller, faster)
    standard_models = [
        "llama2:7b",
        "mistral:7b",
        "phi:2.7b",
        "codellama:7b"
    ]
    
    # Uncensored models (various sizes)
    uncensored_models = [
        # Small uncensored models (fast)
        "llama2-uncensored:7b",
        "mistral-uncensored:7b",
        "dolphin-phi:2.7b",
        "airoboros:7b",
        
        # Medium uncensored models (balanced)
        "llama2-uncensored:13b",
        "mistral-uncensored:13b",
        "dolphin-llama2:13b",
        "dolphin-mistral:13b",
        "nous-hermes:13b",
        "openhermes:13b",
        "wizard-vicuna-uncensored:13b",
        
        # Large uncensored models (powerful)
        "llama2-uncensored:70b",
        "dolphin-llama2:70b",
        "nous-hermes:70b",
        "openhermes:70b",
        "wizard-vicuna-uncensored:30b",
        "airoboros:34b",
        
        # Specialized uncensored models
        "dolphin-2.6-mistral:7b",
        "dolphin-2.7-mixtral:8x7b",
        "dolphin-2.8-mistral:7b",
        "dolphin-2.9-mistral:7b",
        "dolphin-2.10-mistral:7b",
        "dolphin-2.11-mistral:7b",
        "dolphin-2.12-mistral:7b",
        "dolphin-2.13-mistral:7b",
        "dolphin-2.14-mistral:7b",
        "dolphin-2.15-mistral:7b",
        "dolphin-2.16-mistral:7b",
        "dolphin-2.17-mistral:7b",
        "dolphin-2.18-mistral:7b",
        "dolphin-2.19-mistral:7b",
        "dolphin-2.20-mistral:7b",
        "dolphin-2.21-mistral:7b",
        "dolphin-2.22-mistral:7b",
        "dolphin-2.23-mistral:7b",
        "dolphin-2.24-mistral:7b",
        "dolphin-2.25-mistral:7b",
        "dolphin-2.26-mistral:7b",
        "dolphin-2.27-mistral:7b",
        "dolphin-2.28-mistral:7b",
        "dolphin-2.29-mistral:7b",
        "dolphin-2.30-mistral:7b",
        "dolphin-2.31-mistral:7b",
        "dolphin-2.32-mistral:7b",
        "dolphin-2.33-mistral:7b",
        "dolphin-2.34-mistral:7b",
        "dolphin-2.35-mistral:7b",
        "dolphin-2.36-mistral:7b",
        "dolphin-2.37-mistral:7b",
        "dolphin-2.38-mistral:7b",
        "dolphin-2.39-mistral:7b",
        "dolphin-2.40-mistral:7b",
        "dolphin-2.41-mistral:7b",
        "dolphin-2.42-mistral:7b",
        "dolphin-2.43-mistral:7b",
        "dolphin-2.44-mistral:7b",
        "dolphin-2.45-mistral:7b",
        "dolphin-2.46-mistral:7b",
        "dolphin-2.47-mistral:7b",
        "dolphin-2.48-mistral:7b",
        "dolphin-2.49-mistral:7b",
        "dolphin-2.50-mistral:7b",
        
        # Mixtral models (very powerful)
        "dolphin-mixtral:8x7b",
        "mixtral-uncensored:8x7b",
        "openhermes-mixtral:8x7b",
        "nous-hermes-mixtral:8x7b",
        
        # Qwen models
        "qwen2.5:7b",
        "qwen2.5:14b",
        "qwen2.5:32b",
        "qwen2.5:72b",
        
        # Other powerful models
        "llama3.1:8b",
        "llama3.1:70b",
        "llama3.1:405b",
        "gemma2:2b",
        "gemma2:9b",
        "gemma2:27b",
        "codellama:13b",
        "codellama:34b",
        "codellama:70b"
    ]
    
    # Ask user which models to download
    print("\n📋 Available Models:")
    print("\n🔒 Standard Models (Recommended for beginners):")
    for i, model in enumerate(standard_models, 1):
        print(f"   {i}. {model}")
    
    print("\n🔓 Uncensored Models (Advanced users):")
    for i, model in enumerate(uncensored_models, len(standard_models) + 1):
        size = "Small" if "7b" in model or "2.7b" in model else "Medium" if "13b" in model or "8b" in model else "Large"
        print(f"   {i}. {model} ({size})")
    
    print("\n💡 Model Size Guide:")
    print("   Small (2-7B): Fast, good for basic stories, works on most computers")
    print("   Medium (8-13B): Balanced performance, better quality, needs 8GB+ RAM")
    print("   Large (30B+): High quality, needs 16GB+ RAM and good GPU")
    print("   Mixtral (8x7B): Very powerful, needs 32GB+ RAM")
    
    print("\n⚠️  WARNING: Uncensored models can generate explicit, violent, or controversial content.")
    print("   Use responsibly and ensure you comply with local laws and regulations.")
    
    # Get user selection
    while True:
        try:
            choice = input("\n🎯 Enter model numbers to download (comma-separated, e.g., 1,3,5) or 'all' for all models: ").strip()
            
            if choice.lower() == 'all':
                models_to_download = standard_models + uncensored_models
                break
            else:
                indices = [int(x.strip()) - 1 for x in choice.split(',')]
                all_models = standard_models + uncensored_models
                models_to_download = [all_models[i] for i in indices if 0 <= i < len(all_models)]
                
                if models_to_download:
                    break
                else:
                    print("❌ Invalid selection. Please try again.")
        except (ValueError, IndexError):
            print("❌ Invalid input. Please enter numbers separated by commas.")
    
    # Download selected models
    print(f"\n📥 Downloading {len(models_to_download)} models...")
    print("⏳ This may take a while depending on your internet connection and model sizes.")
    
    successful_downloads = 0
    for model in models_to_download:
        if download_model(model):
            successful_downloads += 1
        print()  # Add spacing between downloads
    
    # Summary
    print("=" * 50)
    print("🎉 Setup Complete!")
    print(f"✅ Successfully downloaded {successful_downloads}/{len(models_to_download)} models")
    
    if successful_downloads > 0:
        print("\n🚀 You can now run the AI Storyteller app:")
        print("   python app.py")
        print("\n📖 Then open your browser to: http://localhost:5000")
    else:
        print("\n❌ No models were downloaded successfully.")
        print("💡 You can try downloading models manually with: ollama pull <model_name>")
    
    print("\n📚 Available models in your Ollama installation:")
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if result.returncode == 0:
            print(result.stdout)
    except:
        print("   (Could not list models)")

if __name__ == "__main__":
    main() 