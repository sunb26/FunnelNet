package net.jobayer.murmurdetector.data.utils

import android.Manifest
import android.app.Activity
import android.content.pm.PackageManager
import android.os.Build
import androidx.core.content.ContextCompat

fun getPermissionList(): Array<String> {
    val permissions = arrayListOf<String>()
    permissions.add(Manifest.permission.READ_EXTERNAL_STORAGE)
    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
        permissions.add(Manifest.permission.READ_MEDIA_AUDIO)
    }
    return permissions.toTypedArray()
}

fun Activity.permissionGranted(vararg permissions: String): Boolean {
    var granted = false
    val grantCode = PackageManager.PERMISSION_GRANTED
    for (permission in permissions) {
        granted = ContextCompat.checkSelfPermission(this, permission) == grantCode
    }
    return granted
}