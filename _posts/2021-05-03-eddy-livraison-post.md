---
layout: post
title: How I Created a Restaurant Directory in Next.js
date: 2021-05-03 20:38 -0400
---

# The when and why

Soon after I graduated from University in a pandemic, I sat at home, staring at my screen in disbelief. It had been a year since I had seen most of my classmates and I could not believe that the school grind was over. In my confusion, I became hungrier than I ever have. My brain decided to do what it does best: order food. Unfortunately, my small hometown of Edmundston doesn't necessarily have any service that resembles Uber Eats. Most businesses around here barely have an online presence or close at odd hours. My fruitless search for nourishment wasted around 30 minutes of my time. This gave me the idea that Edmundston needs a simple website that serves as a directory for all restaurants. It should be easy to use and provide basic information about the places around town.

# The how

With my stomach empty of food but full of motivation, I decided to build my idea. The simplest way I could get this project in motion was using GitHub Pages. It was the perfect match because all I needed was static file hosting. As a bonus, the service is free!

The rest of the website is a combination of Next.js magic and GitHub workflow deployment. The only real issues I ran into were:

- Learning a lot of new CSS while trying to simplify everything as much as possible.
- Next.js static rendering not supporting internationalization while using static rendering.
- Figuring out a smart display order for the list of restaurants. I settled on ranking them loosely based on how local they are and if they deliver to your door.

# The result

Eddy-Livraison is a multi-lingual website that displays a list of restaurants in the Edmundston region. It favors delivery and local restaurants. It is a strict subset of all the restaurants in Edmundston. If you want your restaurant to be added to it, contact me at **CENSORED**, or simply make a pull request!

[Check out the live website here.](https://aidetechbot.github.io/eddy-livraison/)

[View the source code here.](https://github.com/AideTechBot/eddy-livraison)

**Update as of June 2025**: Unfortunately, I no longer own the domain eddy-livraison.com because it expired. Namecheap is now price gouging me to reclaim it, so I probably won't buy it again.
