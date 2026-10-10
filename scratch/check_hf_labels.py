import os
import sys
sys.path.append(os.path.abspath("."))
from audio_utils import load_audio_file
from model_detector import get_huggingface_pipeline

pipeline_obj = get_huggingface_pipeline()
print("HF Pipeline object:", pipeline_obj)

for s in ["samples/sample_authentic_human.wav", "samples/sample_ai_clone_scam.wav"]:
    data, sr = load_audio_file(s)
    preds = pipeline_obj({"array": data, "sampling_rate": sr})
    print(f"\n[FILE]: {s}")
    print("Raw HF Predictions:", preds)
