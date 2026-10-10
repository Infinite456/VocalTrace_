import os
import sys

# Detect if running under Streamlit runner
def is_running_streamlit():
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        return get_script_run_ctx() is not None
    except Exception:
        return "streamlit" in sys.modules or any("streamlit" in arg for arg in sys.argv)

if is_running_streamlit():
    import io
    import time
    import json
    import streamlit as st
    import numpy as np
    from backend.audio_utils import load_audio_file, generate_cyber_plots
    from backend.model_detector import run_deepfake_analysis

    st.set_page_config(
        page_title="VocalTrace - AI Voice Scam & Deepfake Detector",
        page_icon="🛡️",
        layout="wide"
    )

    st.markdown("""
    <style>
        .stApp { background-color: #0d1117; color: #c9d1d9; }
        .header-box { background: linear-gradient(135deg, #161b22 0%, #0d1117 100%); border: 1px solid #30363d; border-radius: 12px; padding: 24px; margin-bottom: 24px; }
        .header-title { font-size: 2.2rem; font-weight: 800; background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .cyber-card { background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 20px; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.title("VocalTrace Console")
        st.caption("Cybersecurity Intelligence Hub")
        st.markdown("---")

    st.markdown("""
    <div class="header-box">
        <div class="header-title">VocalTrace: Real-Time Synthetic Audio & Voice Scam Detector</div>
        <div style="color:#8b949e;">Deepfake forensics and acoustic artifact analysis to combat AI voice-impersonation fraud.</div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📤 Upload Audio File", "🎙️ Record Live Audio", "🌐 Media URL & Web Payload Scanner"])

    with tab1:
        uploaded_file = st.file_uploader("Upload Audio Clip (.wav, .mp3)", type=["wav", "mp3", "ogg", "flac"])
        if uploaded_file is not None:
            st.session_state.current_audio = uploaded_file.read()
            st.session_state.current_filename = uploaded_file.name

    with tab2:
        st.markdown("##### 🎙️ Microphone Live Voice Recorder")
        st.caption("Record your voice live for deepfake & synthetic voice authentication.")
        recorded_audio = st.audio_input("Record live voice clip from microphone")
        if recorded_audio is not None:
            st.session_state.current_audio = recorded_audio.read()
            st.session_state.current_filename = "live_microphone_recording.wav"

    with tab3:
        media_url = st.text_input("Hosted Media URL or Embedded Payload", placeholder="https://cdn.example.com/audio.wav or <audio src='data:audio/wav;base64,...'>")
        if st.button("⚡ Scan Media URL & Payload"):
            if media_url:
                try:
                    from backend.app import fetch_media_from_url_or_payload
                    audio_bytes, filename, content_type, domain = fetch_media_from_url_or_payload(media_url)
                    st.session_state.current_audio = audio_bytes
                    st.session_state.current_filename = filename
                    st.success(f"Fetched media stream from {domain} ({content_type})")
                except Exception as e:
                    st.error(f"Failed to fetch media URL: {e}")

    if getattr(st.session_state, "current_audio", None) is not None:
        audio_bytes = st.session_state.current_audio
        filename = st.session_state.current_filename or "audio.wav"

        # Acoustic Normalization Pipeline: Resample to 16kHz mono, trim silence, normalize amplitude
        audio_data, sr = load_audio_file(io.BytesIO(audio_bytes), target_sr=16000, normalize=True)
        results = run_deepfake_analysis(audio_data, sr, filename=filename)

        st.markdown("---")
        st.caption("✨ Acoustic Normalization Pipeline Applied: 16,000 Hz Mono • Amplitude Normalized (librosa.util.normalize) • Silence Trimmed (librosa.effects.trim)")

        st.subheader("🔊 Forensic Spectrum Analysis")
        st.audio(audio_bytes, format="audio/wav")
        fig = generate_cyber_plots(audio_data, sr)
        st.pyplot(fig)

        if results["is_synthetic"]:
            st.error(f"⚠️ {results['verdict_title']} (Confidence: {results['confidence_pct']}%)")
        else:
            st.success(f"✅ {results['verdict_title']} (Confidence: {results['confidence_pct']}%)")
        st.info(results["advisory_text"])

else:
    # Flask REST API & Web Server Runner
    from backend.app import app
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Starting VocalTrace Web Server at http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)
