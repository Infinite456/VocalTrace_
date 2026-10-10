import os
import math
import struct
import wave
import random

def generate_authentic_human_wav(filename="samples/sample_authentic_human.wav", duration_sec=4.5, sample_rate=16000):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    num_samples = int(duration_sec * sample_rate)
    samples = []
    
    for i in range(num_samples):
        t = i / sample_rate
        envelope = 0.5 * (1.0 + math.sin(2 * math.pi * 1.5 * t)) * (0.8 + 0.2 * math.sin(2 * math.pi * 0.4 * t))
        if 1.2 < t < 1.6 or 3.1 < t < 3.4:
            envelope *= 0.05
            
        f0 = 130.0 + 15.0 * math.sin(2 * math.pi * 0.8 * t) + random.uniform(-1.5, 1.5)
        
        vocal = (
            0.6 * math.sin(2 * math.pi * f0 * t) +
            0.35 * math.sin(2 * math.pi * (2 * f0) * t + 0.2) +
            0.25 * math.sin(2 * math.pi * (3 * f0) * t + 0.5) +
            0.15 * math.sin(2 * math.pi * (500.0) * t) +
            0.10 * math.sin(2 * math.pi * (1500.0) * t) +
            0.05 * math.sin(2 * math.pi * (2500.0) * t)
        )
        
        room_noise = random.gauss(0, 0.012)
        signal = (vocal * envelope) + room_noise
        signal = max(-0.95, min(0.95, signal))
        sample_int = int(signal * 32767)
        samples.append(sample_int)
        
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        packed_bytes = struct.pack(f'<{len(samples)}h', *samples)
        wav_file.writeframes(packed_bytes)

def generate_ai_clone_wav(filename="samples/sample_ai_clone_scam.wav", duration_sec=4.5, sample_rate=16000):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    num_samples = int(duration_sec * sample_rate)
    samples = []
    
    for i in range(num_samples):
        t = i / sample_rate
        if 1.0 < t < 1.4 or 2.8 < t < 3.2:
            envelope = 0.0001
        else:
            envelope = 0.85
            
        f0 = 145.0
        vocoder_buzz = (
            0.7 * math.sin(2 * math.pi * f0 * t) +
            0.5 * math.sin(2 * math.pi * 2 * f0 * t + 1.57) +
            0.4 * math.sin(2 * math.pi * 3 * f0 * t + 3.14) +
            0.3 * math.sin(2 * math.pi * 4 * f0 * t + 4.71) +
            0.25 * math.sin(2 * math.pi * 5 * f0 * t) +
            0.20 * math.sin(2 * math.pi * 6 * f0 * t) +
            0.15 * math.sin(2 * math.pi * 7 * f0 * t)
        )
        
        metallic_artifact = 0.08 * math.sin(2 * math.pi * 7800.0 * t + (i % 7))
        signal = (vocoder_buzz * envelope) + metallic_artifact
        signal = max(-0.95, min(0.95, signal))
        sample_int = int(signal * 32767)
        samples.append(sample_int)
        
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        packed_bytes = struct.pack(f'<{len(samples)}h', *samples)
        wav_file.writeframes(packed_bytes)

def generate_grandparent_scam_wav(filename="samples/sample_grandparent_scam.wav", duration_sec=5.0, sample_rate=16000):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    num_samples = int(duration_sec * sample_rate)
    samples = []
    
    for i in range(num_samples):
        t = i / sample_rate
        envelope = 0.8 * (0.5 + 0.5 * math.sin(2 * math.pi * 2.2 * t))
        if 2.0 < t < 2.5:
            envelope = 0.0
            
        f0 = 160.0
        synth_voice = (
            0.7 * math.sin(2 * math.pi * f0 * t) +
            0.4 * math.sin(2 * math.pi * 2.1 * f0 * t) +
            0.3 * math.sin(2 * math.pi * 3.9 * f0 * t) +
            0.15 * math.sin(2 * math.pi * 6500.0 * t + (i % 11))
        )
        signal = synth_voice * envelope
        signal = max(-0.95, min(0.95, signal))
        sample_int = int(signal * 32767)
        samples.append(sample_int)
        
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        packed_bytes = struct.pack(f'<{len(samples)}h', *samples)
        wav_file.writeframes(packed_bytes)

def generate_all_samples():
    generate_authentic_human_wav()
    generate_ai_clone_wav()
    generate_grandparent_scam_wav()

if __name__ == "__main__":
    generate_all_samples()
