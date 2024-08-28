---
layout: post
title: Logitech G403 Gaming Mouse Driver
shortTitle: G403 Linux
thumbnail: assets/thumbnails/g403.png
date: 2019-06-01 14:38 -0400
modified: 2024-08-27 21:27 -0400
---

**Status**: Work in progress, stalled.

At the time I started this project, I was using Ubuntu as my main operating system and I just bought a Logitech G403 gaming mouse. There was no driver available for this mouse on Linux and the Windows driver was bloated and slow.

I tried my hand at creating a driver for the mouse in question. This was done by reverse engineering the packets sent to the mouse in Windows using Wireshark. I then used this knowledge to write some code in Linux to send the same data with some tweaks.

Through this process, I got the lights on the mouse to change color. To have a complete driver, more reverse engineering is required to figure out how to trigger all the other features of the peripheral.