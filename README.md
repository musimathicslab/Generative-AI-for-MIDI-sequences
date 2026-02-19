# 🎼🤖 Generative AI for MIDI Sequences  
*A real-time procedural Metal music generation system based on fine-tuned MusicVAE models, integrated into Unity.*

![Screenshot](READMEimg/main.gif)

---

## 🛠️ Technologies Used

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-Deep%20Learning-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)](https://www.tensorflow.org/)
[![Magenta](https://img.shields.io/badge/Magenta-MusicVAE-8E24AA?style=for-the-badge)](https://magenta.tensorflow.org/)
[![Unity](https://img.shields.io/badge/Unity-Game%20Engine-000000?style=for-the-badge&logo=unity&logoColor=white)](https://unity.com/)
[![OSC](https://img.shields.io/badge/OSC-Open%20Sound%20Control-4CAF50?style=for-the-badge)](http://opensoundcontrol.org/)
[![Anaconda](https://img.shields.io/badge/Anaconda-Environment-44A833?style=for-the-badge&logo=anaconda&logoColor=white)](https://www.anaconda.com/)

---

## 📖 Description

**Generative AI for MIDI Sequences** is a thesis project focused on extending the capabilities of generative music models for stylistically complex genres — specifically **Metal music** — and integrating real-time procedural generation into a Unity-based interactive environment.

Despite significant advancements in AI-based music generation, general-purpose pre-trained models often struggle when applied to highly structured and stylistically demanding genres.

During preliminary experimentation using pre-trained MusicVAE models from Magenta, results in Classical and Jazz domains were coherent and musically convincing. However, when applied to Metal, several critical limitations emerged:

- Lack of rhythmic consistency  
- Weak harmonic coherence  
- Absence of genre-specific features such as:
  - Complex drum patterns  
  - Fast tempo structures  
  - Distorted harmonic textures  

These limitations were traced back to the insufficient representation of Metal music in the original training datasets.

---

## 🎯 Project Objectives

The core objective of this thesis was to develop a system capable of generating **dynamic, stylistically coherent Metal music in real time**, designed to be integrated into a Unity game environment.

The project goals included:

- ✅ **Creation of a Specialized Dataset**  
  Collection, selection, and preprocessing (via Python) of a curated Metal MIDI corpus to compensate for dataset bias.

- ✅ **Model Fine-Tuning**  
  Adaptation and fine-tuning of MusicVAE architectures to:
  - Generate complex drum patterns  
  - Produce coherent melodic and harmonic structures  
  - Respect Metal stylistic conventions  

- ✅ **Real-Time Integration**  
  Development of an OSC-based communication interface enabling:
  - Real-time transmission of generated MIDI data  
  - Dynamic synchronization between Magenta’s inference engine and Unity  
  - Event-driven music generation responsive to gameplay  

---

## 🧠 Research Contribution

The adopted methodology demonstrates how **targeted dataset training significantly enhances the adaptability of generative models**, extending their applicability beyond their original optimization scope.

The final result is a **functional prototype** where procedural music generation is not merely a technical demonstration, but an interactive system that dynamically responds to user input inside a game environment.

---

## 🎮 Application Context

This project is part of a broader research direction aimed at developing assistive and inclusive technologies to enable individuals considered “fragile” (such as children, elderly people, or individuals with disabilities) to engage in therapeutic activities through music.

Specifically, this thesis focuses on:

> The development of an innovative real-time procedural music generation system for video games, designed as a potential foundation for interactive therapeutic applications.

---

## ⚙️ System Architecture

### Pipeline Overview

1. 🎵 Metal MIDI Dataset  
2. 🧠 MusicVAE (fine-tuned with TensorFlow)  
3. 🐍 Python inference engine  
4. 🔄 OSC communication layer  
5. 🎮 Unity real-time integration  

The system allows Unity to trigger musical generation events and receive dynamically generated MIDI sequences in real time.

---

## 🚀 Installation

### 1️⃣ Environment Setup (Anaconda)

Install **Anaconda** and create a virtual environment:

```bash
conda create -n magenta_metal python=3.x
conda activate magenta_metal

