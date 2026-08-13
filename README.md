# 🧠 Neural 3D Avatar Assisted Bidirectional Communication Framework for Deaf and Hearing Users

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python">
  <img src="https://img.shields.io/badge/Flask-Web%20Framework-green?style=for-the-badge&logo=flask">
  <img src="https://img.shields.io/badge/OpenCV-Computer%20Vision-red?style=for-the-badge&logo=opencv">
  <img src="https://img.shields.io/badge/MediaPipe-Gesture%20Tracking-orange?style=for-the-badge">
  <img src="https://img.shields.io/badge/Machine%20Learning-Scikit--learn-blueviolet?style=for-the-badge">
  <img src="https://img.shields.io/badge/Speech-Recognition-red?style=for-the-badge">
  <img src="https://img.shields.io/badge/3D-Avatar-purple?style=for-the-badge">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge">
</p>

---

## 📖 Overview

Communication between Deaf and Hearing individuals can be challenging when both users do not share the same communication method.

The **Neural 3D Avatar Assisted Bidirectional Communication Framework for Deaf and Hearing Users** is an **AI-powered communication system** designed to reduce this communication barrier by combining **Computer Vision, Machine Learning, Gesture Recognition, Speech Recognition, Text-to-Speech, and 3D Avatar technology**.

The framework enables communication in both directions by processing sign language gestures from Deaf users and converting spoken communication from Hearing users into understandable outputs.

The system provides an interactive communication platform that combines visual, textual, and audio-based communication.

---

# ✨ Key Features

✅ Real-Time Sign Language Recognition

✅ AI-Based Gesture Detection

✅ Hand Gesture Tracking using MediaPipe

✅ Computer Vision using OpenCV

✅ Machine Learning Based Gesture Classification

✅ Speech-to-Text Conversion

✅ Text-to-Speech Conversion

✅ Interactive 3D Avatar

✅ Bidirectional Communication

✅ Flask-Based Web Interface

✅ User-Friendly Communication System

✅ SQLite Database Support

---

# 🎯 Objectives

- Eliminate communication barriers between Deaf and Hearing users.
- Recognize sign language gestures using Computer Vision.
- Convert recognized gestures into meaningful text.
- Support speech-to-text communication.
- Provide text-to-speech output for Hearing users.
- Represent communication through a 3D avatar.
- Develop an accessible and interactive communication platform.
- Demonstrate the practical application of Artificial Intelligence in accessibility technology.

---

# 🔄 Bidirectional Communication

The framework supports communication in two directions.

### 🖐️ Deaf User → Hearing User

