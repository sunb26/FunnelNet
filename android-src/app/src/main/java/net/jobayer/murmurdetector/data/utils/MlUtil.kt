package net.jobayer.murmurdetector.data.utils

import android.app.Activity
import com.google.gson.Gson
import com.google.gson.reflect.TypeToken
import org.tensorflow.lite.Interpreter
import org.tensorflow.lite.support.tensorbuffer.TensorBuffer
import java.io.FileInputStream
import java.nio.MappedByteBuffer
import java.nio.channels.FileChannel

fun Interpreter.predict(data: String): FloatArray {
    val inputTensor = getInputTensor(0)
    val outputTensor = getOutputTensor(0)

    val inputShape = inputTensor.shape()
    val inputDataType = inputTensor.dataType()
    val outputShape = outputTensor.shape()
    val outputDataType = outputTensor.dataType()

    val input = data.getDataAsArray()

    val flatInput = input.flatMap { it.flatten() }.toFloatArray()

    val inputBuffer = TensorBuffer.createFixedSize(inputShape, inputDataType)
    inputBuffer.loadArray(flatInput)

    val outputBuffer = TensorBuffer.createFixedSize(outputShape, outputDataType)

    run(inputBuffer.buffer, outputBuffer.buffer.rewind())

    return outputBuffer.floatArray
}

private fun String.getDataAsArray(): Array<Array<Array<Float>>> {
    val gson = Gson()
    val type = object : TypeToken<Array<Array<Array<Double>>>>() {}.type
    val doubleArray = gson.fromJson<Array<Array<Array<Double>>>>(this, type)

    return doubleArray.map {
        it.map { i ->
            i.map { d ->
                d.toFloat()
            }.toTypedArray()
        }.toTypedArray()
    }.toTypedArray()
}

fun Activity.getInterpreter(modelName: String): Interpreter {
    val model = loadModelFile(modelName)
    return Interpreter(model)
}

private fun Activity.loadModelFile(model: String): MappedByteBuffer {
    val assetDescriptor = assets.openFd(model)
    val inputStream = FileInputStream(assetDescriptor.fileDescriptor)
    val fileChannel = inputStream.channel
    val startOffset = assetDescriptor.startOffset
    val declaredLength = assetDescriptor.declaredLength
    return fileChannel.map(FileChannel.MapMode.READ_ONLY, startOffset, declaredLength)
}

fun finalResult(pred: FloatArray): Int {
    return if (pred.size == 1) {
        return if (pred[0] >= 0.5) 1 else 0
    } else argMax(pred)
}

private fun argMax(elements: FloatArray): Int {
    var maxIndex = 0
    for (i in 1 until elements.size) {
        if (elements[i] > elements[maxIndex]) {
            maxIndex = i
        }
    }
    return maxIndex
}