# voxover_section1
voiceover app for section 1

# VoxOver: AI Narration Studio

A Streamlit application that empowers users to generate AI voiceovers for their videos using state-of-the-art AI text generation and text-to-speech technology.

## Features

- **Upload Video Files**: Support for MP4, MOV, AVI, and MKV formats
- **AI-Generated Narration**: Analyze video content and generate custom voiceover text
- **Text Editing**: Edit and refine the generated voiceover script
- **Voice Selection**: Choose from 10 high-quality AI voices
- **Speed Control**: Adjust the speaking pace of the voiceover
- **Volume Mixing**: Control the balance between original audio and voiceover
- **Preview and Download**: Watch and download the final video with integrated voiceover

## Installation

1. Clone this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables:
   - Create a `.env` file in the project root directory
   - Add your API keys:
     ```
     OPENAI_API_KEY=your_openai_api_key
     ELEVENLABS_API_KEY=your_elevenlabs_api_key
     ```

## Usage

1. Start the Streamlit app:

```bash
streamlit run app.py
```

2. Open your web browser and navigate to the URL displayed in the terminal (typically http://localhost:8501)

3. Follow the step-by-step workflow in the application:
   - Upload your video
   - Provide instructions for the voiceover style and content
   - Edit the generated voiceover text
   - Select voice and adjust settings
   - Create the final video with voiceover
   - Download the result

## Project Structure

- `app.py`: Main Streamlit application
- `utils.py`: Utility functions for video processing, text generation, and audio synthesis
- `genai.py`: Class for interacting with OpenAI APIs for text and audio generation

## Requirements

- Python 3.8+
- Internet connection for AI API calls
- OpenAI API key with access to GPT-4 and TTS models

## Notes

- Processing time depends on video length and complexity
- Keep generated voiceover text within the appropriate word count for your video duration
- For best results, provide clear instructions about the style and content you want for your voiceover

## License

This project is licensed under the MIT License - see the LICENSE file for details.