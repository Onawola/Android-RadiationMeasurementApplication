package com.uch.radiation

import android.content.Context
import android.content.Intent
import android.content.SharedPreferences
import android.os.Bundle
import android.text.TextUtils
import android.view.Menu
import android.view.MenuItem
import android.view.View
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform
import kotlinx.android.synthetic.main.activity_main.*
import kotlinx.android.synthetic.main.content_main.*
import kotlin.properties.Delegates


class MainActivity : AppCompatActivity(), AdapterView.OnItemSelectedListener {
    private lateinit var measures: String
    private lateinit var answer: String
    private var leadValue: Float by Delegates.notNull()
    private var wedgeValue: Float by Delegates.notNull()
    private val activitySharedPreferences: SharedPreferences by lazy {
        getPreferences(
            Context.MODE_PRIVATE
        )
    }
    private val appSharedPreferences: SharedPreferences by lazy {
        getSharedPreferences(
            packageName + Constants.PREF_FILE_NAME,
            Context.MODE_PRIVATE
        )
    }

    private fun saveAccountData(
        doseRate: Float?,
        pid: Int?
    ) { // Save data to Activity Level SharedPrefs
        val editor: SharedPreferences.Editor = activitySharedPreferences.edit()
        editor.putFloat(Constants.KEY_DOSE_RATE, doseRate!!)
        val inc = pid?.inc()!!
        editor.putInt(Constants.KEY_SERIAL_NO, inc)
        serial_no.setText(inc.toString())

        editor.apply() // editor.commit()
    }

    private fun savePosition(
        position: Int,
        key: String
    ) { // Save data to Activity Level SharedPrefs
        val editor: SharedPreferences.Editor = activitySharedPreferences.edit()
        editor.putInt(key, position)
        editor.apply() // editor.commit()
    }

    private fun loadPosition(key: String): Int { // Load data from Activity Level SharedPrefs
        return activitySharedPreferences.getInt(key, 0)
    }

    private fun loadAccountData() { // Load data from Activity Level SharedPrefs
        val doseRateValue =
            activitySharedPreferences.getFloat(Constants.KEY_DOSE_RATE, 0.0f)
        dose_rate.setText(doseRateValue.toString())

        val serialNoValue =
            activitySharedPreferences.getInt(Constants.KEY_SERIAL_NO, 1)
        serial_no.setText(serialNoValue.toString())
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
//        setSupportActionBar(toolbar)
        btn_submit.setOnClickListener {
            if (TextUtils.isEmpty(point_a.text)) {
                point_a.error = getString(R.string.error_msg)
            }
            if (TextUtils.isEmpty(point_b.text)) {
                point_b.error = getString(R.string.error_msg)
            }
            if (TextUtils.isEmpty(depth.text)) {
                depth.error = getString(R.string.error_msg)
            }
            if (TextUtils.isEmpty(dose.text)) {
                dose.error = getString(R.string.error_msg)
            }
            if (TextUtils.isEmpty(dose_rate.text)) {
                dose_rate.error = getString(R.string.error_msg)
            }
            if (TextUtils.isEmpty(fraction.text)) {
                fraction.error = getString(R.string.error_msg)
            }
            if (!(TextUtils.isEmpty(point_a.text)
                        || TextUtils.isEmpty(point_b.text)
                        || TextUtils.isEmpty(depth.text)
                        || TextUtils.isEmpty(dose.text)
                        || TextUtils.isEmpty(dose_rate.text)
                        || TextUtils.isEmpty(fraction.text))
            ) {
                //proceed with operation
                patient_id.clearError()
                val doseRate: Float? = dose_rate.text.toString().toFloatOrNull()
                val serialNo: Int? = serial_no.text.toString().toIntOrNull()
                saveAccountData(doseRate, serialNo)
                val pointA: Float? = point_a.text.toString().toFloatOrNull()
                val pointB: Float? = point_b.text.toString().toFloatOrNull()
                val depth: Float? = depth.text.toString().toFloatOrNull()
                val dose: Float? = dose.text.toString().toFloatOrNull()
                val faction: Float? = fraction.text.toString().toFloatOrNull()
                answer = getPythonHelloWorld(
                    pointA,
                    pointB,
                    depth,
                    dose,
                    faction,
                    wedgeValue,
                    leadValue,
                    measures,
                    doseRate,
                    serialNo
                )
                hello_textview.text = answer
            }
        }
        btn_save.setOnClickListener {
            if (TextUtils.isEmpty(patient_id.text)) {
                patient_id.error = getString(R.string.error_msg)
            } else {
                if (this::answer.isInitialized) {
                    val patientOutput = getString(R.string.patient_result)
                    val pid = patient_id.text
                    val output = "$patientOutput $pid"
                    val recordsValue =
                        appSharedPreferences.getString(
                            Constants.KEY_RECORDS,
                            getString(R.string.no_records)
                        )
                    val sb = StringBuilder()
                    sb.appendLine(output).appendLine(answer)
                    if (recordsValue != getString(R.string.no_records)) {
                        sb.appendLine("-----------------------------------------")
                        sb.append(recordsValue)
                    }
                    val editor: SharedPreferences.Editor = appSharedPreferences.edit()
                    editor.putString(Constants.KEY_RECORDS, sb.toString())
                    editor.apply() // editor.commit()
                    Toast.makeText(
                        this@MainActivity,
                        getString(R.string.save_msg), Toast.LENGTH_SHORT
                    ).show()
                }
            }
        }
        initPython()
        spinner.onItemSelectedListener = this
        spinner_lead_value.onItemSelectedListener = this
        spinner_wedge_value.onItemSelectedListener = this
// Create an ArrayAdapter using the string array and a default spinner layout
        ArrayAdapter.createFromResource(
            this,
            R.array.measures,
            android.R.layout.simple_spinner_item
        ).also { adapter ->
            // Specify the layout to use when the list of choices appears
            adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
            // Apply the adapter to the spinner
            spinner.adapter = adapter
        }
// Create an ArrayAdapter using the string array and a default spinner layout
        ArrayAdapter.createFromResource(
            this,
            R.array.lead,
            android.R.layout.simple_spinner_item
        ).also { adapter ->
            // Specify the layout to use when the list of choices appears
            adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
            // Apply the adapter to the spinner
            spinner_lead_value.adapter = adapter
        }
// Create an ArrayAdapter using the string array and a default spinner layout
        ArrayAdapter.createFromResource(
            this,
            R.array.wedge,
            android.R.layout.simple_spinner_item
        ).also { adapter ->
            // Specify the layout to use when the list of choices appears
            adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
            // Apply the adapter to the spinner
            spinner_wedge_value.adapter = adapter
        }
        loadAccountData()
        val leadPosition = loadPosition(Constants.KEY_LEAD)
        val wedgePosition = loadPosition(Constants.KEY_WEDGE)
        val measuresPosition = loadPosition(Constants.KEY_MEASURES)
        spinner_lead_value.setSelection(leadPosition)
        spinner_wedge_value.setSelection(wedgePosition)
        spinner.setSelection(measuresPosition)
    }

