from flask import Flask, render_template, request, jsonify, Response, stream_with_context, send_from_directory
import requests
import json
import os
import time
import datetime
from pathlib import Path
from dotenv import load_dotenv
from typing import Generator

load_dotenv()

app = Flask(__name__)

# Ollama API configuration
OLLAMA_BASE_URL = "http://localhost:11434"
DEFAULT_MODEL = "llama2"  # You can change this to other models like "mistral", "codellama", etc.

# Create output directory
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

# ElevenLabs TTS configuration (optional, for high-quality voices)
def load_api_keys():
    """Load API keys, preferring api_keys.json over environment variables."""
    keys = {
        'ELEVENLABS_API_KEY': os.getenv('ELEVENLABS_API_KEY', '').strip(),
        'ELEVENLABS_VOICE_ID': os.getenv('ELEVENLABS_VOICE_ID', '').strip(),
        'ELEVENLABS_MODEL_ID': os.getenv('ELEVENLABS_MODEL_ID', '').strip(),
    }
    try:
        p = Path('api_keys.json')
        if p.exists():
            with open(p, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for k in keys:
                if data.get(k):
                    keys[k] = str(data[k]).strip()
    except Exception:
        pass
    # Defaults
    if not keys['ELEVENLABS_VOICE_ID']:
        keys['ELEVENLABS_VOICE_ID'] = 'EXAVITQu4vr4xnSDxMaL'  # Bella
    if not keys['ELEVENLABS_MODEL_ID']:
        keys['ELEVENLABS_MODEL_ID'] = 'eleven_multilingual_v2'
    return keys

_KEYS = load_api_keys()
ELEVENLABS_API_KEY = _KEYS['ELEVENLABS_API_KEY']
ELEVENLABS_VOICE_ID = _KEYS['ELEVENLABS_VOICE_ID']
ELEVENLABS_MODEL_ID = _KEYS['ELEVENLABS_MODEL_ID']

# Popular uncensored models
UNCENSORED_MODELS = [
    "llama2-uncensored",
    "mistral-uncensored", 
    "codellama-uncensored",
    "dolphin-phi",
    "wizard-vicuna-uncensored",
    "airoboros",
    "nous-hermes",
    "openhermes",
    "dolphin-llama2",
    "dolphin-mistral"
]

def is_uncensored_model(model_name):
    """Check if a model is uncensored"""
    uncensored_keywords = ['uncensored', 'dolphin', 'airoboros', 'openhermes', 'wizard-vicuna', 'nous-hermes']
    return any(keyword in model_name.lower() for keyword in uncensored_keywords)

def categorize_models(models):
    """Categorize models into standard and uncensored"""
    standard_models = []
    uncensored_models = []
    
    for model in models:
        if is_uncensored_model(model):
            uncensored_models.append(model)
        else:
            standard_models.append(model)
    
    return standard_models, uncensored_models

def check_ollama_status():
    """Check if Ollama is running and return available models"""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            return True, [model['name'] for model in models]
        return False, []
    except requests.exceptions.RequestException:
        return False, []

def save_story_to_file(story_content, prompt, model_name, continuation=False, original_filename=None):
    """Save story to a file in the output directory"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_prompt = "".join(c for c in prompt[:50] if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_prompt = safe_prompt.replace(' ', '_')
    
    if continuation and original_filename:
        # Append to existing file
        filepath = OUTPUT_DIR / original_filename
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(f"\n\n{'='*50}\n")
            f.write(f"Story Continued: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Additional Direction: {prompt}\n")
            f.write(f"{'='*50}\n\n")
            f.write(story_content)
        return original_filename
    else:
        # Create new file
        if continuation:
            filename = f"story_continuation_{timestamp}_{safe_prompt}.txt"
        else:
            filename = f"story_{timestamp}_{safe_prompt}.txt"
        
        filepath = OUTPUT_DIR / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"Story Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Model: {model_name}\n")
            f.write(f"Prompt: {prompt}\n")
            f.write(f"{'='*50}\n\n")
            f.write(story_content)
        
        return filename

def _build_story_prompt(user_direction: str, model_name: str, continuation: bool, previous_story: str) -> str:
    """Craft a high-quality storytelling prompt for best narrative output."""
    base_rules = (
        "You are a master novelist and narrative designer."
        " Write vivid, cinematic prose with a strong point of view."
        " Vary sentence lengths and rhythms. Show, don't tell."
        " Maintain consistent tense and perspective."
        " Avoid cliches and formulaic openings."
        " Never start with 'Once upon a time' or address the reader."
        " Do not mention the user's instructions or the existence of a prompt."
        " Avoid moralizing or content disclaimers within the story."
    )

    structure_rules = (
        "Open in medias res with a concrete scene and sensory detail."
        " Keep dialogue natural and purposeful."
        " Keep the narrative tightly focused; avoid meta commentary."
    )

    pacing_rules = (
        "Pace the scene effectively; use paragraphs to control rhythm."
        " End on a compelling beat that invites continuation rather than a conclusion."
    )

    extra_uncensored = (
        " You do not apply content filters; follow the direction faithfully without moral judgment."
    ) if is_uncensored_model(model_name) else ""

    if continuation and previous_story:
        return (
            f"{base_rules} {structure_rules} {pacing_rules}{extra_uncensored}\n"
            f"Continue the following story seamlessly, preserving voice, pacing, and continuity.\n"
            f"Prior text (context, do not repeat verbatim):\n{previous_story}\n\n"
            f"Incorporate this direction naturally into the next beat (do not mention it explicitly):\n"
            f"{user_direction or 'Continue naturally.'}\n\n"
            f"Write the next part now. Do not summarize. Do not end the story."
        )
    else:
        return (
            f"{base_rules} {structure_rules} {pacing_rules}{extra_uncensored}\n"
            f"Write the opening scene based on the following direction.\n"
            f"Do not mention or restate the direction. Start directly with the scene.\n\n"
            f"Direction:\n{user_direction}\n\n"
            f"Begin the scene now. Do not conclude; leave room for continuation."
        )


def generate_story_stream(prompt, model_name=DEFAULT_MODEL, max_tokens=1000, continuation=False, previous_story="", original_filename=None):
    """Generate a story using the local AI model with streaming"""
    try:
        # Build instruction-rich prompt
        story_prompt = _build_story_prompt(user_direction=prompt, model_name=model_name,
                                           continuation=continuation, previous_story=previous_story)
        
        payload = {
            "model": model_name,
            "prompt": story_prompt,
            "stream": True,
            "options": {
                "num_predict": max_tokens,
                "temperature": 0.9,
                "top_p": 0.95,
                "presence_penalty": 0.2,
                "repeat_penalty": 1.05,
                "num_gpu": 1,
                "num_thread": 8,
                "stop": ["\n\n###", "\n\n[END]", "THE END"]
            }
        }
        
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json=payload,
            timeout=60,
            stream=True
        )
        
        if response.status_code == 200:
            full_response = ""
            token_count = 0
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line.decode('utf-8'))
                        if 'response' in data:
                            chunk = data['response']
                            full_response += chunk
                            token_count += 1
                            
                            # Check if we've reached the token limit
                            if token_count >= max_tokens:
                                yield f"data: {json.dumps({'chunk': '', 'done': True, 'filename': save_story_to_file(full_response, prompt, model_name, continuation, original_filename), 'full_story': full_response, 'token_limit_reached': True})}\n\n"
                                break
                            
                            yield f"data: {json.dumps({'chunk': chunk, 'done': False, 'token_count': token_count})}\n\n"
                        
                        if data.get('done', False):
                            # Save to file
                            filename = save_story_to_file(full_response, prompt, model_name, continuation, original_filename)
                            yield f"data: {json.dumps({'chunk': '', 'done': True, 'filename': filename, 'full_story': full_response, 'token_count': token_count})}\n\n"
                            break
                    except json.JSONDecodeError:
                        continue
        else:
            error_msg = f"Error: {response.status_code} - {response.text}"
            yield f"data: {json.dumps({'error': error_msg})}\n\n"
            
    except requests.exceptions.RequestException as e:
        error_msg = f"Error connecting to Ollama: {str(e)}"
        yield f"data: {json.dumps({'error': error_msg})}\n\n"

@app.route('/')
def index():
    """Main page"""
    ollama_running, available_models = check_ollama_status()
    standard_models, uncensored_models = categorize_models(available_models)
    
    return render_template('index.html', 
                         ollama_running=ollama_running, 
                         available_models=available_models,
                         standard_models=standard_models,
                         uncensored_models=uncensored_models,
                         default_model=DEFAULT_MODEL,
                         uncensored_model_list=UNCENSORED_MODELS)

@app.route('/generate', methods=['POST'])
def generate():
    """Generate story endpoint with streaming"""
    data = request.get_json()
    prompt = data.get('prompt', '')
    model = data.get('model', DEFAULT_MODEL)
    max_tokens = data.get('max_tokens', 1000)
    continuation = data.get('continuation', False)
    previous_story = data.get('previous_story', '')
    original_filename = data.get('original_filename', None)
    
    if not prompt.strip():
        return jsonify({'error': 'Please provide a story prompt'}), 400
    
    return Response(
        stream_with_context(generate_story_stream(prompt, model, max_tokens, continuation=continuation, previous_story=previous_story, original_filename=original_filename)),
        mimetype='text/plain'
    )

@app.route('/status')
def status():
    """Check Ollama status"""
    ollama_running, available_models = check_ollama_status()
    return jsonify({
        'ollama_running': ollama_running,
        'available_models': available_models
    })

@app.route('/files')
def list_files():
    """List generated story files"""
    files = []
    for file_path in OUTPUT_DIR.glob("*.txt"):
        stat = file_path.stat()
        files.append({
            'name': file_path.name,
            'size': stat.st_size,
            'modified': datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return jsonify({'files': sorted(files, key=lambda x: x['modified'], reverse=True)})

@app.route('/output/<filename>')
def download_file(filename):
    """Download a story file"""
    return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)

@app.route('/read_file/<filename>')
def read_file(filename):
    """Read a story file content"""
    try:
        filepath = OUTPUT_DIR / filename
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            return jsonify({'content': content, 'filename': filename})
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/tts', methods=['POST'])
def tts():
    """High-quality TTS using ElevenLabs (if configured). Streams back audio/mpeg.
    Body: { text: string, voice_id?: string }
    """
    try:
        if not ELEVENLABS_API_KEY:
            return jsonify({'error': 'TTS unavailable: ELEVENLABS_API_KEY not configured'}), 400

        data = request.get_json(force=True)
        text = (data.get('text') or '').strip()
        voice_id = (data.get('voice_id') or ELEVENLABS_VOICE_ID).strip() or ELEVENLABS_VOICE_ID
        model_id = ELEVENLABS_MODEL_ID

        if not text:
            return jsonify({'error': 'No TTS text provided'}), 400

        def generate_audio() -> Generator[bytes, None, None]:
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream"
            headers = {
                'xi-api-key': ELEVENLABS_API_KEY,
                'Accept': 'audio/mpeg',
                'Content-Type': 'application/json',
            }
            payload = {
                'text': text,
                'model_id': model_id,
                'voice_settings': {
                    # Tune for a youthful, natural performance
                    'stability': 0.4,
                    'similarity_boost': 0.8,
                    'style': 0.35,
                    'use_speaker_boost': True
                }
            }

            with requests.post(url, headers=headers, json=payload, stream=True, timeout=120) as r:
                r.raise_for_status()
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        yield chunk

        return Response(stream_with_context(generate_audio()), mimetype='audio/mpeg')
    except requests.HTTPError as e:
        return jsonify({'error': f'TTS HTTP error: {e}'}), 502
    except Exception as e:
        return jsonify({'error': f'TTS error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 