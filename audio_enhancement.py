from pydub import AudioSegment
from pydub.silence import detect_nonsilent

def process_audio(audio_file):
    # Load the audio file
    audio = AudioSegment.from_wav(audio_file)

    # Voice Activity Detection (VAD) to remove non-speech parts
    def vad(audio_segment):
        non_silent = detect_nonsilent(audio_segment, min_silence_len=1000, silence_thresh=-40)
        segments = [audio_segment[start:end] for start, end in non_silent]
        return sum(segments)

    # Apply VAD to extract speech segments
    speech_only = vad(audio)

    # Adjust volume/loudness, apply equalization, and reduce noise
    adjusted_audio = speech_only + 10  # Increase volume by 10 dB
    adjusted_audio = adjusted_audio.low_pass_filter(100)  # Apply low-pass filter with cutoff frequency of 1000 Hz
    adjusted_audio = adjusted_audio.high_pass_filter(10000)  # Reduce 10 dB from all frequencies

    processed_audio = "adjusted_audio.wav"
    adjusted_audio.export(processed_audio, format="wav")
    return processed_audio