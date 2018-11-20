package com.hagerfamily.soundbytes;

import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.DataOutputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.URL;
import java.util.Iterator;
import java.util.logging.Level;
import java.util.logging.Logger;

import javax.net.ssl.HttpsURLConnection;

class ServerRequester {
    public class Request extends Thread {
        private String url;
        private String method;
        private String contentType;
        private String acceptType;
        private String data;
        private JSONObject headers = new JSONObject();
        private Integer responseCode;
        private String response;
        private Boolean sendData;

        public void run() {
            try {
                URL urlConnection = new URL(url);
                HttpsURLConnection request = (HttpsURLConnection) urlConnection.openConnection();

                request.setRequestMethod(method);
                request.setDoOutput(true);
                request.setRequestProperty("Content-Type", contentType);
                request.setRequestProperty("User-Agent", "Mozilla/5.0 (Android; Linux x86_64; compatible)");
                request.setRequestProperty("Accept", acceptType);

                Iterator<String> keys = headers.keys();
                while (keys.hasNext()) {
                    String key = keys.next();
                    request.setRequestProperty(key, headers.getString(key));
                }

                if (sendData) {
                    OutputStream os = request.getOutputStream();
                    DataOutputStream writer = new DataOutputStream(request.getOutputStream());
                    writer.writeBytes(data);
                    writer.flush();
                    writer.close();
                    os.close();
                    request.connect();
                }

                responseCode = request.getResponseCode();
                if (responseCode >= 200 && responseCode < 300) {
                    BufferedReader input = new BufferedReader(
                            new InputStreamReader(request.getInputStream()));
                    String inputLine;
                    StringBuilder responseBuffer = new StringBuilder();

                    while ((inputLine = input.readLine()) != null) {
                        responseBuffer.append(inputLine);
                    }
                    input.close();
                    response = responseBuffer.toString();
                } else {
                    throw new Exception("Bad Response Code. Returned "+responseCode.toString()+" code, expected 2xx.");
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        }

        Request(String url, String method, String contentType, String acceptType, JSONObject headers) {
            this.url = url;
            this.method = method;
            this.contentType = contentType;
            this.acceptType = acceptType;
            this.headers = headers;
            this.sendData = false;
            start();
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

        private String getResponse() {
            return response;
        }
        private Integer getResponseCode() {
            return responseCode;
        }
    }

    JSONObject GetRequest(JSONObject headers, String url) {
        try {
            Request request = new Request(url, "GET", "text/plain", "application/json", headers);
            request.join();
            String response = request.getResponse();
            if (request.getResponseCode() >= 200 && request.getResponseCode() < 300) {
                return new JSONObject(response);
            } else {
                return new JSONObject();
            }
        } catch (Exception e) {
            e.printStackTrace();
            return new JSONObject();
        }
    }

    JSONObject JSONRequest(JSONObject json, String url) {
        try {
            String jsonString = json.toString();

            Request request = new Request(url, "POST", "application/json", "application/json", jsonString);
            request.join();
            String response = request.getResponse();
            if (request.getResponseCode() >= 200 && request.getResponseCode() < 300) {
                return new JSONObject(response);
            }
            else {
                return new JSONObject();
            }
        } catch (Exception e) {
            e.printStackTrace();
            return new JSONObject();
        }
    }
}
