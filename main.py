import json
import re
import os
import time
import gradio as gr
import numpy as np
import librosa
import soundfile as sf
from gtts import gTTS
import torch
import webrtcvad
import noisereduce as nr
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from fuzzywuzzy import fuzz

# Create folders for inputs/outputs
os.makedirs("audio_inputs", exist_ok=True)
os.makedirs("audio_outputs", exist_ok=True)

# Load model and processor
processor = WhisperProcessor.from_pretrained("benax-rw/KinyaWhisper")
model = WhisperForConditionalGeneration.from_pretrained("benax-rw/KinyaWhisper")


def transcribe_audio(audio_path):
    try:
        audio_data, _ = librosa.load(audio_path, sr=16000)

        if len(audio_data.shape) > 1:
            audio_data = np.mean(audio_data, axis=1)

        # Reduce noise and normalize volume
        audio_data = nr.reduce_noise(y=audio_data, sr=16000, stationary=True)
        audio_data = librosa.util.normalize(audio_data) * 0.9

        # Voice Activity Detection (VAD)
        try:
            vad = webrtcvad.Vad(1)
            frame_duration = 30  # milliseconds
            frame_length = int(16000 * frame_duration / 1000)
            frames = librosa.util.frame(audio_data, frame_length=frame_length, hop_length=frame_length)

            speech_frames = [
                frame for frame in frames.T
                if vad.is_speech(frame.astype(np.int16).tobytes(), 16000)
            ]

            if speech_frames:
                audio_data = np.concatenate(speech_frames)
            else:
                print("No speech detected; using original audio")

        except Exception as vad_err:
            print(f"VAD error: {vad_err} – fallback to original audio")

        inputs = processor(audio_data, sampling_rate=16000, return_tensors="pt")

        predicted_ids = model.generate(
            inputs.input_features,
            num_beams=5,
            repetition_penalty=1.5,
            temperature=0.8,
            max_length=448,
            no_repeat_ngram_size=2,
            early_stopping=True
        )

        transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
        transcription = re.sub(r'(\w)\1{2,}', r'\1', transcription)
        transcription = re.sub(r'\b(\w+)( \1\b)+', r'\1', transcription)

        return transcription.strip()

    except Exception as e:
        print(f"Transcription error: {e}")
        return ""


# Load QA data
with open("nlp_mapping.json") as f:
    qa_data = json.load(f)
    qa_pairs = {pair["question"]: pair["answer"] for pair in qa_data.get("qa_pairs", [])}
    default_response = qa_data.get("default_response", "I'm sorry, I don't understand.")


def normalize(text):
    return re.sub(r'[^\w\s]', '', text.lower()).strip()


def get_answer(question):
    normalized_question = normalize(question)
    best_score = 0
    best_answer = default_response
    matched_key = None

    for key in qa_pairs:
        score = fuzz.ratio(normalize(key), normalized_question)
        if score > best_score and score > 70:
            best_score = score
            best_answer = qa_pairs[key]
            matched_key = key

    return best_answer, matched_key


def process_audio(audio_path):
    timestamp = str(int(time.time()))
    input_path = f"audio_inputs/input_{timestamp}.wav"
    output_path = f"audio_outputs/output_{timestamp}.mp3"

    try:
        audio_data, _ = librosa.load(audio_path, sr=16000)
        sf.write(input_path, audio_data, 16000, subtype='PCM_16')

        question = transcribe_audio(input_path)
        answer, matched_key = get_answer(question)

        tts = gTTS(text=answer, lang="en", slow=False)
        tts.save(output_path)

        return question, answer, matched_key, output_path
    except Exception as e:
        print(f"Processing error: {e}")
        return "Error during processing", default_response, None, None


def create_qa_reference():
    lines = ["**Supported Questions and Answers:**", f"Default Response: {default_response}\n"]
    for i, (q, a) in enumerate(qa_pairs.items(), 1):
        lines.append(f"{i}. **Question**: {q}")
        lines.append(f"   **Answer**: {a}\n")
    return "\n".join(lines)


# Gradio UI
with gr.Blocks(title="Kinyarwanda Voice Assistant") as demo:
    gr.Markdown("# 🤖 Kinyarwanda Voice Assistant")
    gr.Markdown("Record or upload audio in Kinyarwanda to interact with the assistant.")

    with gr.Accordion("📚 Click to see supported questions and answers", open=False):
        gr.Markdown(create_qa_reference())

    with gr.Row():
        audio_input = gr.Audio(
            label="Speak or Upload Audio",
            sources=["microphone", "upload"],
            type="filepath",
            format="wav"
        )
        output_audio = gr.Audio(label="Response Audio", autoplay=True)

    text_outputs = gr.Textbox(label="Conversation History", lines=4)

    with gr.Row():
        submit_btn = gr.Button("Submit", variant="primary")
        clear_btn = gr.Button("Clear")

    def process_and_display(audio_path):
        if not audio_path:
            raise gr.Error("Please provide an audio file first.")

        question, answer, matched_key, output_path = process_audio(audio_path)
        display_text = f"""
🎤 **Transcription**: {question}
🔍 **Matched**: {matched_key if matched_key else "No close match found"}
🤖 **Response**: {answer}
        """.strip()

        return {output_audio: output_path, text_outputs: display_text}

    submit_btn.click(fn=process_and_display, inputs=audio_input, outputs=[output_audio, text_outputs])
    clear_btn.click(fn=lambda: [None, None, ""], outputs=[audio_input, output_audio, text_outputs])

if __name__ == "__main__":
    demo.launch(server_port=7860, share=True)
