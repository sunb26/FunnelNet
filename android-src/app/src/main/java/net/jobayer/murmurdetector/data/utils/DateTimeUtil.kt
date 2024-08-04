package net.jobayer.murmurdetector.data.utils

import java.time.LocalDateTime
import java.time.format.DateTimeFormatter

fun getCurrentTime(): String {
    val current = LocalDateTime.now()
    val formatter = DateTimeFormatter.ofPattern("HH:mm:ss.SSSS")
    return current.format(formatter)
}