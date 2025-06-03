import librosa
import torch
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC

def transcribe_audio(audio_path):
    array, sampling_rate = librosa.load(audio_path, sr=16000)
    processor = Wav2Vec2Processor.from_pretrained("aman-batazia/Swahili_xlsr")
    model = Wav2Vec2ForCTC.from_pretrained("aman-batazia/Swahili_xlsr")

    input_values = processor(array, return_tensors="pt", padding="longest").input_values
    logits = model(input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.batch_decode(predicted_ids)

    return transcription[0]

