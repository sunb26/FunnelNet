import io
import json
import os

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse

from sig import preprocess_audio
from dsp import dsp

app = FastAPI()

@app.get("/")
def read_root():
    return {"msg": "Welcome to the audio processing API!"}

@app.get("/ping")
def ping():
    return { "msg": "Help" }

@app.post("/filter_audio")
async def filter_audio(audio: UploadFile = File(...)):
    try:
        buffer = io.BytesIO(await audio.read())
        
        print("Processing audio...")
        processed_audio_buffer = await dsp(buffer)
        
        print("Finished filtering audio...")
        return StreamingResponse(processed_audio_buffer, media_type="audio/wav")
    except Exception as e:
        return {"error": str(e)}

@app.post("/process_audio")
async def process_audio(audio: UploadFile = File(...)):
    try:
        temp_file = "temp.wav"
        with open(temp_file, "wb") as buffer:
            buffer.write(await audio.read())
        buffer.close()

        processed_audio = await preprocess_audio(temp_file)

        os.remove(temp_file)

        return {
            "data": json.dumps(processed_audio.tolist())
        }

    except Exception as e:
        return {"error": str(e)}