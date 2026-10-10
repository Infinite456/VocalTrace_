import os
import io
import wave
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def preprocess_acoustic_buffer(audio_source, target_sr=16000):
    """
    Acoustic normalization pipeline for live microphone recordings & audio clips:
    1. Resample recorded buffer strictly to 16,000 Hz mono (via librosa.load).
    2. Trim silent / background room noise segments (via librosa.effects.trim).
    3. Normalize peak signal amplitude to [-1.0, 1.0] (via librosa.util.normalize).
    Returns (normalized_numpy_mono_array, 16000).
    """
    import librosa

    if hasattr(audio_source, "seek"):
        audio_source.seek(0)

    try:
        # 1. Resample strictly to 16,000 Hz mono
        data, sr = librosa.load(audio_source, sr=target_sr, mono=True)
    except Exception as e:
        data, sr = _raw_load_audio_file(audio_source)
        if sr != target_sr:
            data = librosa.resample(data, orig_sr=sr, target_sr=target_sr)
            sr = target_sr

    if len(data) == 0:
        return np.zeros(target_sr, dtype=np.float32), target_sr

    # 2. Trim silent segments with librosa.effects.trim
    try:
        data_trimmed, _ = librosa.effects.trim(data, top_db=25)
        if len(data_trimmed) > 0:
            data = data_trimmed
    except Exception:
        pass

    # 3. Normalize amplitude using librosa.util.normalize
    try:
        data_normalized = librosa.util.normalize(data)
    except Exception:
        max_val = np.max(np.abs(data)) + 1e-9
        data_normalized = data / max_val

    return data_normalized.astype(np.float32), target_sr

def _raw_load_audio_file(audio_source):
    if isinstance(audio_source, (str, os.PathLike)):
        filepath = audio_source
        try:
            import soundfile as sf
            data, sr = sf.read(filepath)
            if data.ndim > 1:
                data = np.mean(data, axis=1)
            return data.astype(np.float32), sr
        except Exception:
            with wave.open(filepath, 'rb') as wf:
                sr = wf.getframerate()
                n_frames = wf.getnframes()
                frames = wf.readframes(n_frames)
                data = np.frombuffer(frames, dtype=np.int16).astype(np.float32) / 32768.0
                return data, sr

    elif hasattr(audio_source, "read"):
        audio_source.seek(0)
        file_bytes = audio_source.read()
        audio_source.seek(0)
        
        try:
            import soundfile as sf
            bio = io.BytesIO(file_bytes)
            data, sr = sf.read(bio)
            if data.ndim > 1:
                data = np.mean(data, axis=1)
            return data.astype(np.float32), sr
        except Exception:
            try:
                bio = io.BytesIO(file_bytes)
                with wave.open(bio, 'rb') as wf:
                    sr = wf.getframerate()
                    n_frames = wf.getnframes()
                    frames = wf.readframes(n_frames)
                    data = np.frombuffer(frames, dtype=np.int16).astype(np.float32) / 32768.0
                    return data, sr
            except Exception as e:
                raise ValueError(f"Could not decode audio file: {e}")
    else:
        raise TypeError("Unsupported audio source type.")

def load_audio_file(audio_source, target_sr=16000, normalize=True):
    """
    Loads audio data from file path, BytesIO, or uploaded buffer.
    By default performs 16kHz resampling, silence trimming, and amplitude normalization.
    """
    if normalize:
        try:
            return preprocess_acoustic_buffer(audio_source, target_sr=target_sr)
        except Exception as e:
            print(f"Warning: librosa acoustic preprocessing fallback: {e}")
    return _raw_load_audio_file(audio_source)


