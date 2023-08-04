from basic_pitch.inference import predict_and_save
from basic_pitch import ICASSP_2022_MODEL_PATH
import os


output_dir = './'
input_path = 'piano.mp3'
os.system(f'basic-pitch {output_dir} {input_path}')