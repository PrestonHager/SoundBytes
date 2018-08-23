package com.hagerfamily.soundbytes;

import org.json.JSONObject;

import java.io.BufferedWriter;
import java.io.OutputStream;
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
        private Integer responseCode;
        private String response;
        private Boolean sendData;

        public void run() {
            try {
                URL urlConnection = new URL(url);
                HttpsURLConnection request = (HttpsURLConnection) urlConnection.openConnection();

                request.setRequestMethod(method);
                request.setRequestProperty("Content-Type", contentType);
                request.setRequestProperty("Accept", acceptType);
                request.setDoOutput(sendData);
                request.setDoInput(true);

                OutputStream os = request.getOutputStream();
                BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(os, "UTF-8"));
                writer.write(data);
                writer.flush();
                writer.close();
                os.close();
                request.connect();

                responseCode = request.getResponseCode();
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
            this.sendData = true;
            start();
        }
        Request(String url, String method, String contentType, String acceptType) {
            this.url = url;
            this.method = method;
            this.contentType = contentType;
            this.acceptType = acceptType;
            start();
        }

        private String getResponse() {
            return response;
        }
        private Integer getResponseCode() {
            return responseCode;
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
