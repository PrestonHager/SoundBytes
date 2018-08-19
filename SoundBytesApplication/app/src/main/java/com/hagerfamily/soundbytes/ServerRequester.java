package com.hagerfamily.soundbytes;

import org.json.JSONObject;

import java.io.OutputStreamWriter;
import java.net.URL;

import javax.net.ssl.HttpsURLConnection;

public class ServerRequester {
    public JSONObject JSONRequest(JSONObject json, String url) {
        try {
            String jsonString = json.toString();

            URL urlConnection = new URL(url);
            HttpsURLConnection request = (HttpsURLConnection) urlConnection.openConnection();

            request.setRequestMethod("POST");
            request.setRequestProperty("Content-Type", "application/json;charset=UTF-8");
            request.setRequestProperty("Accept", "application/json");
            request.setDoOutput(true);
            request.setDoInput(true);

            OutputStreamWriter os = new OutputStreamWriter(request.getOutputStream());
            os.write(jsonString);
            os.close();

            return new JSONObject(request.getResponseMessage());
        } catch (Exception e) {
            e.printStackTrace();
            return new JSONObject();
        }
    }
}
