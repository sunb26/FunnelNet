package net.jobayer.murmurdetector.data.utils

import android.app.Activity
import androidx.appcompat.app.AlertDialog
import net.jobayer.murmurdetector.R

fun Activity.loadingDialog(): AlertDialog {

    val dialogView = layoutInflater.inflate(R.layout.loading_dialog, null)

    val dialogBuilder = AlertDialog.Builder(this, R.style.TransparentDialog)
        .setView(dialogView)
        .setCancelable(false)

    val customDialog = dialogBuilder.create().apply {
        setCanceledOnTouchOutside(false)
    }

    return customDialog
}

fun AlertDialog.showDialog() {
    if (!isShowing) {
        show()
    }
}

fun AlertDialog.dismissDialog() {
    if (isShowing) {
        dismiss()
    }
}