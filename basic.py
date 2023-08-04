from basic_pitch.inference import predict
from basic_pitch import ICASSP_2022_MODEL_PATH
import streamlit as st

upload_file = st.file_uploader('Upload a MP3 or a WAV file', type=['mp3', 'wav'])
if upload_file is not None:
    bytes_val = upload_file.getvalue()
    
    model_output, midi_data, note_events = predict('piano.mp3')
    st.write(midi_data.write(f'{upload_file.name}.mid'))
