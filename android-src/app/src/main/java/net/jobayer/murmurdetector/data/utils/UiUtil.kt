package net.jobayer.murmurdetector.data.utils

import android.text.Spannable
import android.text.SpannableStringBuilder
import android.text.method.ScrollingMovementMethod
import android.text.style.ForegroundColorSpan
import android.view.View
import android.widget.Button
import android.widget.ScrollView
import android.widget.TextView
import net.jobayer.murmurdetector.R

fun Button.onClick(toDo : () -> Unit) {
    setOnClickListener {
        toDo()
    }
}

fun TextView.makeScrollable() {
    movementMethod = ScrollingMovementMethod()
}

fun TextView.appendText(newText: String, color: Int, scrollView: ScrollView) {
    val currentText = text
    val spannableBuilder = SpannableStringBuilder(currentText)

    val newTextWithColor = SpannableStringBuilder(newText)
    newTextWithColor.setSpan(
        ForegroundColorSpan(color),
        0,
        newText.length,
        Spannable.SPAN_EXCLUSIVE_EXCLUSIVE
    )

    val currentDateTime = getCurrentTime()
    val dateTimeTextWithColor = SpannableStringBuilder("$currentDateTime ")
    dateTimeTextWithColor.setSpan(
        ForegroundColorSpan(this.context.getColor(R.color.light_blue)),
        0,
        currentDateTime.length,
        Spannable.SPAN_EXCLUSIVE_EXCLUSIVE
    )

    spannableBuilder.append("\n\n").append(dateTimeTextWithColor).append(newTextWithColor)

    text = spannableBuilder

    scrollView.post {
        scrollView.fullScroll(View.FOCUS_DOWN)
    }
}

fun View.visible() {
    if (visibility != View.VISIBLE) {
        visibility = View.VISIBLE
    }
}

fun View.gone() {
    if (visibility != View.GONE) {
        visibility = View.GONE
    }
}

fun View.enable() {
    isEnabled = true
}

fun View.disable() {
    isEnabled = false
}
