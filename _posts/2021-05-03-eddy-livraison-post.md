---
layout: post
title: Eddy-Livraison, a new way to order!
date: 2020-05-11 21:34 -0400
---

# The when and why

Soon after I graduated from University in a pandemic, I sat at home, staring at my screen in disbelief. It had been a year since I had seen most of my classmates and I could not believe that the school grind was over. In my confusion, I became hungrier than anyone ever has. I decided to do what I do best: order food. Unfortunately, my small home town of Edmundston doesn't necessarily have any service that resembles Uber Eats. Most businesses around here barely even have an online presence. Unfortunately, most places where closed **and** the search for those places wasted around 30 minutes. This led me to believe that Edmundston needs a small and simple website that serves as a directory for delivery and/or take-out food.

# The how

With my belly empty and lots of motivation, I decided to build a simple website to do exactly what I wanted. The simplest way I could get this project in motion was using GitHub Pages. It was the perfect match because I did not need a back-end and it's free.



The rest of the website is a combination of Next.js magic and GitHub workflow deployment. The only real issues I ran into where:
- CSS being as quirky as it usually is and doing the opposite of what I want it to do.
- Next.js static rendering not supporting i18n while using static rendering. (Look at the Github workflow deployment script for more info)
- The way I would display the list of restaurants. (I settled on ranking them loosely by how local they are and if they deliver to your door.)

# The what

Eddy-Livraison is a multi-lingual website that displays a list of restaurants in the Edmundston region. It favours delivery and local restaurants. It is a strict subset of all the restaurants in Edmundston. If you want your restaurant to be added to it, contact me at **help@eddy-livraison.com**.

[Check out the live website here.](https://eddy-livraison.com)

[View the source code here.](https://github.com/AideTechBot/eddy-livraison)
