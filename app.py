from typing import Annotated
import audiofile
import soundfile
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse
from fastapi import FastAPI, File, UploadFile
from basic_pitch.inference import predict
from basic_pitch import ICASSP_2022_MODEL_PATH
import os
from fastapi import Path


app = FastAPI()
tmp_file_dir = "./"

@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    # if file.content_type != 'audio/wav' or file.content_type != 'audio/mp3' or file.content_type != 'audio/mpeg':
    #     raise HTTPException(400, detail = 'Wrong File format')
    print(file.filename)
    if 'mp3' in file.filename:
        with open(os.path.join(tmp_file_dir, file.filename), 'wb') as disk_file:
            file_bytes = file.file.read()

            disk_file.write(file_bytes)

            print(f"Received file named {file.filename} containing {len(file_bytes)} bytes. ")

        signal, sampling_rate = audiofile.read(file.filename)
        audiofile.write(f'{file.filename.replace("mp3", "wav")}', signal=signal, sampling_rate=sampling_rate)
        model_output, midi_data, note_events = predict(f'{file.filename.replace("mp3", "wav")}')
        midi_data.write(f'{file.filename.replace("mp3", "mid")}')
        return FileResponse(path=f'{file.filename.replace("mp3", "mid")}', media_type='audio/midi', filename=f'{file.filename.replace("mp3", "mid")}')
    else:
        
        
        print(f"Filename -> {file.filename}")
        with open(os.path.join(tmp_file_dir, file.filename), 'wb') as disk_file:
            file_bytes = file.file.read()

            disk_file.write(file_bytes)

            print(f"Received file named {file.filename} containing {len(file_bytes)} bytes. ")

            # return FileResponse(disk_file.name, media_type=file.content_type)
        signal, sampling_rate = audiofile.read(file.filename)
        audiofile.write(f'{file.filename}', signal=signal, sampling_rate=sampling_rate)
        model_output, midi_data, note_events = predict(f'{file.filename}')
        midi_data.write(f'{file.filename.replace("wav", "mid")}')
        return FileResponse(path=f'{file.filename.replace("wav", "mid")}', media_type='audio/midi', filename=f'{file.filename.replace("wav", "mid")}')