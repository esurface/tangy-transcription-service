import streamlit as st
import os
import zipfile
import json

#from asr import transcribe_audio

st.title("Tangerine Transcription Service")
st.write(
    "Use this service to upload and transcribe audio files."
)

zip_file = st.file_uploader(label="Upload Zip File", type=["zip"], key="zip_uploader")

def unzip_files(zip_file):
    if zip_file is not None:
        # Create a directory to extract files
        extract_dir = "extracted_files"
        os.makedirs(extract_dir, exist_ok=True)

        # Unzip the file
        with zipfile.ZipFile(zip_file, 'r') as z:
            z.extractall(extract_dir)
            st.success(f"Files extracted to {extract_dir}")

st.button("Unzip", on_click=unzip_files, args=(zip_file,))

# show the audio files in streamlit table
for root, dirs, files in os.walk("extracted_files"):
    for file in files:
        if file.endswith(".wav") or file.endswith(".mp3"):
            st.write(f"File: {file}")
            st.audio(os.path.join(root, file), format="audio/wav")
            evaluation_key = f"evaluation_{file}"
            if st.button("Evaluate", key=evaluation_key):
                transctiption_key = f"transcription_{file}"
                #transcription = transcribe_audio(file)
                st.text_area("Transcription", key=transctiption_key, value="Transcription will appear here.", height=300)

def save_transcriptions():
    # Save a json file with the transcriptions in the format:
    """
    {
        "response_id": {
            "filename": "filename.wav",
            "transcription": "transcription text",
            "score": "score text"
        }
    }
    """
    transcriptions = {}
    for root, dirs, files in os.walk("extracted_files"):
        for file in files:
            if file.endswith(".wav") or file.endswith(".mp3"):
                transcription_key = f"transcription_{file}"
                transcription = st.session_state.get(transcription_key, "")
                score_key = f"score_{file}"
                score = st.session_state.get(score_key, "")

                if transcription:
                    transcriptions[file] = {
                        "filename": file,
                        "transcription": transcription,
                        "score": score
                    }
    # Save to a JSON file
    with open("transcriptions.json", "w") as f:
        json.dump(transcriptions, f, indent=4)


st.button("Save Transcriptions", on_click=lambda: st.success("Transcriptions saved!"))