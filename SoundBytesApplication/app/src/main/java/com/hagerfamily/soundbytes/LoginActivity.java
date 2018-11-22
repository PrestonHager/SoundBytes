package com.hagerfamily.soundbytes;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;

import org.json.JSONObject;

public class LoginActivity extends AppCompatActivity {

    private SharedPreferences clientTokensSp;
    private SharedPreferences loginSp;
    private ServerRequester requester = new ServerRequester();
    private TextView errorTextView;
    private String urlAuthorize;
    private String urlCreateAccount;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        // set url variables.
        urlAuthorize = getString(R.string.url_auth);
        urlCreateAccount = getString(R.string.url_create_account);

        clientTokensSp = getSharedPreferences("ClientTokens", MODE_PRIVATE);
        loginSp = getSharedPreferences("Login", MODE_PRIVATE);

        findViewById(R.id.usernameEntry).requestFocus();
        errorTextView = findViewById(R.id.errorTextView);
    }

    @Override
    public void onBackPressed() {
        // exit the app when the back button is pressed.
        finish();
    }

    public void onLoginButtonPressed(View v) {
        EditText usernameEntry = findViewById(R.id.usernameEntry);
        EditText passwordEntry = findViewById(R.id.passwordEntry);
        String username = usernameEntry.getText().toString();
        String password = passwordEntry.getText().toString();
        try {
            JSONObject loginTokens = loginRequest(username, password);
            if (loginTokens.getInt("cod") >= 100) {
                SharedPreferences.Editor loginSpEditor = loginSp.edit();
                loginSpEditor.putString("Username", username);
                loginSpEditor.putString("Password", password);
                loginSpEditor.apply();
                SharedPreferences.Editor clientTokensSpEditor = clientTokensSp.edit();
                clientTokensSpEditor.putString("AccessToken", loginTokens.getString("id"));
                clientTokensSpEditor.putString("RefreshToken", loginTokens.getString("rt"));
                clientTokensSpEditor.putInt("IssuedAt", loginTokens.getInt("iat"));
                clientTokensSpEditor.putInt("ExpiresAt", loginTokens.getInt("exp")+loginTokens.getInt("iat"));
                clientTokensSpEditor.apply();
                Log.i("LoginActivity", "Logged in and set Tokens to storage. Now moving to main activity.");
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
        if (!password.equals(passwordVerify)) {
            errorTextView.setText(R.string.error_password_match);
            errorTextView.setVisibility(View.VISIBLE);
            return;
        }
        // otherwise send a request with all the info to the authentication server.
        EditText usernameEntry = findViewById(R.id.usernameEntrySignup);
        EditText emailEntry = findViewById(R.id.emailEntrySignup);
        String username = usernameEntry.getText().toString();
        String email = emailEntry.getText().toString();
        try {
            JSONObject signupRequest = signupRequest(username, password, email);
            if (signupRequest.getInt("cod") >= 100) {
                errorTextView.setText(R.string.signup_verify);
                errorTextView.setVisibility(View.VISIBLE);
            } else {
                String error = signupRequest.getString("err");
                String code = String.format("%s", signupRequest.getInt("cod"));
                String errorMsg = R.string.error_default + " (" + code + ") " + error;
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
            json.put("username", username);
            json.put("password", password);

            return requester.JSONRequest(json, urlAuthorize);
        } catch (Exception e) {
            e.printStackTrace();
            return new JSONObject();
        }
    }

    private JSONObject signupRequest(String username, String password, String email) {
        try {
            JSONObject json = new JSONObject();
            json.put("username", username);
            json.put("password", password);
            json.put("email", email);

            return requester.JSONRequest(json, urlCreateAccount);
        } catch (Exception e) {
            e.printStackTrace();
            return new JSONObject();
        }
    }
}
