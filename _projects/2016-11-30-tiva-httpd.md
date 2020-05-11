---
layout: post
shortTitle: Tiva HTTP
title: Tiva HTTP - A Microcontroller-based Web Server
thumbnail: assets/thumbnails/hockey.png
date: 2016-11-30 00:00 -0400
---


<!---
Write a really in depth explanation for this with more pictures and maybe refactor and redo my code
-->
This is a web server that was built from ground up to run on a Tiva C Series microcontroller with an Orbit Booster Pack. Using a python script to redirect the web traffic to the serial port, you can host content directly from a file system that utilises the onboard EEPROM memory of the boosterpack. Also, the server complies with most of the RFC 2616 standard. It was coded for the software engineering class at my school with the help of Philip Tang.

[The code is available here](https://github.com/AideTechBot/tiva-httpd)
