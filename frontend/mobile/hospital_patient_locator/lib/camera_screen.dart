import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:typed_data';

class PatientInfo {
  final String id;
  final String name;
  final int age;
  final String room;
  final String condition;
  final String admissionDate;

  PatientInfo({
    required this.id,
    required this.name,
    required this.age,
    required this.room,
    required this.condition,
    required this.admissionDate,
  });

  factory PatientInfo.fromJson(Map<String, dynamic> json) {
    return PatientInfo(
      id: json['id'],
      name: json['name'],
      age: json['age'],
      room: json['room'],
      condition: json['condition'],
      admissionDate: json['admission_date'],
    );
  }
}

class CameraScreen extends StatefulWidget {
  @override
  _CameraScreenState createState() => _CameraScreenState();
}

class _CameraScreenState extends State<CameraScreen> {
  CameraController? _controller;
  List<CameraDescription>? cameras;
  bool isCameraActive = false;
  bool isProcessing = false;

  @override
  void initState() {
    super.initState();
    _initializeCamera();
  }

  Future<void> _initializeCamera() async {
    cameras = await availableCameras();
    _controller = CameraController(
      cameras![0], 
      ResolutionPreset.high,
      enableAudio: false,
      imageFormatGroup: ImageFormatGroup.yuv420
    );
    await _controller!.initialize();
  }

  void _startCamera() {
    setState(() {
      isCameraActive = true;
    });
    
    Duration processingDelay = Duration(milliseconds: 500);
    DateTime lastProcessingTime = DateTime.now();
    
    _controller!.startImageStream((CameraImage image) async {
      final currentTime = DateTime.now();
      if (!isProcessing && currentTime.difference(lastProcessingTime) > processingDelay) {
        isProcessing = true;
        lastProcessingTime = currentTime;
        await _detectQRCode(image);
        isProcessing = false;
      }
    });
  }

  void _stopCamera() {
    setState(() {
      isCameraActive = false;
    });
    _controller!.stopImageStream();
  }

  Future<void> _detectQRCode(CameraImage image) async {
    try {
      final allBytes = BytesBuilder();
      allBytes.add(image.planes[0].bytes);
      
      final bytes = allBytes.takeBytes();
      final base64Image = base64Encode(bytes);
      
      final response = await http.post(
        Uri.parse('http://192.168.8.111:5000/scan'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'image': 'data:image/jpeg;base64,$base64Image',
          'width': image.width,
          'height': image.height,
          'format': 'yuv420'
        }),
      );

      if (response.statusCode == 200) {
        final result = jsonDecode(response.body);
        if (result['success'] && result['results'].isNotEmpty) {
          final userInfo = PatientInfo.fromJson(result['results'][0]['user']);
          print('QR Code Content: ${result['results'][0]['qr_data']}');
          print('User ID: ${userInfo.id}');
        }
      }
    } catch (e) {
      print('Error detecting QR code: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Camera QR Code Scanner')),
      body: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          if (isCameraActive)
            Container(
              height: MediaQuery.of(context).size.height * 0.7,
              child: AspectRatio(
                aspectRatio: _controller!.value.aspectRatio,
                child: CameraPreview(_controller!),
              ),
            ),
          SizedBox(height: 20),
          ElevatedButton(
            onPressed: isCameraActive ? _stopCamera : _startCamera,
            child: Text(isCameraActive ? 'Stop Camera' : 'Start Camera'),
          ),
        ],
      ),
    );
  }

  @override
  void dispose() {
    _controller?.dispose();
    super.dispose();
  }
} 