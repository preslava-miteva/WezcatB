package com.example.bot_chos

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarColors
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import com.example.bot_chos.ui.theme.BotchosTheme
import com.example.bot_chos.TodoActivity
import android.content.Intent
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.width
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.NavigationBarItemDefaults
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.vectorResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp


var mainBackColor = 0xFFFCF6EB
var secondaryColor = 0xFFB7CFD2
var accentColor = 0xFF545F66


@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun TopNavBar(){
    //tuk se durji wremeto
    TopAppBar(
        title = {Text("navigation bar")},
        colors = TopAppBarDefaults.topAppBarColors(
            containerColor = Color(0xFFFCF6EB),
            titleContentColor = Color(0xFFB7CFD2)
        ),
        modifier = Modifier
            .padding(horizontal = 16.dp, vertical = 30.dp)
            .clip(RoundedCornerShape(size = 24.dp))
            .border(width = 2.dp, color = Color(0xFFB7CFD2), shape = RoundedCornerShape(size=24.dp))
            .height(72.dp)
    )
}
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun BottomNavBar(){
    val context = LocalContext.current

    NavigationBar(
        containerColor = Color(0xFFFCF6EB),
        modifier = Modifier
            .height(128.dp)
            .border(width = 2.dp, color = Color(0xFFB7CFD2))
    ){

        NavigationBarItem(
            selected = true,
            colors = NavigationBarItemDefaults.colors(
                indicatorColor = Color.Transparent
            ),
            icon = {Icon(
                tint = Color(secondaryColor),
                painter = painterResource(id = R.drawable.todo_icon),
                contentDescription = "todoicon",

                modifier = Modifier
                    .padding(horizontal = 8.dp, vertical = 8.dp)
                    .background(color = Color(mainBackColor))
                    .width(56.dp)

            )},

            onClick = {
                val intent = Intent(context, TodoActivity::class.java)
                context.startActivity(intent)
            })


    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun Authentication(action: String){

    var username by remember({ mutableStateOf("") })
    var password by remember({ mutableStateOf("") })
    var email by remember({ mutableStateOf("") })
    Column(
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally,
        modifier = Modifier
            .fillMaxSize()
            .background(color = Color(mainBackColor))

    ) {
        Text("$action!", color = Color(accentColor), modifier = Modifier.padding(horizontal=16.dp, vertical = 16.dp),
            fontSize = 24.sp, fontWeight = FontWeight.Bold
        )

        Box() {
            OutlinedTextField(
                value = username,
                onValueChange = {newText -> username = newText},
                label = { Text("Username", color = Color(secondaryColor)) },
                colors = OutlinedTextFieldDefaults.colors(
                    unfocusedBorderColor = Color(secondaryColor),
                    focusedBorderColor = Color(secondaryColor)
                ),
                modifier = Modifier.padding(horizontal = 5.dp, vertical = 5.dp)
            )
        }

        Box() {
            OutlinedTextField(
                value = password,
                onValueChange = {newText -> password = newText},
                label = { Text("Password", color = Color(secondaryColor)) },
                colors = OutlinedTextFieldDefaults.colors(
                    unfocusedBorderColor = Color(secondaryColor),
                    focusedBorderColor = Color(secondaryColor)
                ),
                modifier = Modifier.padding(horizontal = 5.dp, vertical = 5.dp)
            )
        }

        Box() {
            OutlinedTextField(
                value = email,
                onValueChange = {newText -> email = newText},
                label = { Text("Email", color = Color(secondaryColor)) },
                colors = OutlinedTextFieldDefaults.colors(
                    unfocusedBorderColor = Color(secondaryColor),
                    focusedBorderColor = Color(secondaryColor)
                ),
                modifier = Modifier.padding(horizontal = 5.dp, vertical = 5.dp)
            )
        }
        Button(
            onClick = {sendAuthReq(username, password, email, action)},
            colors = ButtonDefaults.buttonColors(
                containerColor = Color(mainBackColor),
                contentColor = Color(accentColor)
            ),

            modifier = Modifier
                .padding(horizontal = 6.dp, vertical = 6.dp)
                .clip(RoundedCornerShape(2.dp))
                .border(color = Color(secondaryColor), width = 2.dp)
                .background(color = Color(mainBackColor))
        ) {
            Text(action, color = Color(accentColor))
        }


    }

}
