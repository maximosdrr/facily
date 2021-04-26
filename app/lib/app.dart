import 'package:app/pages/home/index.dart';
import 'package:app/routes.dart';
import 'package:app/themes/main-theme.dart';
import 'package:flutter/material.dart';

class Facily extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Facily',
      theme: MainTheme.appThemeData,
      onGenerateRoute: AppRouter.generateRoute,
      initialRoute: '/home',
    );
  }
}
