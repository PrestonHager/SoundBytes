package com.hagerfamily.soundbytes;

import org.json.JSONObject;

import java.io.OutputStreamWriter;
import java.net.URL;

import javax.net.ssl.HttpsURLConnection;

public class ServerRequester {
    public class Request extends Thread {
        private String url;
        private String method;
        private String contentType;
        private String acceptType;
        private String data;
        private String response;

        public void run() {
            try {
                URL urlConnection = new URL(url);
                HttpsURLConnection request = (HttpsURLConnection) urlConnection.openConnection();

                request.setRequestMethod(method);
                request.setRequestProperty("Content-Type", contentType);
                request.setRequestProperty("Accept", acceptType);
                request.setDoOutput(true);
                request.setDoInput(true);

                OutputStreamWriter os = new OutputStreamWriter(request.getOutputStream());
                os.write(data);
                os.close();

                response = request.getResponseMessage();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }

        Request(String url, String method, String contentType, String acceptType, String data) {
            this.url = url;
            this.method = method;
            this.contentType = contentType;
            this.acceptType = acceptType;
            this.data = data;
            start();
        }

        private String getResponse() {
            return response;
        }
    }

    public JSONObject JSONRequest(JSONObject json, String url) {
        try {
            String jsonString = json.toString();

            Request request = new Request(url, "POST", "application/json", "application/json", jsonString);
            request.join();
            return new JSONObject(request.getResponse());
        } catch (Exception e) {
            e.printStackTrace();
            return new JSONObject();
        }
    }
}
