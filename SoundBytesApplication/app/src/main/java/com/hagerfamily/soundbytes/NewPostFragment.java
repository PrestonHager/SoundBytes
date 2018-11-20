package com.hagerfamily.soundbytes;

import android.annotation.SuppressLint;
import android.content.Context;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.MotionEvent;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;

public class NewPostFragment extends Fragment {
    public NewPostFragment() {}

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }

    @SuppressLint("ClickableViewAccessibility")
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.new_post_fragment, container, false);
        Button recordButton = view.findViewById(R.id.newPostButton);
        recordButton.setOnTouchListener(new View.OnTouchListener() {
            private boolean stopRecording;
            private Long startTime;
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                if (event.getAction() == MotionEvent.ACTION_DOWN && !stopRecording) {
                    startTime = System.currentTimeMillis();
                    Log.i("NewPost","Started recording.");
                    // start recording.
                } else if (event.getAction() == MotionEvent.ACTION_UP) {
                    v.performClick();
                    Long endTime = System.currentTimeMillis();
                    if (endTime - startTime >= 3000) {
                        // end the recording and make new clip.
                        Log.i("NewPost","Ended recording and made a new clip.");
                        stopRecording = true;
                    } else if (stopRecording) {
                        // stop the recording and make new clip.
                        Log.i("NewPost","Ended recording and made a new clip.");
                    }
                    stopRecording = !stopRecording;
                    // keep recording until button pressed again.
                }
                return false;
            }
        });
        return view;
    }

    @Override
    public void onAttach(Context context) {
        super.onAttach(context);
    }

    @Override
    public void onDetach() {
        super.onDetach();
    }
}
