import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'screens/login_screen.dart';

void main() {
  runApp(const ProviderScope(child: GigShieldApp()));
}

class GigShieldApp extends StatelessWidget {
  const GigShieldApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'GigShield',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF00E5B0),
          brightness: Brightness.dark,
        ),
        scaffoldBackgroundColor: const Color(0xFF060810),
        fontFamily: 'SpaceGrotesk',
        useMaterial3: true,
      ),
      home: const LoginScreen(),
    );
  }
}
