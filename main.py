#@ab
import data_collection
import audio_enhancement
import transcribe
import text_preprocessing
import summarize

audio_file = data_collection.load_data()
enh_audio_path = audio_enhancement.process_audio(audio_file)
text = transcribe.segment_and_transcribe_audio(enh_audio_path)
print("Generated Text :", text)
corrected_text = text_preprocessing.correct_spelling(text)
sentences = text_preprocessing.tokenize_sentences(corrected_text)
preprocessed_text = text_preprocessing.preprocess_text(corrected_text)
result = summarize.summary(preprocessed_text)
print("Generated Summary :", result)
