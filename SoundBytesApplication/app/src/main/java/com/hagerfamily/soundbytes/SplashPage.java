package com.hagerfamily.soundbytes;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;

import org.json.JSONObject;

public class SplashPage extends AppCompatActivity {

    private ServerRequester requester = new ServerRequester();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_splash_page);

        // Get the SharedPreferences instance for login data.
        SharedPreferences sp = getSharedPreferences("Login", MODE_PRIVATE);
        SharedPreferences sp2 = getSharedPreferences("ClientTokens", MODE_PRIVATE);
        SharedPreferences.Editor spEditor = sp2.edit();
        // Find the current values.
        String username = sp.getString("Username", null);
        String password = sp.getString("Password", null);
        // If the user has not logged in before, or is logged out.
        if (username == null || password == null) {
            Intent loginIntent = new Intent(this, LoginActivity.class);
            startActivity(loginIntent);
        } else {
            // If the tokens are still valid, there is no use in requesting more tokens.
            if (!sp2.getString("AccessToken", "").isEmpty() && !sp2.getString("RefreshToken", "").isEmpty()) {
                // check the expire time to the current time.
                if (sp2.getInt("IssuedAt", 0)+3600 > System.currentTimeMillis()/1000) {
                    // if all these succeed then the tokens are still valid, and we move to the main activity.
                    Log.i("SplashPage", "Tokens already exist. Moving to main activity.");
                    Intent mainActivityIntent = new Intent(this, MainActivity.class);
                    startActivity(mainActivityIntent);
                    return;
                }
            }
            // If the user is logged in then request an access token and go to the main activity.
            try {
                JSONObject loginTokens = loginRequest(username, password);
                spEditor.putString("AccessToken", loginTokens.getString("id"));
                spEditor.putString("RefreshToken", loginTokens.getString("rt"));
                spEditor.putInt("IssuedAt", loginTokens.getInt("iat"));
                spEditor.putInt("ExpiresIn", loginTokens.getInt("exp"));
                spEditor.apply();
                Log.i("SplashPage", "Logged in, now moving to main activity.");
                Intent mainActivityIntent = new Intent(this, MainActivity.class);
                startActivity(mainActivityIntent);
            } catch (Exception e) {
                e.printStackTrace();
                Log.i("SplashPage", "Failed to log in, now moving to login activity.");
                Intent loginIntent = new Intent(this, LoginActivity.class);
                startActivity(loginIntent);
            }
        }
    }

    private JSONObject loginRequest(String username, String password) {
        try {
            JSONObject json = new JSONObject();
            json.put("username", username);
            json.put("password", password);

            return requester.JSONRequest(json, "https://faidg1ey0l.execute-api.us-west-2.amazonaws.com/prod/auth");
        } catch (Exception e) {
            e.printStackTrace();
            return new JSONObject();
        }
    }
}
