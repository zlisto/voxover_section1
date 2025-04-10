import streamlit as st
import os
import tempfile
import time
from pathlib import Path
import uuid
import base64
from utils import (
    generate_voiceover_text,
    generate_voiceover_audio,
    merge_video_with_audio
)

# Set page configuration
st.set_page_config(
    page_title="VoxOver: AI Narration Studio",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to improve the appearance
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #4CAF50;
        margin-bottom: 0;
    }
    .subheader {
        font-size: 1.2rem;
        color: #555;
        margin-top: 0;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #2196F3;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .info-text {
        color: #666;
        font-size: 1rem;
    }
    .success-text {
        color: #4CAF50;
        font-weight: bold;
    }
    .warning-text {
        color: #ff9800;
        font-weight: bold;
    }
    .error-text {
        color: #f44336;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to create a download link for files
def get_download_link(file_path, link_text="Download File"):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    file_name = os.path.basename(file_path)
    href = f'<a href="data:file/mp4;base64,{b64}" download="{file_name}">{link_text}</a>'
    return href

# Function to create a temporary directory for this session
def get_session_temp_dir():
    if 'temp_dir' not in st.session_state:
        st.session_state.temp_dir = tempfile.mkdtemp()
    return st.session_state.temp_dir

# Initialize session state variables
def init_session_state():
    if 'video_path' not in st.session_state:
        st.session_state.video_path = None
    if 'voiceover_text' not in st.session_state:
        st.session_state.voiceover_text = ""
    if 'audio_path' not in st.session_state:
        st.session_state.audio_path = None
    if 'merged_video_path' not in st.session_state:
        st.session_state.merged_video_path = None
    if 'processing_step' not in st.session_state:
        st.session_state.processing_step = 0
    if 'instructions' not in st.session_state:
        st.session_state.instructions = ""
    if 'video_volume' not in st.session_state:
        st.session_state.video_volume = 0.3  # Default to 30% of original volume
    if 'audio_volume' not in st.session_state:
        st.session_state.audio_volume = 1.0  # Default to 100% voiceover volume
    if 'selected_voice' not in st.session_state:
        st.session_state.selected_voice = 'nova'
    if 'voice_speed' not in st.session_state:
        st.session_state.voice_speed = 1.0

# Function to save uploaded video file
def save_uploaded_file(uploaded_file):
    try:
        temp_dir = get_session_temp_dir()
        file_extension = Path(uploaded_file.name).suffix
        temp_file_path = os.path.join(temp_dir, f"input_video_{uuid.uuid4()}{file_extension}")
        
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        return temp_file_path
    except Exception as e:
        st.error(f"Error saving uploaded file: {e}")
        return None

# Callback functions
def generate_text_callback():
    st.session_state.processing_step = 1
    with st.spinner("Analyzing video and generating voiceover text..."):
        try:
            st.session_state.voiceover_text = generate_voiceover_text(
                st.session_state.video_path, 
                st.session_state.instructions
            )
            st.success("Voiceover text generated successfully!")
        except Exception as e:
            st.error(f"Error generating voiceover text: {e}")
            st.session_state.voiceover_text = ""

def generate_audio_callback():
    st.session_state.processing_step = 2
    with st.spinner("Converting text to speech..."):
        try:
            temp_dir = get_session_temp_dir()
            audio_path = os.path.join(temp_dir, f"voiceover_{uuid.uuid4()}.mp3")
            
            generate_voiceover_audio(
                st.session_state.voiceover_text,
                audio_path,
                voice_name=st.session_state.selected_voice,
                speed=st.session_state.voice_speed
            )
            
            st.session_state.audio_path = audio_path
            st.success("Audio voiceover generated successfully!")
        except Exception as e:
            st.error(f"Error generating audio: {e}")
            st.session_state.audio_path = None

def merge_video_audio_callback():
    st.session_state.processing_step = 3
    with st.spinner("Merging video with voiceover audio..."):
        try:
            temp_dir = get_session_temp_dir()
            merged_path = os.path.join(temp_dir, f"merged_video_{uuid.uuid4()}.mp4")
            
            merge_video_with_audio(
                st.session_state.video_path,
                st.session_state.audio_path,
                merged_path,
                video_volume=st.session_state.video_volume,
                audio_volume=st.session_state.audio_volume
            )
            
            st.session_state.merged_video_path = merged_path
            st.success("Video and audio merged successfully!")
        except Exception as e:
            st.error(f"Error merging video and audio: {e}")
            st.session_state.merged_video_path = None

def start_over():
    for key in ['video_path', 'voiceover_text', 'audio_path', 'merged_video_path', 'processing_step']:
        if key in st.session_state:
            st.session_state[key] = None if key != 'voiceover_text' else ""
    st.session_state.processing_step = 0
    st.rerun()

# Main app
def main():
    # Initialize session state
    init_session_state()
    
    # App header
    st.markdown('<h1 class="main-header">VoxOver: AI Narration Studio</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subheader">Create professional AI voiceovers for your videos in minutes</p>', unsafe_allow_html=True)
    
    # Sidebar for instructions and controls
    with st.sidebar:
        st.markdown('<h2 class="section-header">How It Works</h2>', unsafe_allow_html=True)
        st.markdown("""
        1. **Upload** your video file
        2. **Describe** the style and content for your voiceover
        3. **Generate & Edit** the voiceover text
        4. **Choose** your preferred AI voice
        5. **Adjust** volume levels
        6. **Create** your final video with voiceover
        7. **Download** the result
        """)
        
        st.markdown('<h2 class="section-header">Start Over</h2>', unsafe_allow_html=True)
        if st.button("Start New Project", type="primary"):
            start_over()
    
    # Main workflow based on current step
    if st.session_state.processing_step == 0:
        # Step 1: Video Upload
        st.markdown('<h2 class="section-header">Step 1: Upload Your Video</h2>', unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "mov", "avi", "mkv"])
        if uploaded_file is not None:
            video_path = save_uploaded_file(uploaded_file)
            if video_path:
                st.session_state.video_path = video_path
                video_col, _ = st.columns([1, 3])
                with video_col:
                    st.video(video_path)
                
                st.markdown('<h2 class="section-header">Step 2: Describe Your Voiceover</h2>', unsafe_allow_html=True)
                st.markdown("""
                <p class="info-text">
                Describe the style, tone, and content for your voiceover. Be specific about what you want the 
                narration to focus on and any particular speaking style you prefer.
                </p>
                """, unsafe_allow_html=True)
                
                instructions = st.text_area(
                    "Voiceover Instructions",
                    placeholder="Examples:\n- Create a professional documentary-style narration that explains what's happening in the video\n- Make an enthusiastic tutorial voice that guides viewers through each step shown\n- Generate a calm, meditative narration focusing on the natural scenery in this video",
                    height=150
                )
                
                if instructions:
                    st.session_state.instructions = instructions
                    if st.button("Generate Voiceover Text", type="primary"):
                        generate_text_callback()
    
    if st.session_state.processing_step >= 1:
        # Display the original video
        st.markdown('<h2 class="section-header">Your Video</h2>', unsafe_allow_html=True)
        video_col, _ = st.columns([1, 3])  # This creates a 1:3 ratio column layout
        with video_col:
            st.video(st.session_state.video_path)
        
        # Step 3: Edit Voiceover Text
        st.markdown('<h2 class="section-header">Step 3: Edit Voiceover Text</h2>', unsafe_allow_html=True)
        st.markdown("""
        <p class="info-text">
        Review and edit the AI-generated voiceover text below. Make any changes needed to better match your vision.
        </p>
        """, unsafe_allow_html=True)
        
        voiceover_text = st.text_area(
            "Voiceover Script", 
            st.session_state.voiceover_text,
            height=250
        )
        
        if voiceover_text != st.session_state.voiceover_text:
            st.session_state.voiceover_text = voiceover_text
        
        # Step 4: Voice Selection and Settings
        st.markdown('<h2 class="section-header">Step 4: Voice Settings</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            voice_options = [
                'nova', 'alloy', 'ash', 'ballad', 'coral', 
                'echo', 'fable', 'onyx', 'sage', 'shimmer'
            ]
            selected_voice = st.selectbox(
                "Select Voice", 
                options=voice_options,
                index=voice_options.index(st.session_state.selected_voice)
            )
            if selected_voice != st.session_state.selected_voice:
                st.session_state.selected_voice = selected_voice
        
        with col2:
            voice_speed = st.slider(
                "Voice Speed", 
                min_value=0.5, 
                max_value=1.5, 
                value=st.session_state.voice_speed,
                step=0.1
            )
            if voice_speed != st.session_state.voice_speed:
                st.session_state.voice_speed = voice_speed
        
        # Generate Audio button
        if st.button("Generate Voiceover Audio", type="primary"):
            generate_audio_callback()
    
    if st.session_state.processing_step >= 2:
        # Display the generated audio
        st.markdown('<h2 class="section-header">Step 5: Preview Voiceover Audio</h2>', unsafe_allow_html=True)
        
        if st.session_state.audio_path and os.path.exists(st.session_state.audio_path):
            st.audio(st.session_state.audio_path)
            
            # Step 6: Volume Controls
            st.markdown('<h2 class="section-header">Step 6: Adjust Volume Levels</h2>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                video_volume = st.slider(
                    "Original Video Volume", 
                    min_value=0.0, 
                    max_value=1.0, 
                    value=st.session_state.video_volume,
                    step=0.1,
                    help="0 = mute original audio, 1 = full volume"
                )
                if video_volume != st.session_state.video_volume:
                    st.session_state.video_volume = video_volume
            
            with col2:
                audio_volume = st.slider(
                    "Voiceover Volume", 
                    min_value=0.1, 
                    max_value=2.0, 
                    value=st.session_state.audio_volume,
                    step=0.1,
                    help="Adjust the volume of the AI voiceover"
                )
                if audio_volume != st.session_state.audio_volume:
                    st.session_state.audio_volume = audio_volume
            
            # Merge button
            if st.button("Create Final Video", type="primary"):
                merge_video_audio_callback()
    
    if st.session_state.processing_step >= 3:
        # Display the final result
        st.markdown('<h2 class="section-header">Step 7: Final Video with Voiceover</h2>', unsafe_allow_html=True)
        
        if st.session_state.merged_video_path and os.path.exists(st.session_state.merged_video_path):
            video_col, _ = st.columns([1, 3])
            with video_col:
                st.video(st.session_state.merged_video_path)
            
            # Download button
            st.markdown('<h2 class="section-header">Download Your Video</h2>', unsafe_allow_html=True)
            st.markdown(get_download_link(st.session_state.merged_video_path, "Download Video with Voiceover"), unsafe_allow_html=True)
            
            # Provide option to adjust and retry
            st.markdown('<h2 class="section-header">Not satisfied? Adjust and try again</h2>', unsafe_allow_html=True)
            
            retry_cols = st.columns(3)
            with retry_cols[0]:
                if st.button("Edit Text Again"):
                    st.session_state.processing_step = 1
                    st.rerun()
            
            with retry_cols[1]:
                if st.button("Change Voice Settings"):
                    st.session_state.processing_step = 1
                    st.rerun()
            
            with retry_cols[2]:
                if st.button("Adjust Volumes"):
                    st.session_state.processing_step = 2
                    st.rerun()

if __name__ == "__main__":
    main()