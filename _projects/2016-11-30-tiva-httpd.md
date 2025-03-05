---
layout: project
shortTitle: Tiva HTTP
title: Tiva HTTP - Microcontroller Web Server
thumbnail: assets/thumbnails/tiva.png
date: 2016-11-30 00:00 -0400
modified: 2024-08-27 21:12 -0400
---

<!---
Write a really in depth explanation for this with more pictures and maybe refactor and redo my code
-->

**Status**: Done.

This is a web server that was built from scratch to run on a Tiva C Series microcontroller with an Orbit Booster Pack. Using a Python script to redirect the web traffic to the serial port, you can host content directly from a file system that utilizes the onboard EEPROM memory of the Orbit Booster Pack. The server tries to comply with a small subset of the RFC 2617 standard. It was created for the SE 101 class at the University of Waterloo with the help of a classmate.

[The code is available here](https://github.com/AideTechBot/tiva-httpd)
