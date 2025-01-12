import 'package:flutter/material.dart';

final culturedColor = Color(0xFFF5F5F5);
final whiteColor = Color(0xFFFEFEFE);
final floralWhiteColor = Color(0xFFFFFAEF);
final whiteChocolateColor = Color(0xFFEDE6D6);
final blackOliveColor = Color(0xFF3B3B3D);

final lightGrayColor = Color.fromARGB(255, 166, 165, 165);
final darkGunMetalColor = Color(0xFF1A1A1A);


var mainTheme = ThemeData(
  scaffoldBackgroundColor: floralWhiteColor,
        
  appBarTheme: AppBarTheme(
    
    iconTheme: IconThemeData(
      color: lightGrayColor,
    ),
    backgroundColor: floralWhiteColor,
    
    actionsIconTheme: IconThemeData(
      color: lightGrayColor,
    ),
    
    titleTextStyle: TextStyle(
      color: lightGrayColor,
    ),

  ),

  bottomNavigationBarTheme: BottomNavigationBarThemeData(
    backgroundColor: floralWhiteColor,
    elevation: 20,
    selectedItemColor: darkGunMetalColor,
    unselectedItemColor: lightGrayColor,
    selectedLabelStyle: TextStyle(fontSize: 12, fontWeight: FontWeight.bold),
    unselectedLabelStyle: TextStyle(fontSize: 12, fontWeight: FontWeight.normal),
  ),

  floatingActionButtonTheme: FloatingActionButtonThemeData(
    foregroundColor: whiteColor,
    backgroundColor: darkGunMetalColor,
    elevation: 10,

    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular(50),
      side: BorderSide(
        color: darkGunMetalColor,
        width: 2,
      ),
    ),
  ),
);