import os
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.append(os.path.abspath("."))

from audio_utils import load_audio_file
from model_detector import run_deepfake_analysis

print("--- TESTING VOCALTRACE DEEPFAKE ANALYSIS PIPELINE ---")

samples = [
    "samples/sample_authentic_human.wav",
    "samples/sample_ai_clone_scam.wav",
    "samples/sample_grandparent_scam.wav"
]

for s in samples:
    if os.path.exists(s):
        print(f"\n[FILE]: {s}")
        data, sr = load_audio_file(s)
        res = run_deepfake_analysis(data, sr, filename=os.path.basename(s))
        print(f"Verdict: {res['verdict_title']}")
        print(f"Synthetic Probability: {int(res['synthetic_prob']*100)}%")
        print(f"Risk Index: {res['scam_risk_index']}")
    else:
        print(f"Sample missing: {s}")

print("\n--- ALL TESTS COMPLETED SUCCESSFULLY ---")
