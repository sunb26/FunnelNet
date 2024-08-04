package net.jobayer.murmurdetector.ui.activities

import android.app.Activity
import android.content.Intent
import android.content.pm.PackageManager
import android.content.res.ColorStateList
import android.graphics.Color
import android.net.Uri
import android.os.Bundle
import android.provider.MediaStore
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.lifecycle.lifecycleScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import net.jobayer.murmurdetector.Const.PERMISSION_REQUEST_CODE
import net.jobayer.murmurdetector.R
import net.jobayer.murmurdetector.data.Const.PING_RESPONSE_ALIVE
import net.jobayer.murmurdetector.data.Const.TFLITE_MODEL_NAME
import net.jobayer.murmurdetector.data.api.HeartSoundApi
import net.jobayer.murmurdetector.data.model.PingResponse
import net.jobayer.murmurdetector.data.utils.NetUtil
import net.jobayer.murmurdetector.data.utils.appendText
import net.jobayer.murmurdetector.data.utils.disable
import net.jobayer.murmurdetector.data.utils.dismissDialog
import net.jobayer.murmurdetector.data.utils.enable
import net.jobayer.murmurdetector.data.utils.finalResult
import net.jobayer.murmurdetector.data.utils.getFileName
import net.jobayer.murmurdetector.data.utils.getInterpreter
import net.jobayer.murmurdetector.data.utils.getMultipartFromUri
import net.jobayer.murmurdetector.data.utils.getPermissionList
import net.jobayer.murmurdetector.data.utils.gone
import net.jobayer.murmurdetector.data.utils.isNetAvailable
import net.jobayer.murmurdetector.data.utils.loadingDialog
import net.jobayer.murmurdetector.data.utils.makeScrollable
import net.jobayer.murmurdetector.data.utils.onClick
import net.jobayer.murmurdetector.data.utils.openAppSettings
import net.jobayer.murmurdetector.data.utils.permissionGranted
import net.jobayer.murmurdetector.data.utils.predict
import net.jobayer.murmurdetector.data.utils.showDialog
import net.jobayer.murmurdetector.data.utils.toast
import net.jobayer.murmurdetector.data.utils.visible
import net.jobayer.murmurdetector.databinding.ActivityMainBinding
import org.tensorflow.lite.Interpreter

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding

    private lateinit var loadingDialog: AlertDialog

    private val audioFilePickerLauncher =
        registerForActivityResult(ActivityResultContracts.StartActivityForResult()) {
            if (it.resultCode == Activity.RESULT_OK) {
                it.data?.data?.let { audioUri ->
                    val mimeType = contentResolver.getType(audioUri)
                    if (mimeType != null && mimeType.startsWith("audio/")) {
                        log("Selected audio file: ${getFileName(audioUri)}", Color.LTGRAY)
                        uploadSample(audioUri)
                    } else log("Not an audio file!", getColor(R.color.red_orange))
                }
            } else log("No audio file selected!", getColor(R.color.red_orange))
        }

    private lateinit var heartSoundApi: HeartSoundApi

    private var interpreter: Interpreter? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }
        init()
    }

    private fun init() {
        log("App started!", Color.LTGRAY)
        initUi()
        checkForPermission()
        initVars()
        checkServerStatus()
        initTfLiteModel()
    }

    private fun initUi() {
        loadingDialog = loadingDialog()
        with(binding) {
            log.makeScrollable()
            selectBtn.onClick { openAudioSelector() }
        }
    }

    private fun initVars() {
        heartSoundApi = NetUtil.heartSoundApi
    }

    private fun checkServerStatus() {
        if (!isNetAvailable()) {
            log("No internet connection!", getColor(R.color.red_orange))
            return
        }

        log("Checking server status...", Color.LTGRAY)
        loadingDialog.showDialog()
        lifecycleScope.launch {
            val pingResponse = heartSoundApi.ping().body()
            launch(Dispatchers.Main) {
                loadingDialog.dismissDialog()
                handleServerPing(pingResponse)
            }
        }
    }

    private fun handleServerPing(response: PingResponse?) {
        if (response != null) {
            if (response.msg.isNotEmpty()) {
                with(binding) {
                    serverStatusText.text = response.msg
                    val alive = response.msg.lowercase() == PING_RESPONSE_ALIVE
                    if (alive) {
                        log("Server is ready!", getColor(R.color.flat_green))
                        helperText.text = getString(R.string.select_an_audio_file_to_predict)
                        serverStatusIcon.imageTintList = ColorStateList.valueOf(getColor(R.color.flat_green))
                    } else {
                        helperText.text = getString(R.string.please_try_after_some_time)
                        log("Server is not responding!", getColor(R.color.red_orange))
                    }
                    selectBtn.isEnabled = alive
                }
            } else {
                binding.helperText.text = getString(R.string.please_try_after_some_time)
                log("Failed to check server status!", getColor(R.color.red_orange))
            }
        } else {
            binding.helperText.text = getString(R.string.please_try_after_some_time)
            log("Failed to check server status!", getColor(R.color.red_orange))
        }
    }

    private fun uploadSample(uri: Uri) {
        log("Uploading audio...", Color.LTGRAY)
        with(binding) {
            progressbar.visible()
            selectBtn.disable()
            helperText.text = getString(R.string.waiting_to_be_preprocessed)
            lifecycleScope.launch {
                val part = getMultipartFromUri(uri)
                val response = heartSoundApi.processAudio(part)
                launch(Dispatchers.Main) {
                    log("Audio processed successfully!", getColor(R.color.flat_green))
                    if (response.isSuccessful) {
                        val result = response.body()
                        if (result != null) {
                            val data = result.data
                            makeInference(data)
                        } else {
                            progressbar.gone()
                            selectBtn.enable()
                            helperText.text = getString(R.string.please_try_again)
                            log("Failed to preprocess audio!", getColor(R.color.red_orange))
                            log("Please try again!", Color.LTGRAY)
                        }
                    } else {
                        progressbar.gone()
                        selectBtn.enable()
                        helperText.text = getString(R.string.please_try_again)
                        log("Failed to preprocess audio!", getColor(R.color.red_orange))
                        log("Please try again!", Color.LTGRAY)
                    }
                }
            }
        }
    }

    private fun initTfLiteModel() {
        interpreter = getInterpreter(TFLITE_MODEL_NAME)
    }

    private fun makeInference(data: String) {
        with(binding) {
            if (interpreter == null) {
                log("Model not loaded!", getColor(R.color.red_orange))
                return
            }

            helperText.text = getString(R.string.making_inference)
            log("Making inference...", Color.LTGRAY)

            val resultArray = interpreter!!.predict(data)

            val result = finalResult(resultArray)

            status.text = result.toString()

            helperText.text = getString(R.string.inference_completed)
            log("Predicted label: $result", getColor(R.color.flat_green))

            progressbar.gone()
            selectBtn.enable()
        }
    }

    private fun openAudioSelector() {
        val permissions = getPermissionList()
        if (!permissionGranted(*permissions)) {
            log("Please grant all the required permission!", Color.YELLOW)
            requestPermissions(permissions, PERMISSION_REQUEST_CODE)
            return
        }

        log("Waiting for audio file...", Color.LTGRAY)

        val intent = Intent(Intent.ACTION_PICK, MediaStore.Audio.Media.EXTERNAL_CONTENT_URI)
        audioFilePickerLauncher.launch(intent)
    }

    private fun log(message: String, color: Int) {
        binding.log.appendText(message, color, binding.logcatHolder)
    }

    private fun checkForPermission() {
        val permissions = getPermissionList()
        if (!permissionGranted(*permissions)) {
            requestPermissions(permissions, PERMISSION_REQUEST_CODE)
        } else log("All permissions granted!", getColor(R.color.flat_green))
    }

    private fun updatePermissionResult(granted: Boolean) {
        with(binding) {
            selectBtn.isEnabled = granted
        }
        if (!granted) {
            toast("Please grant all the required permission!")
            openAppSettings()
        } else { log("All permissions granted!", getColor(R.color.flat_green)) }
    }

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == PERMISSION_REQUEST_CODE) {
            if (grantResults.isNotEmpty()) {
                var granted = false
                grantResults.forEach {
                    granted = it == PackageManager.PERMISSION_GRANTED
                }
                updatePermissionResult(granted)
            } else updatePermissionResult(false)
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        interpreter?.close()
    }

}