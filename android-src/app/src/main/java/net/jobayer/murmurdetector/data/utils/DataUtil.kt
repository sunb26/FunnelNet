package net.jobayer.murmurdetector.data.utils

import android.content.Context
import android.net.Uri
import net.jobayer.murmurdetector.data.Const.API_PROCESS_MULTIPART_NAME
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.MultipartBody
import okhttp3.RequestBody.Companion.asRequestBody

fun Context.getMultipartFromUri(uri: Uri): MultipartBody.Part {
    val audioFile = getFile(this, uri)
    val requestFile = audioFile.asRequestBody("multipart/form-data".toMediaTypeOrNull())
    return MultipartBody.Part.createFormData(API_PROCESS_MULTIPART_NAME, audioFile.name, requestFile)
}