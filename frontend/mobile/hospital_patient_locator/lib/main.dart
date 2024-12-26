import 'package:flutter/material.dart';
import 'camera_screen.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Camera QR Code Scanner',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: CameraScreen(),
    );
  }
}
