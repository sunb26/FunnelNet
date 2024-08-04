package net.jobayer.murmurdetector.data

object Const {

    const val TFLITE_MODEL_NAME = "model.tflite"

    // TODO: remove this url before pushing to public repository
    const val API_BASE_URL = "https://heart-sound-server.onrender.com/"

    const val API_PATH_PING = "ping"
    const val API_PATH_PROCESS_AUDIO = "process_audio"
    const val API_PROCESS_MULTIPART_NAME = "audio"

    const val PING_RESPONSE_ALIVE = "alive"

}