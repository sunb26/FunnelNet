package net.jobayer.murmurdetector.data.utils

import android.content.Context
import android.content.Context.CONNECTIVITY_SERVICE
import android.net.ConnectivityManager
import android.net.NetworkCapabilities
import net.jobayer.murmurdetector.data.Const.API_BASE_URL
import net.jobayer.murmurdetector.data.api.HeartSoundApi
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

object NetUtil {

    private val retrofitForTimeApi = Retrofit.Builder()
        .addConverterFactory(GsonConverterFactory.create())
        .baseUrl(API_BASE_URL)
        .build()

    val heartSoundApi: HeartSoundApi by lazy {
        retrofitForTimeApi.create(HeartSoundApi::class.java)
    }

}

fun Context.isNetAvailable(): Boolean {
    val connectivityManager = getSystemService(CONNECTIVITY_SERVICE) as ConnectivityManager
    val nw = connectivityManager.activeNetwork ?: return false
    val actNw = connectivityManager.getNetworkCapabilities(nw) ?: return false
    return when {
        actNw.hasTransport(NetworkCapabilities.TRANSPORT_WIFI) -> true
        actNw.hasTransport(NetworkCapabilities.TRANSPORT_CELLULAR) -> true
        actNw.hasTransport(NetworkCapabilities.TRANSPORT_ETHERNET) -> true
        actNw.hasTransport(NetworkCapabilities.TRANSPORT_BLUETOOTH) -> true
        else -> false
    }
}