import 'dart:async';

import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:typed_data';

class PatientInfo {
  final String id;
  final String username;
  final List<String> roles;

  PatientInfo({
    required this.id,
    required this.username,
    required this.roles,
  });

  factory PatientInfo.fromJson(Map<String, dynamic> json) {
    return PatientInfo(
      id: json['id'] ?? '',
      username: json['username'] ?? '',
      roles: (json['roles'] as List<dynamic>?)?.map((role) => 
        (role['name'] ?? '').toString()
      ).toList() ?? [],
    );
  }
}

class CameraScreen extends StatefulWidget {
  @override
  _CameraScreenState createState() => _CameraScreenState();
}

class _CameraScreenState extends State<CameraScreen> {
  // Update the BASE_URL constant
  static const String BASE_URL = 'http://192.168.3.89:8082';
  static const String SCAN_URL = 'http://192.168.3.89:5002';

  // Add common headers
  static final Map<String, String> _headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  };

  // Add hardcoded user info
  static const Map<String, dynamic> MOCK_USER = {
    "id": "1",
    "username": "khawla",
    "roles": [
      {
        "id": "1",
        "name": "PATIENT"
      }
    ]
  };

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
        Uri.parse('$SCAN_URL/scan'),
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
        if (result['success'] == true && 
            result['results'] != null && 
            result['results'].isNotEmpty) {
          
          final qrData = result['results'][0]['qr_data'];
          
          // Parse the QR data to get room number
          final qrDataMap = jsonDecode(qrData);
          final roomNumber = qrDataMap['room_number'];

          // Save localisation with hardcoded username
          await saveLocalisation(roomNumber, MOCK_USER['username']);
          
          // Add delay to prevent multiple scans
          await Future.delayed(const Duration(seconds: 2));
        }
      }
    } catch (e, stackTrace) {
      print('Error detecting QR code: $e');
      print('Stack trace: $stackTrace');
    }
  }

  Future<void> saveLocalisation(String roomNumber, String username) async {
    try {
      print('Sending localisation request with room_id: $roomNumber, username: $username');
      
      final uri = Uri.parse('$BASE_URL/api/localisations');
      print('Request URL: $uri');
      
      final requestBody = jsonEncode({
        'room_id': roomNumber,
        'username': username
      });
      print('Request body: $requestBody');
      
      final response = await http.post(
        uri,
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: requestBody,
      ).timeout(
        const Duration(seconds: 10),
        onTimeout: () {
          print('Request timed out');
          throw TimeoutException('Request timed out');
        },
      );

      print('Response status code: ${response.statusCode}');
      print('Response headers: ${response.headers}');
      print('Response body: ${response.body}');

      if (response.statusCode == 200 || response.statusCode == 201) {
        print('Localisation saved successfully');
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Location updated successfully'),
            backgroundColor: Colors.green,
          ),
        );
      } else {
        print('Failed to save localisation: ${response.statusCode}');
        print('Error response body: ${response.body}');
        
        String errorMessage = 'Failed to update location';
        try {
          final errorBody = jsonDecode(response.body);
          errorMessage = errorBody['message'] ?? errorMessage;
        } catch (e) {
          print('Error parsing error response: $e');
        }
        
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(errorMessage),
            backgroundColor: Colors.red,
          ),
        );
      }
    } catch (e) {
      print('Error saving localisation: $e');
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Network error: $e'),
          backgroundColor: Colors.red,
        ),
      );
    }
  }

  Future<void> printLocalisations() async {
    try {
      final uri = Uri.parse('http://192.168.3.89:8082/api/localisations');
      print('Fetching localisations from: $uri');
      
      final response = await http.get(
        uri,
        headers: {
          'Accept': 'application/json',
        },
      ).timeout(
        const Duration(seconds: 30),
        onTimeout: () {
          print('Request timed out after 30 seconds');
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text('Connection timeout - Please check your network connection'),
              backgroundColor: Colors.red,
            ),
          );
          throw TimeoutException('Request timed out');
        },
      );

      print('Response status code: ${response.statusCode}');
      
      if (response.statusCode == 200) {
        final List<dynamic> localisations = jsonDecode(response.body);
        print('\nAll Localisations:');
        if (localisations.isEmpty) {
          print('No localizations found in database');
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text('No localizations found'),
              backgroundColor: Colors.orange,
            ),
          );
        } else {
          for (var loc in localisations) {
            print('Room: ${loc['room_id']}, User: ${loc['username']}');
          }
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('Found ${localisations.length} localizations'),
              backgroundColor: Colors.green,
            ),
          );
        }
      } else {
        print('Failed to fetch localisations: ${response.statusCode}');
        print('Error response body: ${response.body}');
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Error: HTTP ${response.statusCode}'),
            backgroundColor: Colors.red,
          ),
        );
      }
    } catch (e) {
      print('Error fetching localisations: $e');
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Network error: $e'),
          backgroundColor: Colors.red,
        ),
      );
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
          SizedBox(height: 10),
          ElevatedButton(
            onPressed: printLocalisations,
            child: Text('Print Localisations'),
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