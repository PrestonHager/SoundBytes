package com.hagerfamily.soundbytes;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.EditText;

import org.json.JSONObject;

import java.io.DataOutputStream;
import java.net.URL;

import javax.net.ssl.HttpsURLConnection;

public class LoginActivity extends AppCompatActivity {

    private SharedPreferences sp;
    private SharedPreferences.Editor spEditor;
    private ServerRequester requester = new ServerRequester();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        sp = getSharedPreferences("ClientTokens", MODE_PRIVATE);
        spEditor = sp.edit();
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
            spEditor.putString("AccessToken", loginTokens.getString("id"));
            spEditor.putString("RefreshToken", loginTokens.getString("rt"));
            spEditor.putInt("IssuedAt", loginTokens.getInt("iat"));
            spEditor.putInt("ExpiresAt", loginTokens.getInt("exp"));
        } catch (Exception e) {
            e.printStackTrace();
            Intent loginIntent = new Intent(this, LoginActivity.class);
            startActivity(loginIntent);
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
                spEditor.putString("AccessToken", loginTokens.getString("id"));
                spEditor.putString("RefreshToken", loginTokens.getString("rt"));
                spEditor.putInt("IssuedAt", loginTokens.getInt("iat"));
                spEditor.putInt("ExpiresAt", loginTokens.getInt("exp"));
            } else {
                // error is displayed.
                String error = signupRequest.getString("err");
            }
        } catch (Exception e) {
            e.printStackTrace();
            return;
        }
    }

    private JSONObject loginRequest(String username, String password) {
        try {
            JSONObject json = new JSONObject();
            json.put("protocolVersion", "1.0");
            json.put("username", username);
            json.put("password", password);

            return requester.JSONrequest(json, "https://nj0okdeivk.execute-api.us-west-2.amazonaws.com/prod/auth");
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

            return requester.JSONrequest(json, "https://nj0okdeivk.execute-api.us-west-2.amazonaws.com/prod/create-account");
        } catch (Exception e) {
            e.printStackTrace();
            return new JSONObject();
        }
    }
}
