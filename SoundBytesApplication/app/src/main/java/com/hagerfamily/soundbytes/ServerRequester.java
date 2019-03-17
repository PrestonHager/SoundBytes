package com.hagerfamily.soundbytes;

import android.content.Context;
import org.json.JSONException;
import org.json.JSONObject;
import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.URL;
import java.nio.Buffer;
import java.util.Iterator;
import javax.net.ssl.HttpsURLConnection;

class ServerRequester {
    private Context context;

    public class Request extends Thread {
        private String url;
        private String method;
        private String contentType;
        private String acceptType;
        private String data;
        private JSONObject params = new JSONObject();
        private Integer responseCode;
        private String response;
        private Boolean sendData;

        public void run() {
            try {
                URL urlConnection;
                if (params.length() > 0) {
                    StringBuilder paramsString = new StringBuilder().append("?");
                    Iterator<String> keys = params.keys();
                    while (keys.hasNext()) {
                        String key = keys.next();
                        if (paramsString.length() != 1) {
                            paramsString.append("&");
                        }
                        paramsString.append(key).append("=").append(params.getString(key));
                    }
                    urlConnection = new URL(url+paramsString.toString());
                } else {
                    urlConnection = new URL(url);
                }
                HttpsURLConnection request = (HttpsURLConnection) urlConnection.openConnection();

                request.setRequestMethod(method);
                request.setDoOutput(true);
                request.setRequestProperty("Content-Type", contentType);
                request.setRequestProperty("Accept", acceptType);
                request.setRequestProperty("Authorization", "");

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
                BufferedReader input;
                if (responseCode >= 200 && responseCode < 300) {
                    input = new BufferedReader(new InputStreamReader(request.getInputStream()));
                } else {
                    input = new BufferedReader(new InputStreamReader(request.getErrorStream()));
                }
                String inputLine;
                StringBuilder responseBuffer = new StringBuilder();

                while ((inputLine = input.readLine()) != null) {
                    responseBuffer.append(inputLine);
                }
                input.close();
                response = responseBuffer.toString();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }

        Request(String url, String method, String contentType, String acceptType, JSONObject params) {
            this.url = url;
            this.method = method;
            this.contentType = contentType;
            this.acceptType = acceptType;
            this.params = params;
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

        String getResponse() {
            return response;
        }
    }

    ServerRequester(Context context) {
        this.context = context;
    }

    JSONObject getNewJSONObjectWithError(Integer error) {
        try {
            return new JSONObject().put("cod", -1).put("err", context.getString(error));
        } catch (JSONException e) {
            e.printStackTrace();
            return new JSONObject();
        }
    }

    JSONObject GetRequest(JSONObject params, String url) {
        try {
            Request request = new Request(url, "GET", "text/plain", "application/json", params);
            request.join();
            String response = request.getResponse();
            return new JSONObject(response);
        } catch (Exception e) {
            e.printStackTrace();
            return getNewJSONObjectWithError(R.string.error_unknown);
        }
    }

    JSONObject JSONRequest(JSONObject json, String url) {
        try {
            String jsonString = json.toString();

            Request request = new Request(url, "POST", "application/json", "application/json", jsonString);
            request.join();
            String response = request.getResponse();
            return new JSONObject(response);
        } catch (Exception e) {
            e.printStackTrace();
            return getNewJSONObjectWithError(R.string.error_unknown);
        }
    }
}
