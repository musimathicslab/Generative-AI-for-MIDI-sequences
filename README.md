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

Preliminary experiments using pre-trained MusicVAE models showed limitations in rhythmic consistency and harmonic coherence for the Metal genre. This project overcomes those barriers through a custom pipeline for domain-specific fine-tuning and real-time synthesis.

---

## 🎯 Project Objectives

**Key goals achieved:**
* ✅ Creation of a **specialized Metal MIDI dataset**.
* ✅ Fine-tuning MusicVAE models for genre-specific generation.
* ✅ Real-time integration through **OSC communication**.
* ✅ Development of a responsive procedural music system that manages **interactive game logic (such as card selection)**.

---

## 🚀 Installation & Usage

### 1️⃣ Environment Setup
1. Install [**Anaconda**](https://www.anaconda.com/).
2. Create a Python 3.10 virtual environment.
3. Install the required dependencies (`tensorflow`, `magenta`, etc.).

### 2️⃣ Dataset Preparation & Training
* **Split Tracks:** 👉 [`Scripts/splitter.py`](./Scripts/splitter.py)
* **Convert to TFRecord:** Use scripts for [**Guitar**](./Scripts/convert_guitar_to_tf.py), [**Bass**](./Scripts/convert_bass_to_tf.py), and [**Drums**](./Scripts/convert_drums_to_tf.py).
* **Training:** Run the dedicated training scripts for each instrument: [`train_guitar.py`](./Scripts/train_guitar.py), [`train_bass.py`](./Scripts/train_bass.py), or [`train_drums.py`](./Scripts/train_drums.py).

---

## 🎹 MIDI Generation

After training, you can generate new, original MIDI sequences:

👉 [`Scripts/generate_MIDI.py`](./Scripts/generate_MIDI.py)

**Customization:** The generation process is highly flexible. By modifying the parameters within the script, you can vary the musical output at will—adjusting **musical progressions**, structural logic, and core generation data to fit your specific needs.

---

## 🎮 Unity Integration

The system uses the **OSC (Open Sound Control)** protocol to trigger audio samples dynamically based on AI-generated data.

### 🛠️ Setup Instructions

1. **Install OSCJack:** Download and import [**OSCJack**](https://github.com/keijiro/OscJack) into Unity following the official instructions.
2. **OSCManager:** Create an empty GameObject named `OSCManager`.
3. **Player Objects:** Create 5 child GameObjects inside `OSCManager`: `GuitarPlayer`, `BassPlayer`, `KickPlayer`, `SnarePlayer`, and `HiHatPlayer`.
4. **AudioSources:** Add an `AudioSource` to each Player and assign a short (one-shot) audio sample corresponding to the instrument.
5. **MetalReceiver:** Apply the script 👉 [`Scripts/MetalReceiver.cs`](./Scripts/MetalReceiver.cs) to the `OSCManager` and link the Players in the Inspector.
6. **SoundTrackManager:** Apply the script 👉 [`Scripts/SoundTrackManager.cs`](./Scripts/SoundTrackManager.cs) within Unity. This component manages the overall soundtrack flow and handles the **card selection logic**, allowing the music to react to player choices.

### ⚡ Running the System

1. **Start the OSC Server:** Open the **Anaconda Prompt**, activate your environment, and run the server script:
   👉 [`Scripts/playbackOSC.py`](./Scripts/playbackOSC.py)
   *This script acts as the server that generates the Metal music and sends the data to Unity via OSC.*
2. **Play in Unity:** Press **Play** in the Unity Editor to listen to the generated output.
3. **Parameter Tweaking:** You can modify generation parameters, musical progressions, and other settings within the code to customize the musical results as needed.

---

## 📌 Current Status

> ⚠️ **Disclaimer:** This project is currently a **research prototype** and has not yet been released as a production-ready system.

It serves as a comprehensive proof-of-concept demonstrating:
* Genre-specialized generative AI
* Real-time procedural music systems
* Interactive AI-driven audio design

---

## 🔬 Future Work

* 📈 **Expansion** of the Metal dataset for broader stylistic coverage.
* 🔗 **Multi-instrument conditioning** for tighter band cohesion.
* 🎭 **Emotional modulation models** to drive music based on game tension.
* 🏥 **Validation in therapeutic environments** (e.g., active music therapy).
