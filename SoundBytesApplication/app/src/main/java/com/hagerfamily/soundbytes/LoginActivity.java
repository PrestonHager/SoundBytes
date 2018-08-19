package com.hagerfamily.soundbytes;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;

import org.json.JSONObject;

public class LoginActivity extends AppCompatActivity {

    private SharedPreferences sp;
    private SharedPreferences.Editor spEditor;
    private ServerRequester requester = new ServerRequester();
    private TextView errorTextView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        sp = getSharedPreferences("ClientTokens", MODE_PRIVATE);

        findViewById(R.id.usernameEntry).requestFocus();
        errorTextView = findViewById(R.id.errorTextView);
    }

    @Override
    public void onBackPressed() {
        // do nothing when the back button is pressed.
    }

    public void onLoginButtonPressed(View v) {
        EditText usernameEntry = findViewById(R.id.usernameEntry);
        EditText passwordEntry = findViewById(R.id.passwordEntry);
        String username = usernameEntry.getText().toString();
        String password = passwordEntry.getText().toString();
        try {
            JSONObject loginTokens = loginRequest(username, password);
            if (loginTokens.getInt("cod") > 100) {
                spEditor = sp.edit();
                spEditor.putString("AccessToken", loginTokens.getString("id"));
                spEditor.putString("RefreshToken", loginTokens.getString("rt"));
                spEditor.putInt("IssuedAt", loginTokens.getInt("iat"));
                spEditor.putInt("ExpiresAt", loginTokens.getInt("exp"));
                spEditor.apply();
                Intent mainActivityIntent = new Intent(this, MainActivity.class);
                startActivity(mainActivityIntent);
            } else {
                String error = loginTokens.getString("err");
                String code = String.format("%s", loginTokens.getInt("cod"));
                String errorMsg = R.string.error_default + " (" + code + ") " + error;
                errorTextView.setText(errorMsg);
                errorTextView.setVisibility(View.VISIBLE);
            }
        } catch (Exception e) {
            e.printStackTrace();
            errorTextView.setText(R.string.error_connection);
            errorTextView.setVisibility(View.VISIBLE);
        }
    }

    public void onSignupButtonPressed(View v) {
        // first make sure the passwords match.
        EditText passwordEntry = findViewById(R.id.passwordEntrySignup);
        EditText passwordEntryVerify = findViewById(R.id.passwordEntryVerifySignup);
        String password = passwordEntry.getText().toString();
        String passwordVerify = passwordEntryVerify.getText().toString();
        if (password != passwordVerify) {
            return;
        }
        // otherwise send a request with all the info to the authentication server.
        EditText usernameEntry = findViewById(R.id.usernameEntrySignup);
        EditText emailEntry = findViewById(R.id.emailEntrySignup);
        String username = usernameEntry.getText().toString();
        String email = emailEntry.getText().toString();
        try {
            JSONObject signupRequest = signupRequest(username, password, email);
            if (signupRequest.getInt("cod") > 100) {
                JSONObject loginTokens = loginRequest(username, password);
                spEditor = sp.edit();
                spEditor.putString("AccessToken", loginTokens.getString("id"));
                spEditor.putString("RefreshToken", loginTokens.getString("rt"));
                spEditor.putInt("IssuedAt", loginTokens.getInt("iat"));
                spEditor.putInt("ExpiresAt", loginTokens.getInt("exp"));
                spEditor.apply();
                Intent mainActivityIntent = new Intent(this, MainActivity.class);
                startActivity(mainActivityIntent);
            } else {
                // error is displayed.
                String error = signupRequest.getString("err");
                String code = String.format("%s", signupRequest.getInt("cod"));
                String errorMsg = "Error (" + code + ") " + error;
                errorTextView.setText(errorMsg);
                errorTextView.setVisibility(View.VISIBLE);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private JSONObject loginRequest(String username, String password) {
        try {
            JSONObject json = new JSONObject();
            json.put("protocolVersion", "1.0");
            json.put("username", username);
            json.put("password", password);

            return requester.JSONRequest(json, "https://faidg1ey0l.execute-api.us-west-2.amazonaws.com/prod/auth");
        } catch (Exception e) {
            e.printStackTrace();
            return new JSONObject();
        }
    }

    private JSONObject signupRequest(String username, String password, String email) {
        try {
            JSONObject json = new JSONObject();
            json.put("protocolVersion", "1.0");
            json.put("username", username);
            json.put("password", password);
            json.put("email", email);

            return requester.JSONRequest(json, "https://faidg1ey0l.execute-api.us-west-2.amazonaws.com/prod/create-account");
        } catch (Exception e) {
            e.printStackTrace();
            return new JSONObject();
        }
    }
}
