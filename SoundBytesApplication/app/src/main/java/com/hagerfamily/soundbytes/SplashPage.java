package com.hagerfamily.soundbytes;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;

import org.json.JSONObject;

import java.io.DataOutputStream;
import java.net.URL;

import javax.net.ssl.HttpsURLConnection;

public class SplashPage extends AppCompatActivity {

    private SharedPreferences sp;
    private SharedPreferences sp2;
    private SharedPreferences.Editor spEditor;
    private ServerRequester requester = new ServerRequester();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_splash_page);

        // Get the SharedPreferences instance for login data.
        sp = getSharedPreferences("Login", MODE_PRIVATE);
        sp2 = getSharedPreferences("ClientTokens", MODE_PRIVATE);
        spEditor = sp2.edit();
        // Find the current values.
        String username = sp.getString("Username", null);
        String password = sp.getString("Password", null);
        // If the user has not logged in before, or is logged out.
        if (username == null || password == null) {
            Intent loginIntent = new Intent(this, LoginActivity.class);
            startActivity(loginIntent);
        } else {
            // If the user is logged in then request an access token and go to the main activity.
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
}
