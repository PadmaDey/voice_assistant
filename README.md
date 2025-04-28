# voice_assistant_groq

Here’s a clean, professional `README.md` for your Voice Assistant project:

---

# 🎙️ Voice Assistant

A voice-based assistant built using Flask, Hugging Face models, and Groq API for natural language processing. The assistant listens to your voice, transcribes it, detects emotions, generates responses, and speaks back to you with Text-to-Speech (TTS). It also stores chat history in a local database.

## Features

- **Speech-to-Text (ASR)**: Uses Whisper model from OpenAI to transcribe audio into text.
- **Emotion Detection**: Detects emotions from the user’s speech using Hugging Face models.
- **Response Generation**: Generates intelligent responses using the Groq API and natural language processing.
- **Text-to-Speech**: Converts generated responses back to speech using pyttsx3.
- **Real-time Chat History**: Displays previous interactions and current conversation.
- **Dark/Light Mode**: Toggle between dark and light themes in the user interface.

## Requirements

To run this project, you need to install the required dependencies. You can do so by running:

```bash
pip install -r requirements.txt
```

### Key Dependencies:
- **Flask**: Web framework for the server.
- **Transformers**: Hugging Face library for Natural Language Processing (NLP).
- **Pyttsx3**: Text-to-Speech engine.
- **Groq SDK**: For generating intelligent responses.
- **Whisper**: Automatic Speech Recognition (ASR) for transcribing audio.

## Setup & Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-username/voice-assistant.git
   cd voice-assistant
   ```

2. **Set up environment variables**:

   Create a `.env` file in the project root and add your Hugging Face and Groq API tokens.

   Example `.env` file:

   ```
   HF_TOKEN=your_huggingface_token
   GROQ_API_KEY=your_groq_api_key
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask server**:

   Start the Flask application with the following command:

   ```bash
   python record_and_transcribe.py
   ```

   This will run the server locally at `http://127.0.0.1:5000`.

## API Routes

- `/`: **GET** - Displays the current chat history and system status.
- `/record`: **POST** - Starts recording the user’s voice and processes the audio.
- `/transcribe`: **GET** - Transcribes the recorded audio into text.
- `/emotion`: **GET** - Detects the emotion from the user’s transcribed text.
- `/generate`: **GET** - Generates a response based on the user’s message and emotion.
- `/latest_chat`: **GET** - Fetches the latest chat entry.

## Usage

Once the server is running, visit `http://127.0.0.1:5000` in your web browser.

- **Start Recording**: Click the "Start Talking" button to record your voice.
- **Interaction**: The assistant will transcribe your voice, detect emotions, generate a response, and speak it back to you.

## Contributing

Feel free to fork the repository, submit issues, or create pull requests. Contributions are welcome!

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

### Explanation:
1. **Project Overview**: Gives a brief introduction to the functionality of the voice assistant.
2. **Features**: Lists the core features of the app, focusing on speech-to-text, emotion detection, and response generation.
3. **Requirements & Setup**: Detailed steps for installation and running the project, including environment setup and dependencies.
4. **API Routes**: Documents the available API endpoints in case you plan to expand or expose them.
5. **Usage**: Describes how users can interact with the assistant once it’s up and running.
6. **Contributing**: Encourages collaboration and makes it easy for other developers to contribute.
7. **License**: A standard MIT License for open-source projects.

This README is structured to be clear, professional, and informative, ideal for a real-world project. Let me know if you need further customizations or additions!