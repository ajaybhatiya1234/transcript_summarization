import os
import torch
import torchaudio
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer
import librosa
import soundfile as sf

def segment_and_transcribe_audio(enhanced_file):
    stream = librosa.stream(
        enhanced_file,
        block_length=30,
        frame_length=16000,
        hop_length=16000
    )

    file_loc = "audio_segments"
    for i, speech in enumerate(stream):
        sf.write(f'{file_loc}/{i}.wav', speech, 16000)

    audio_path = [f'{file_loc}/{a}.wav' for a in range(i+1)]

    model_path = "model"
    tokenizer_path = "tokenizer"

    if not os.path.exists(model_path):
        model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")
        model.save_pretrained(model_path)
    else:
        model = Wav2Vec2ForCTC.from_pretrained(model_path)

    if not os.path.exists(tokenizer_path):
        tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")
        tokenizer.save_pretrained(tokenizer_path)
    else:
        tokenizer = Wav2Vec2Tokenizer.from_pretrained(tokenizer_path)

    def transcribe_audio_chunk(audio_path):
        waveform, sample_rate = torchaudio.load(audio_path)
        input_values = tokenizer(waveform[0], return_tensors="pt").input_values
        logits = model(input_values).logits
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = tokenizer.batch_decode(predicted_ids, skip_special_tokens=True)[0]
        return transcription

    transcriptions = []
    for audio_path in audio_path:
        transcription = transcribe_audio_chunk(audio_path)
        transcriptions.append(transcription)
    text = ' '.join(transcriptions)
    return text