def generate_cyber_plots(data, sr):
    """
    Renders dual interactive cybersecurity forensic plots:
    1. Acoustic Waveform (Amplitude vs Time) with cyan glowing aesthetics
    2. Spectrogram Heatmap (Frequency vs Time) illustrating vocoder brickwall cutoffs
    """
    plt.style.use('dark_background')
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 5.5), gridspec_kw={'height_ratios': [1, 1.3]})
    fig.patch.set_facecolor('#0d1117')
    ax1.set_facecolor('#161b22')
    ax2.set_facecolor('#161b22')

    num_samples = len(data)
    duration = num_samples / float(sr)
    time_axis = np.linspace(0, duration, num_samples)

    # 1. Waveform Plot
    ax1.plot(time_axis, data, color='#00f2fe', linewidth=0.8, alpha=0.9, label='Amplitude')
    ax1.fill_between(time_axis, data, 0, color='#00f2fe', alpha=0.15)
    ax1.set_title('Forensic Acoustic Waveform (Amplitude vs. Time)', color='#f0f6fc', fontsize=11, fontweight='bold', pad=8)
    ax1.set_ylabel('Amplitude', color='#8b949e', fontsize=9)
    ax1.set_xlim(0, duration)
    ax1.set_ylim(-1.0, 1.0)
    ax1.grid(True, color='#30363d', linestyle='--', alpha=0.5)
    ax1.tick_params(colors='#8b949e', labelsize=8)

    # 2. Spectrogram Plot
    nperseg = min(512, len(data))
    noverlap = nperseg // 2
    step = nperseg - noverlap
    shape = ((len(data) - nperseg) // step + 1, nperseg)
    strides = (data.strides[0] * step, data.strides[0])
    try:
        frames = np.lib.stride_tricks.as_strided(data, shape=shape, strides=strides)
    except Exception:
        frames = np.array([data[i:i+nperseg] for i in range(0, len(data)-nperseg+1, step)])

    window = np.hanning(nperseg)
    windowed_frames = frames * window
    fft_vals = np.abs(np.fft.rfft(windowed_frames, axis=1))
    spectrogram_db = 20 * np.log10(fft_vals + 1e-6)
    
    freq_bins = np.fft.rfftfreq(nperseg, 1.0 / sr)
    spec_duration = (len(frames) * step) / sr
    
    im = ax2.imshow(
        spectrogram_db.T,
        aspect='auto',
        origin='lower',
        extent=[0, spec_duration, freq_bins[0], freq_bins[-1]],
        cmap='magma',
        vmin=np.max(spectrogram_db) - 60,
        vmax=np.max(spectrogram_db)
    )
    
    ax2.set_title('High-Resolution Spectral Intensity & Neural Vocoder Artifact Analysis', color='#f0f6fc', fontsize=11, fontweight='bold', pad=8)
    ax2.set_xlabel('Time (seconds)', color='#8b949e', fontsize=9)
    ax2.set_ylabel('Frequency (Hz)', color='#8b949e', fontsize=9)
    ax2.grid(True, color='#30363d', linestyle=':', alpha=0.4)
    ax2.tick_params(colors='#8b949e', labelsize=8)
    
    if sr >= 16000:
        ax2.axhline(y=7800, color='#ff4b4b', linestyle='--', linewidth=1, label='Vocoder Cutoff Threshold (7.8kHz)')
        ax2.legend(loc='upper right', facecolor='#161b22', edgecolor='#30363d', fontsize=8, labelcolor='#f0f6fc')

    cbar = fig.colorbar(im, ax=ax2, orientation='horizontal', pad=0.25, shrink=0.7)
    cbar.set_label('Spectral Density (dB)', color='#8b949e', fontsize=8)
    cbar.ax.tick_params(labelsize=7, colors='#8b949e')

    plt.tight_layout()
    return fig

def extract_acoustic_forensic_metrics(data, sr):
    """
    Extracts acoustic forensic indicators used for AI voice synthesis detection.
    """
    fft_spectrum = np.abs(np.fft.rfft(data))
    freqs = np.fft.rfftfreq(len(data), 1.0 / sr)
    
    total_energy = np.sum(fft_spectrum**2) + 1e-9
    high_freq_mask = freqs > (0.4 * sr)
    high_freq_energy = np.sum(fft_spectrum[high_freq_mask]**2)
    hf_ratio = float(high_freq_energy / total_energy)

    frame_len = int(0.025 * sr)
    hop_len = int(0.010 * sr)
    num_frames = (len(data) - frame_len) // hop_len
    
    zcrs = []
    energies = []
    for i in range(max(1, num_frames)):
        frame = data[i*hop_len : i*hop_len + frame_len]
        zcr = np.mean(np.abs(np.diff(np.sign(frame)))) / 2.0
        energy = np.sum(frame**2)
        zcrs.append(zcr)
        energies.append(energy)
        
    zcr_std = float(np.std(zcrs)) if zcrs else 0.05
    energy_std = float(np.std(energies)) if energies else 0.1

    energies = np.array(energies) if energies else np.array([0.01])
    min_energy = np.min(energies[energies > 0]) if np.any(energies > 0) else 1e-6
    max_energy = np.max(energies) + 1e-6
    dynamic_range_db = float(10 * np.log10(max_energy / min_energy))

    phase_spectrum = np.angle(np.fft.rfft(data))
    phase_diff = np.diff(phase_spectrum)
    phase_variance = float(np.var(phase_diff))

    return {
        "hf_ratio": hf_ratio,
        "zcr_std": zcr_std,
        "energy_std": energy_std,
        "dynamic_range_db": dynamic_range_db,
        "phase_variance": phase_variance
    }
