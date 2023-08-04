from typing import Annotated
import audiofile
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse
from fastapi import FastAPI, File, UploadFile
from basic_pitch.inference import predict
from basic_pitch import ICASSP_2022_MODEL_PATH


app = FastAPI()


@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    # if file.content_type != 'audio/wav' or file.content_type != 'audio/mp3' or file.content_type != 'audio/mpeg':
    #     raise HTTPException(400, detail = 'Wrong File format')
    print(file.filename)
    if 'mp3' in file.filename:
        signal, sampling_rate = audiofile.read(file.filename)
        audiofile.write(f'{file.filename.replace("mp3", "wav")}', signal=signal, sampling_rate=sampling_rate)
        model_output, midi_data, note_events = predict(f'{file.filename.replace("mp3", "wav")}')
        midi_data.write(f'{file.filename.replace("mp3", "mid")}')
        return FileResponse(path=f'{file.filename.replace("mp3", "mid")}', media_type='audio/midi', filename=f'{file.filename.replace("mp3", "mid")}')
    else:
        signal, sampling_rate = audiofile.read(file.filename)
        audiofile.write(f'{file.filename}', signal=signal, sampling_rate=sampling_rate)
        model_output, midi_data, note_events = predict(f'{file.filename}')
        midi_data.write(f'{file.filename.replace("wav", "mid")}')
        return FileResponse(path=f'{file.filename.replace("wav", "mid")}', media_type='audio/midi', filename=f'{file.filename.replace("wav", "mid")}')