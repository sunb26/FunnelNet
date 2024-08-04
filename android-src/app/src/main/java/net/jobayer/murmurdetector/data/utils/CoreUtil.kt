package net.jobayer.murmurdetector.data.utils

import android.content.Context
import android.content.Intent
import android.net.Uri
import android.widget.Toast

fun Context.toast(msg: String, duration: Int = Toast.LENGTH_SHORT) {
    Toast.makeText(this, msg, duration).show()
}

fun Context.openAppSettings() {
    val intent = Intent().apply {
        action = android.provider.Settings.ACTION_APPLICATION_DETAILS_SETTINGS
        data = Uri.fromParts("package", packageName, null)
    }
    startActivity(intent)
}