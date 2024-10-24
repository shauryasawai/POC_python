import os
import streamlit as st
from gtts import gTTS
from pydub import AudioSegment
from pydub.utils import which

ffmpeg_path = r"C:\FFmpeg\bin"
os.environ["PATH"] += os.pathsep + ffmpeg_path

AudioSegment.converter = which("ffmpeg")
AudioSegment.ffprobe = which("ffprobe")
# Streamlit app starts here
st.title("Audio Processing with AI Voice Replacement")

uploaded_file = st.file_uploader("Upload an MP3 or WAV file", type=['mp3', 'wav'])

if uploaded_file is not None:
    # Display the name of the uploaded file
    st.write(f"Uploaded file: {uploaded_file.name}")
    
    # Check if the file is in MP3 or WAV format
    if uploaded_file.name.endswith('.mp3') or uploaded_file.name.endswith('.wav'):
        # Save the uploaded file temporarily
        file_path = f"temp_{uploaded_file.name}"
        
        # Write the file to disk
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success(f"File saved as {file_path}")
        
        # Process the audio file (replace the audio with AI-generated voice)
        st.write("Generating AI voice...")
        
        # Generate AI voice using gTTS (Google Text-to-Speech)
        tts = gTTS("This is a test replacement of your audio with an AI voice.")
        tts.save("ai_voice.mp3")
        
        # Load the AI-generated audio (mp3) using pydub
        ai_voice = AudioSegment.from_mp3("ai_voice.mp3")
        
        # Load the original uploaded audio file using pydub
        if uploaded_file.name.endswith('.mp3'):
            original_audio = AudioSegment.from_mp3(file_path)
        elif uploaded_file.name.endswith('.wav'):
            original_audio = AudioSegment.from_wav(file_path)
        
        # Replace or combine the original audio with the AI-generated voice
        combined_audio = ai_voice  # You can modify this to mix or replace as needed
        
        # Export the combined audio to a new file
        output_path = "output_audio.mp3"
        combined_audio.export(output_path, format="mp3")
        
        st.success(f"AI voice replaced audio saved as {output_path}")
        
        # Provide a download link for the new audio file
        with open(output_path, "rb") as f:
            st.download_button("Download the modified audio", f, file_name="modified_audio.mp3")
        
        # Clean up temporary files after the process is complete
        os.remove(file_path)
        del ai_voice  # Ensure all references are removed
        os.remove("ai_voice.mp3")
        os.remove(output_path)

    else:
        st.error("Please upload a valid MP3 or WAV file.")
