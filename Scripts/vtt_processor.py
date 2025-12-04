#!/usr/bin/env python3
"""VTT Processor for CoreLink"""
import sys, json, pyperclip, argparse
import sounddevice as sd
import wavio
import whisperx
from pathlib import Path

# --- Config ---
MODEL_NAME = "base"
SAMPLE_RATE = 16000

def record_audio(filepath: Path, duration: int):
    print(f"🎤 Recording {duration}s... (Speak now)")
    audio = sd.rec(int(duration * SAMPLE_RATE), samplerate=SAMPLE_RATE, 
                   channels=1, dtype='float32')
    sd.wait()
    wavio.write(str(filepath), audio, SAMPLE_RATE, sampwidth=2)
    print("✅ Recording saved")

def transcribe(filepath: Path) -> str:
    print(f"🤖 Loading WhisperX '{MODEL_NAME}'...")
    model = whisperx.load_model(MODEL_NAME, device="cpu", compute_type="int8")
    result = model.transcribe(str(filepath))
    return result["text"].strip()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration", type=int, default=5)
    parser.add_argument("--clipboard", action="store_true")
    args = parser.parse_args()
    
    temp_file = Path.home() / "temp_vtt.wav"
    try:
        record_audio(temp_file, args.duration)
        text = transcribe(temp_file)
        
        if args.clipboard:
            pyperclip.copy(text)
            print(f"\n📋 Copied to clipboard: {text[:60]}...")
        
        # Return JSON for CoreLink logging
        print(json.dumps({"status": "success", "text": text}))
        return 0
    except Exception as e:
        print(json.dumps({"status": "error", "error": str(e)}), file=sys.stderr)
        return 1
    finally:
        if temp_file.exists():
            temp_file.unlink()

if __name__ == "__main__":
    sys.exit(main())