package com.hagerfamily.soundbytes;

import android.content.SharedPreferences;

public class LoginManager {

    public SharedPreferences clientTokensSp;
    public SharedPreferences loginSp;

    LoginManager (SharedPreferences clientTokensSp, SharedPreferences loginSp) {
        this.clientTokensSp = clientTokensSp;
        this.loginSp = loginSp;
    }

    public SharedPreferences.Editor clientTokensEdit() {
        return clientTokensSp.edit();
    }
}
