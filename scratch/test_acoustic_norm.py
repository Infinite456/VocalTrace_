import io
import wave
import numpy as np
import soundfile as sf
import librosa
from backend.audio_utils import preprocess_acoustic_buffer, load_audio_file
from backend.model_detector import run_deepfake_analysis

def test_acoustic_normalization_pipeline():
    print("=== Testing Acoustic Normalization Pipeline ===")

    # 1. Create a simulated live microphone recording (48,000 Hz stereo with initial room silence & noise)
    sr_raw = 48000
    duration_sec = 4
    t = np.linspace(0, duration_sec, sr_raw * duration_sec)
    
    # 0.5s initial room silence + 3.0s voice signal + 0.5s ending silence
    silence_initial = np.zeros(int(0.5 * sr_raw), dtype=np.float32)
    voice_signal = 0.05 * np.sin(2 * np.pi * 440 * t[:int(3.0 * sr_raw)]).astype(np.float32) # Quiet voice note
    room_noise = np.random.normal(0, 0.002, len(t)).astype(np.float32)
    
    raw_recording = np.concatenate([silence_initial, voice_signal, np.zeros(int(0.5 * sr_raw), dtype=np.float32)]) + room_noise
    stereo_recording = np.vstack([raw_recording, raw_recording]).T

    # Save to BytesIO buffer
    buf = io.BytesIO()
    sf.write(buf, stereo_recording, sr_raw, format='WAV')
    buf.seek(0)

    print(f"Raw Microphone Buffer: {len(raw_recording)} samples @ {sr_raw} Hz (Stereo)")

    # 2. Run preprocess_acoustic_buffer
    norm_audio, sr_out = preprocess_acoustic_buffer(buf, target_sr=16000)

    print(f"Preprocessed Buffer: {len(norm_audio)} samples @ {sr_out} Hz (Mono)")
    print(f"Peak Amplitude after librosa.util.normalize: {np.max(np.abs(norm_audio)):.4f}")

    # Check assertions
    assert sr_out == 16000, f"Expected 16000 Hz sample rate, got {sr_out}"
    assert np.max(np.abs(norm_audio)) <= 1.0, "Amplitude exceeding 1.0 threshold"
    assert len(norm_audio) < len(raw_recording) * (16000 / sr_raw), "Silence was not trimmed by librosa.effects.trim"

    # 3. Test analysis with normalized audio
    analysis_res = run_deepfake_analysis(norm_audio, sr_out, filename="live_mic_recording.wav")
    verdict = analysis_res["verdict_title"].encode("ascii", "ignore").decode("ascii")
    print("Analysis Verdict:", verdict)
    print("Confidence:", analysis_res["confidence_pct"], "%")

    print("=== All Acoustic Normalization Tests Passed! ===")

if __name__ == "__main__":
    test_acoustic_normalization_pipeline()
