# 🎼🤖 Generative AI for MIDI Sequences  
*A real-time procedural Metal music generation system based on fine-tuned MusicVAE models, integrated into Unity.*

![Screenshot](READMEimg/main.gif)

---

## 🛠️ Technologies Used

[![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-Deep%20Learning-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)](https://www.tensorflow.org/)
[![Magenta](https://img.shields.io/badge/Magenta-MusicVAE-8E24AA?style=for-the-badge)](https://magenta.tensorflow.org/)
[![Unity](https://img.shields.io/badge/Unity-Game%20Engine-000000?style=for-the-badge&logo=unity&logoColor=white)](https://unity.com/)
[![OSC](https://img.shields.io/badge/OSC-Open%20Sound%20Control-4CAF50?style=for-the-badge)](http://opensoundcontrol.org/)
[![Anaconda](https://img.shields.io/badge/Anaconda-Environment-44A833?style=for-the-badge&logo=anaconda&logoColor=white)](https://www.anaconda.com/)
[![MuseScore](https://img.shields.io/badge/MuseScore%20Studio-Notation%20Software-1E90FF?style=for-the-badge)](https://musescore.org/)

---

## 📖 Description

**Generative AI for MIDI Sequences** is a thesis project focused on extending the capabilities of generative music models for stylistically complex genres — specifically **Metal music** — and integrating real-time procedural generation into a Unity-based interactive environment.

Despite significant advancements in AI-based music generation, general-purpose pre-trained models often struggle when applied to highly structured and stylistically demanding genres.

Preliminary experiments using pre-trained MusicVAE models produced convincing results in Classical and Jazz domains. However, when applied to Metal, significant limitations emerged:

- Lack of rhythmic consistency  
- Weak harmonic coherence  
- Absence of genre-specific features such as complex drum patterns and fast tempo structures  

These issues were linked to the limited representation of Metal music within the original training datasets.

---

## 🎯 Project Objectives

The primary objective of this thesis was to develop a system capable of generating **dynamic and stylistically coherent Metal music in real time**, integrated within a Unity game environment.

Key goals:

- ✅ Creation of a **specialized Metal MIDI dataset**
- ✅ Fine-tuning MusicVAE models for genre-specific generation
- ✅ Real-time integration through OSC communication
- ✅ Development of a responsive procedural music system for interactive environments

---

## 🧠 Research Contribution

This project demonstrates how **targeted fine-tuning on domain-specific datasets significantly extends the expressive capabilities of generative models**, allowing them to operate effectively in stylistically complex domains.

The final result is a **functional prototype** in which procedural generation dynamically responds to user interaction inside a game environment.

---

## 🚀 Installation

### 1️⃣ Environment Setup

- Install **Anaconda**
- Create a Python 3.10 virtual environment
- Install:
  - TensorFlow
  - Magenta
  - Required dependencies

> ⚠️ Note: Magenta and TensorFlow require careful dependency management. Python 3.10 is required for compatibility.

---

### 2️⃣ Dataset Preparation

- Download Metal MIDI files (e.g., Metal genre corpus)
- Place them inside your dataset directory.

To separate instrumental tracks (Guitar, Bass, Drums), use:

Scripts/splitter.py

This script isolates individual instrument tracks from the original MIDI files.

### 3️⃣ TFRecord Conversion

After splitting the tracks, convert each instrument dataset into TFRecord format using:

Scripts/convert_guitar_to_tf.py

Scripts/convert_bass_to_tf.py

Scripts/convert_drums_to_tf.py

These scripts prepare the data in a format compatible with MusicVAE training.

---

### 4️⃣ Model Fine-Tuning

The following pre-trained MusicVAE models were fine-tuned:

🎸 Guitar → cat-mel_2bar_big

🎸 Bass → cat-mel_2bar_med_chords

🥁 Drums → cat-drums_2bar_small

To start training:

Scripts/train_guitar.py

Scripts/train_bass.py

Scripts/train_drums.py

Training parameters such as:

Number of training steps ;
Batch size ; 
Checkpoint intervals ; can be configured directly inside each training script.

---

## MIDI Generation
After training, generate new MIDI sequences using:

Scripts/generate_MIDI.py

---

## Musical Validation
Generated MIDI files were imported into MuseScore Studio for:

Score visualization, Structural validation, Auditory evaluation,

This step allowed musical inspection and refinement of the generated sequences.

---

## 🎮 Unity Integration

Once trained, the system was adapted for real-time use inside Unity.

Instead of directly streaming MIDI:

- Musical data is transmitted via **OSC (Open Sound Control)**
- Unity receives generation parameters in real time
- Short adaptive audio samples are triggered dynamically
- Audio behavior changes according to AI-generated musical structures

This architecture allows procedural music to respond directly to gameplay events.

---

## 📌 Current Status

⚠️ This project is currently a **research prototype** and has not yet been released as a production-ready system.

It serves as a proof-of-concept demonstrating:

- Genre-specialized generative AI
- Real-time procedural music systems
- Interactive AI-driven audio design

---

## 🔬 Future Work

- Expansion of the Metal dataset
- Multi-instrument conditioning
- Emotional modulation models
- Validation in therapeutic environments
