package com.hagerfamily.soundbytes;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.net.Uri;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;

import java.util.Objects;

import static android.content.Context.MODE_PRIVATE;

public class SettingsFragment extends Fragment {
    public SettingsFragment() {}

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.settings_fragment, container, false);
        Button logoutButton = view.findViewById(R.id.logoutButton);
        logoutButton.setOnClickListener(new View.OnClickListener() {
            private SharedPreferences sp = Objects.requireNonNull(getContext()).getSharedPreferences("Login", MODE_PRIVATE);;
            private SharedPreferences.Editor spEditor = sp.edit();
            @Override
            public void onClick(View v) {
                spEditor.remove("Username");
                spEditor.remove("Password");
                spEditor.apply();
                Log.i("Settings", "Logged out of current account. Now moving to login activity.");
                Intent loginActivityIntent = new Intent(getContext(), LoginActivity.class);
                startActivity(loginActivityIntent);
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