```text
       Deaf User
           │
           ▼
    Sign Language
           │
           ▼
   Webcam / Camera
           │
           ▼
   OpenCV + MediaPipe
           │
           ▼
   Gesture Recognition
           │
           ▼
 Machine Learning Model
           │
           ▼
      Predicted Text
           │
      ┌────┴────┐
      ▼         ▼
 Text Output   Speech
      │         │
      └────┬────┘
           ▼
     Hearing User
🎙️ Hearing User → Deaf User
     Hearing User
           │
           ▼
     Speech / Text
           │
           ▼
  Speech Recognition
           │
           ▼
       Text Data
           │
           ▼
   Language Processing
           │
           ▼
      3D Avatar
           │
           ▼
 Visual Communication
           │
           ▼
       Deaf User
🏗️ System Architecture
                    ┌───────────────────────┐
                    │        USERS          │
                    └───────────┬───────────┘
                                │
                 ┌──────────────┴──────────────┐
                 │                             │
                 ▼                             ▼
          ┌──────────────┐              ┌──────────────┐
          │  Deaf User   │              │ Hearing User │
          └──────┬───────┘              └──────┬───────┘
                 │                             │
                 ▼                             ▼
        ┌─────────────────┐            ┌─────────────────┐
        │ Camera / Sign   │            │ Speech / Text   │
        │ Language Input  │            │ Input           │
        └────────┬────────┘            └────────┬────────┘
                 │                             │
                 ▼                             ▼
        ┌─────────────────┐            ┌─────────────────┐
        │ OpenCV +        │            │ Speech          │
        │ MediaPipe       │            │ Recognition     │
        └────────┬────────┘            └────────┬────────┘
                 │                             │
                 ▼                             ▼
        ┌─────────────────┐            ┌─────────────────┐
        │ Gesture         │            │ Text Processing │
        │ Recognition     │            │                 │
        └────────┬────────┘            └────────┬────────┘
                 │                             │
                 ▼                             ▼
        ┌─────────────────┐            ┌─────────────────┐
        │ ML Model        │            │ Communication   │
        │ Classification  │            │ Processing      │
        └────────┬────────┘            └────────┬────────┘
                 │                             │
                 └──────────────┬──────────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │   3D Avatar /       │
                     │   Output Layer      │
                     └──────────┬──────────┘
                                │
                                ▼
                     Accessible Communication
💻 Technologies Used
Category	Technologies
Programming Language	Python
Backend	Flask
Frontend	HTML5, CSS3, JavaScript
Computer Vision	OpenCV
Gesture Tracking	MediaPipe
Machine Learning	Scikit-learn
Speech Recognition	SpeechRecognition
Text-to-Speech	gTTS
Database	SQLite
3D Visualization	3D Avatar
Development Tool	Visual Studio Code
Version Control	Git & GitHub
📂 Project Structure
Neural-3d-avatar-Assisted-Bidirectional-Communication-Framework-For-Deaf-And-Hearing-Users/
│
├── avatar/
│   └── 3D Avatar Resources
│
├── database/
│   └── Database Resources
│
├── dd/
│   └── Supporting Resources
│
├── sign/
│   └── Sign Language Resources
│
├── static/
│   ├── CSS
│   ├── JavaScript
│   └── Images
│
├── templates/
│   └── HTML Templates
│
├── camera.py
├── camera1.py
├── main.py
│
├── gesture_model.pkl
├── gesture_map.pkl
│
├── read.txt
├── bc.txt
│
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
⚙️ Installation
1️⃣ Clone the Repository
git clone https://github.com/Dhonijd12345/Neural-3d-avatar-Assisted-Bidirectional-Communication-Framework-For-Deaf-And-Hearing-Users.git
2️⃣ Navigate to the Project Directory
cd Neural-3d-avatar-Assisted-Bidirectional-Communication-Framework-For-Deaf-And-Hearing-Users
3️⃣ Create a Virtual Environment
Windows
python -m venv venv

Activate the environment:

venv\Scripts\activate
macOS / Linux
python3 -m venv venv

Activate:

source venv/bin/activate
4️⃣ Install Dependencies
pip install -r requirements.txt
▶️ Running the Application

Start the Flask application using:

python main.py

After starting the application, open the local Flask address displayed in the terminal in your web browser.

🖐️ Sign Language Recognition Workflow
Camera Input
     │
     ▼
Video Frame Capture
     │
     ▼
OpenCV Processing
     │
     ▼
MediaPipe Hand Tracking
     │
     ▼
Feature Extraction
     │
     ▼
Gesture Model
     │
     ▼
Gesture Classification
     │
     ▼
Recognized Text
🎙️ Speech Recognition Workflow
User Speech
     │
     ▼
Microphone
     │
     ▼
Speech Recognition
     │
     ▼
Text Conversion
     │
     ▼
Text Processing
     │
     ▼
Communication Output
🔊 Text-to-Speech Workflow
Recognized Text
      │
      ▼
Text Processing
      │
      ▼
Text-to-Speech Engine
      │
      ▼
Generated Audio
      │
      ▼
Hearing User
🤖 3D Avatar Communication

The 3D avatar acts as a visual communication component of the framework.

Text / Speech Input
       │
       ▼
Speech Recognition
       │
       ▼
Text Processing
       │
       ▼
Gesture / Sign Mapping
       │
       ▼
3D Avatar
       │
       ▼
Visual Communication
📸 Screenshots

Add your application screenshots inside the screenshots/ directory.

🏠 Home Page

🖐️ Gesture Detection

🤖 3D Avatar

📝 Communication Output

Replace the screenshot filenames above with the exact files available in your repository.

🎥 Demo

Add your project demonstration video link here after uploading it to YouTube or LinkedIn.

https://youtu.be/YourDemoVideo

The demonstration can showcase:

Application startup
Sign language detection
Gesture recognition
Text generation
Speech recognition
Text-to-speech
3D avatar communication
Bidirectional communication
📊 Applications

The framework can potentially be used in:

🏫 Educational Institutions

🏥 Hospitals and Healthcare Centers

🏦 Banks and Financial Institutions

🏢 Corporate Workplaces

🏛️ Government Offices

🚉 Railway Stations

✈️ Airports

🛍️ Customer Service Centers

📞 Communication Support Systems

🌐 Accessibility Platforms

🌟 Advantages
♿ Improves communication accessibility.
🤖 Uses Artificial Intelligence for gesture recognition.
🖐️ Supports real-time sign language processing.
🎙️ Supports speech recognition.
🔊 Provides speech output.
🤖 Uses a 3D avatar for visual communication.
🌐 Provides a web-based interface.
🧩 Modular and extendable architecture.
💡 Demonstrates a real-world AI accessibility application.
⚠️ Limitations

The performance of the system may depend on:

Camera quality.
Lighting conditions.
Background complexity.
Gesture execution.
Training dataset quality.
Machine learning model accuracy.
Hardware performance.
Supported sign vocabulary.

The current implementation may require further development for complete sentence-level and continuous sign language recognition.

🚀 Future Enhancements

The project can be further improved with:

🧠 Deep Learning based Sign Language Recognition
📝 Sentence-Level Sign Language Translation
🌍 Multiple Sign Language Support
📱 Mobile Application
☁️ Cloud Deployment
🎙️ Advanced Voice Assistant
🤖 AI Chatbot Integration
🎥 Real-Time Video Calling
🧠 Transformer-Based Gesture Recognition
🌐 Multilingual Communication
🤖 Advanced 3D Avatar Animation
⚡ Real-Time Edge AI Processing
📚 Learning Outcomes

Through this project, I strengthened my practical knowledge in:

Artificial Intelligence
Machine Learning
Computer Vision
OpenCV
MediaPipe
Gesture Recognition
Speech Recognition
Text-to-Speech
Natural Language Processing
Flask Web Development
Python Programming
SQLite Database Integration
Git & GitHub
AI-Based Accessibility Solutions
📌 Project Information
Information	Details
Project Type	AI-Based Accessibility Application
Domain	Artificial Intelligence
Category	Computer Vision & Communication
Interface	Flask Web Application
Language	Python
Framework	Flask
Recognition	Gesture Recognition
Communication	Bidirectional
License	MIT
Version	1.0.0
🔮 Project Impact

This project demonstrates how Artificial Intelligence can be applied to solve real-world accessibility challenges.

By combining:

Computer Vision + Machine Learning + Speech Processing + 3D Avatar Technology

the framework aims to create a more inclusive communication environment for Deaf and Hearing users.

🤝 Contributing

Contributions are welcome!

To contribute:

Fork this repository.
Create a new feature branch.
Make your changes.
Test your implementation.
Commit your changes.
Push the branch.
Create a Pull Request.

Example:

git checkout -b feature/new-feature
git add .
git commit -m "Add new communication feature"
git push origin feature/new-feature

Please follow the contribution guidelines before submitting major changes.

📄 License

This project is licensed under the MIT License.

See the LICENSE file for more information.

🙏 Acknowledgements

Special thanks to:

Python Community
OpenCV Community
MediaPipe Community
Scikit-learn Community
Flask Community
Open-Source AI Community
Accessibility Technology Researchers
👨‍💻 Author
Nikile Eines Dhoni J

B.Tech – Artificial Intelligence and Data Science

Mohamed Sathak Engineering College

🔗 GitHub

https://github.com/Dhonijd12345

🔗 LinkedIn

https://www.linkedin.com/in/dhoni-j-7b73b92a2

⭐ Support

If you find this project useful or interesting:

⭐ Star this repository

🍴 Fork this repository

🐛 Report issues

💡 Suggest improvements

🤝 Contribute to the project

<p align="center">
🌍 Breaking Communication Barriers with Artificial Intelligence ❤️
Built with Python, Computer Vision, Machine Learning, Speech Processing & 3D Avatar Technology

Made with ❤️ by Nikile Eines Dhoni J

</p> ```
