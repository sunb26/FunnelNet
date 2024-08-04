import json
import os

from fastapi import FastAPI, File, UploadFile

from sig import preprocess_audio

app = FastAPI()

@app.get("/")
def read_root():
    return {"msg": "Welcome to the audio processing API!"}

@app.get("/ping")
def ping():
    return { "msg": "alive" }

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