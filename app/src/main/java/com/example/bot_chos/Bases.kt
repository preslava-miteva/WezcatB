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
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.NavigationBar
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
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import com.example.bot_chos.ui.theme.BotchosTheme


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
    NavigationBar(
        containerColor = Color(0xFFFCF6EB),
        modifier = Modifier
            .height(128.dp)
            .border(width = 2.dp, color = Color(0xFFB7CFD2))
    ){

    }
}

