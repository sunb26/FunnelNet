package net.jobayer.murmurdetector.data.api

import net.jobayer.murmurdetector.data.Const.API_PATH_PING
import net.jobayer.murmurdetector.data.Const.API_PATH_PROCESS_AUDIO
import net.jobayer.murmurdetector.data.Const.API_PROCESS_MULTIPART_NAME
import net.jobayer.murmurdetector.data.model.PingResponse
import net.jobayer.murmurdetector.data.model.ProcessedAudio
import okhttp3.MultipartBody
import retrofit2.Response
import retrofit2.http.GET
import retrofit2.http.Multipart
import retrofit2.http.POST
import retrofit2.http.Part

interface HeartSoundApi {

    @GET(API_PATH_PING)
    suspend fun ping(): Response<PingResponse>

    @Multipart
    @POST(API_PATH_PROCESS_AUDIO)
    suspend fun processAudio(@Part file: MultipartBody.Part): Response<ProcessedAudio>

}