    private fun initPython() {
        if (!Python.isStarted()) {
            Python.start(AndroidPlatform(this))
        }
    }

    private fun getPythonHelloWorld(
        point_a: Float?, point_b: Float?,
        depth: Float?, dose: Float?,
        faction: Float?,
        wedge_value: Float?,
        lead_value: Float?,
        measures: String,
        dose_value: Float?,
        serial_no_value: Int?
    ): String {
        val python = Python.getInstance()
        val pythonFile = python.getModule("EBRTcalculations")
        return pythonFile.callAttr(
            "helloworld",
            point_a,
            point_b,
            depth,
            dose,
            faction,
            wedge_value,
            lead_value,
            measures,
            dose_value,
            serial_no_value
        ).toString()
    }

    override fun onPause() {
        super.onPause()
        point_a.clearError()
        point_b.clearError()
        depth.clearError()
        dose.clearError()
        dose_rate.clearError()
        fraction.clearError()
        patient_id.clearError()
    }

    private fun EditText.clearError() {
        error = null
    }


    override fun onNothingSelected(p0: AdapterView<*>?) {
        TODO("Not yet implemented")
    }

    override fun onItemSelected(parent: AdapterView<*>?, p1: View?, position: Int, p3: Long) {
        val item: String = parent?.getItemAtPosition(position).toString()
        when (parent?.id) {
            R.id.spinner -> {
                savePosition(position, Constants.KEY_MEASURES)
                measures = item
                Toast.makeText(
                    this@MainActivity,
                    getString(R.string.selected_item) + " " +
                            "" + item, Toast.LENGTH_SHORT
                ).show()
            }
            R.id.spinner_lead_value -> {
                savePosition(position, Constants.KEY_LEAD)
                leadValue = when (item) {
                    getString(R.string.plain) -> 0.939f
                    getString(R.string.star_pattern) -> 0.957f
                    getString(R.string.slotted_pattern) -> 0.957f
                    getString(R.string.stripes_pattern) -> 0.981f
                    else -> 1f
                }
                Toast.makeText(
                    this@MainActivity,
                    getString(R.string.selected_item) + " " +
                            "" + item, Toast.LENGTH_SHORT
                ).show()
            }
            R.id.spinner_wedge_value -> {
                savePosition(position, Constants.KEY_WEDGE)
                wedgeValue = when (item) {
                    getString(R.string.fifteen_degrees) -> 0.665f
                    getString(R.string.thirty_degrees) -> 0.567f
                    getString(R.string.forty_five_degrees) -> 0.471f
                    getString(R.string.sixty_degrees) -> 0.371f
                    else -> 1f
                }
                Toast.makeText(
                    this@MainActivity,
                    getString(R.string.selected_item) + " " +
                            "" + item, Toast.LENGTH_SHORT
                ).show()
            }
        }
    }

    override fun onCreateOptionsMenu(menu: Menu): Boolean {
        // Inflate the menu; this adds items to the action bar if it is present.
        menuInflater.inflate(R.menu.menu_main, menu)
        return true
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        return when (item.itemId) {
            R.id.action_records -> {
                val intent = Intent(this, SecondActivity::class.java)
                startActivity(intent)
                true
            }
            R.id.action_clear -> {
                val sharedPreferencesEditor: SharedPreferences.Editor =
                    activitySharedPreferences.edit()
                sharedPreferencesEditor.remove(Constants.KEY_SERIAL_NO)
                sharedPreferencesEditor.apply()
                serial_no.setText("1")
                val spEditor: SharedPreferences.Editor = appSharedPreferences.edit()
                spEditor.clear()
                spEditor.apply()
                true
            }
            else -> super.onOptionsItemSelected(item)
        }
    }
}
