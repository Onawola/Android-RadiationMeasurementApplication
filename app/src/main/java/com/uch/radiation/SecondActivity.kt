package com.uch.radiation

import android.content.Context
import android.os.Bundle
import android.text.method.ScrollingMovementMethod
import androidx.appcompat.app.AppCompatActivity
import kotlinx.android.synthetic.main.activity_second.*

class SecondActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_second)
        // calling the action bar
        val actionBar = supportActionBar

        // showing the back button in action bar
        actionBar?.let {
            // Customize the back button
            actionBar.setHomeAsUpIndicator(R.drawable.ic_baseline_arrow_back_white_24dp)
            actionBar.setDisplayHomeAsUpEnabled(true)
        }
        val sharedPreferences = getSharedPreferences(
            packageName + Constants.PREF_FILE_NAME,
            Context.MODE_PRIVATE
        )
        textView.text =
            sharedPreferences.getString(
                Constants.KEY_RECORDS,
                getString(R.string.no_records)
            )
        textView.movementMethod = ScrollingMovementMethod()
    }
}