
# 🤖 KinyaVoice 

An intelligent voice assistant that understands and speaks **Kinyarwanda**, developed as part of the **Intelligent Robotics** course. It combines advanced speech recognition, contextual understanding, and natural language response generation to enable real-time human-computer interaction in Kinyarwanda.

![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/Python-3.12-blue)

---

## 🎥 Interface Demo

A web-based interactive demo is included using **Gradio**. Launch the app locally and interact with it through your browser.

---

## 🌟 Features

- 🎙️ **Kinyarwanda ASR** powered by [`KinyaWhisper`](https://huggingface.co/benax-rw/KinyaWhisper) (optimized for 16kHz audio)  
- 🧠 **Contextual Understanding** using fuzzy logic matching  
- 📢 **Natural Language Responses** with Kinyarwanda Text-to-Speech (TTS)  
- 🔇 **Noise Reduction** with advanced audio cleaning  
- 🎚️ **Voice Activity Detection (VAD)** for precise speech segmentation  
- 🔄 **Repetition Filters** for clean, intelligible transcription  
- 📊 **Conversation Analytics** with question matching insights  
- 🌐 **Web Interface** via Gradio for user-friendly interaction  

---

## 🛠️ Tech Stack

| 🧩 Layer             | 🛠️ Tools Used                        |
|---------------------|--------------------------------------|
| Core AI             | Hugging Face Transformers            |
| Audio Processing    | Librosa, Soundfile, WebRTC VAD       |
| NLP Matching        | FuzzyWuzzy, Python-Levenshtein       |
| Voice Interface     | Gradio                               |
| Optimization        | Noisereduce, FFmpeg                  |

---

## 💻 Installation

### ✅ Prerequisites

- Python 3.12  
- FFmpeg

Install FFmpeg:

```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Windows (via Chocolatey)
choco install ffmpeg
```

---

### 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/Chiesa14/KinyarwandaVoiceAssistant.git
cd KinyarwandaVoiceAssistant

# Set up virtual environment
python -m venv .venv

# Activate virtual environment
.\.venv\Scriptsctivate      # Windows
# or
source .venv/bin/activate     # Linux/macOS

# Install dependencies
pip install -r requirements.txt
```

---

### ⚙️ Configuration

Edit the `nlp_mapping.json` file to define custom question–answer pairs:

```json
{
  "qa_pairs": [
    {
      "question": "Mwiriwe neza?",
      "answer": "Mwiriwe neza cyane ! Mwebwe mumeze mute??"
    },
    {
      "question": "Amazina yawe ni ayahe?",
      "answer": "Nitwa KinyaWhisper."
    },
    {
      "question": "Ninde wagukoze se?",
      "answer": "Nakozwe na Nathan Nduwayo."
    },
    {
      "question": "Ufite imyaka ingahe?",
      "answer": "Nta myaka mfite, ndi porogaramu ya mudasobwa."
    },
    {
      "question": "Uzi ikinyarwanda neza?",
      "answer": "Yego, !"
    },
    {
      "question": "Umeze neza?",
      "answer": "Yego! Turashima Imana."
    },
    {
      "question": "Rwanda Coding Academy iherereye he?",
      "answer": "Iherereye mu Karere ka Nyabihu, mu Ntara y’Iburengerazuba."
    }
  ],
  "default_response": "Mwihangane! Muhindure ikibazo"
}
```

---

### 🗂️ Audio Files

Use the `/sample_inputs` folder to test with existing audio clips.  

**Supported formats:** `.wav`, `.mp3`, `.ogg`

---

### 🧪 Usage

Start the App:

```bash
python main.py
```

Access the Interface:  
👉 Open your browser and navigate to: [http://localhost:7860](http://localhost:7860)

---

## 💡 Interface Guide

1. 🎤 Record your voice or upload a Kinyarwanda audio file.  
2. 📨 Click **Submit** to process the input (~10–60 seconds).  
3. 🔊 The system will auto-play the Kinyarwanda response.  
4. 📜 Review the transcription and matched response.  
5. 🧹 Use **Clear** to reset the session.

---

## 🗣️ Example Interactions

| Raw Transcription | Matched Question                  | System Response                                                        |
|-------------------|-----------------------------------|------------------------------------------------------------------------|
| mizeneza          | Umeze neza?                       | Yego! Turashima Imana.                                                |
| wakorewee heheh   | Wakorewe hehe?                    | Nakorewe muri Rwanda Coding Academy, nakozwe na Nathan Nduwayo.      |
| mwiriwe neza      | Mwiriwe neza?                     | Mwiriwe neza cyane ! Mwebwe mumeze mute??                             |
| amazina           | Amazina yawe ni ayahe?            | Nitwa KinyaWhisper.                                                   |
| ninde wakoze      | Ninde wagukoze se?                | Nakozwe na Nathan Nduwayo.                                            |
| ufite imyaka      | Ufite imyaka ingahe?              | Nta myaka mfite, ndi porogaramu ya mudasobwa.                         |
| ikinyarwanda      | Uzi ikinyarwanda neza?            | Yego, !                                                                |
| academy iherereye | Rwanda Coding Academy ...         | Iherereye mu Karere ka Nyabihu, mu Ntara y’Iburengerazuba.           |

---

## 🔐 Accessing Gated Model

This project uses a **private model** on Hugging Face: [`benax-rw/KinyaWhisper`](https://huggingface.co/benax-rw/KinyaWhisper)

⚠️ **You must request and be granted access** on Hugging Face and then log in via CLI:

```bash
huggingface-cli login
```

---

## 👤 Author

**Nathan Nduwayo**  
📍 Rwanda Coding Academy  
💬 Passionate about intelligent systems for African languages

---

## 🙌 Acknowledgments

Special thanks to **Hugging Face** and the open-source community supporting NLP in underrepresented languages.
