package com.example.bot_chos

import android.util.Log
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONObject

val client = OkHttpClient()

fun sendReq(path: String, reqInfo: JSONObject){

    val mediaType = "application/json; charset=utf-8".toMediaType()
    val requestBody = reqInfo.toString().toRequestBody(mediaType)

    val request = Request.Builder()
        .url(path)
        .post(requestBody)
        .build()

    Log.d("sdji", "AILSASDJAPOSADIDAPI")
    Thread{
        client.newCall(request).execute()
            .use {
                response ->
                if(response.isSuccessful){
                    Log.d("HTTP", response.body?.string() ?: "")
                }
                else{
                    Log.d("HTTP", "Failed")
                }
            }
    }.start()

}



fun sendAuthReq(username: String, password: String, email: String, action: String ){

    Log.d("sign up","Yaa")
    var url: String
    if (action == "Sign Up"){
        url = "signUp";
    }
    else{
        url = "logIn";
    }

    val ip = "192.168.0.199"
    val port = ":5000/"

    val path = "http://" + ip + port + url
    Log.d("path","created")

    val jsonBody = JSONObject().apply {
        put("username", username)
        put("password", password)
        put("email", email)
    }
    Log.d("Body", "created")

    sendReq(path, jsonBody)


}