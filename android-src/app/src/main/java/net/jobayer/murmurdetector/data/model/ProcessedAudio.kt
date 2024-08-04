package net.jobayer.murmurdetector.data.model

import android.os.Parcelable
import androidx.annotation.Keep
import com.google.gson.annotations.SerializedName
import kotlinx.parcelize.Parcelize

@Keep
@Parcelize
data class ProcessedAudio(
    @SerializedName("data")
    var `data`: String = ""
) : Parcelable