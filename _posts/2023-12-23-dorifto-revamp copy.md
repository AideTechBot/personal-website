---
layout: post
title: Dorifto Racing Version 2 
date: 2023-12-23 14:55 -0400
---

Ever since I created dorifto.racing back in 2017, I always thought I would come around to revamping it. This is because it was built in-between classes while I was studying at university. The website was a product of endless caffeine, procrastination, and me wanting to waste my time during a weekend. I've had a lot more time to myself recently, so I decided to give Dorifto some new life. **After 632 days of continuous uptime without updates, Dorifto has risen from the ashes reborn!**


**[You can see the final product live at https://dorifo.racing](https://dorifto.racing)**


This re-architecture took me a bit longer than I initially expected. The intention was to make it more secure, stable, and easier to update. On the other hand, I also wanted to play around with a couple of interesting technologies while I was at it. Balancing these two objectives was tough, but I finally accomplished it.

## The old architecture

In 2017 after I finished Dorifto, I left it mostly untouched for a very long time. Occasionally, I would fix the website when something hosting-related broke, but otherwise it was left alone. It was run on an ancient Ubuntu VPS that I had set up manually. I made no setup scripts, so I could not recreate it if I tried.

From what I remember, it was running Apache and the entire website was made in PHP. I had a MySQL database to keep track of IPs, so I could block abusers of the system. Every time someone requested a video, it would run a static version of FFMPEG to copy files around and splice them together.

Overall, there wasn't much to it. It was just a pain in the ass to maintain and update. This meant that overtime all the dependencies became extremely old, and I was scared that some security vulnerability would ruin it.

## The new architecture

Here is a complete list of things that have been introduced or improved:
- A set of update and setup scripts, so I can completely blow away a VPS and reconfigure it *within minutes*.
- The entire application is dockerized, so I can deploy it easily.
- The version of FFMPEG is updated dynamically.
- NGINX is used to host the server now, complete with SSL and auto-certificate renewal.
- A combination of Typescript, Bun, Hono, and HTMX are being used to deliver a great UI/UX.
- Loading indicators have been added so that you know your file is being processed.
- Fully server-sided rendering.
- Improved load time due to smaller assets.
- Improved accessibility due to HTML refactor.
- Better asynchronous job handling, which means multiple people can upload videos at once.
- Better styling.
- Automatic temporary file cleaning on the server side with CRON jobs.
- Easier updating of dependencies.

## Conclusion

It was a massive amount of fun to recreate my own project from years ago. I have learned a lot about web development since I initially released the website, and it was really cool to be able to practice what I absorbed. It's nice to be able to correct all my mistakes and (hopefully) give another 6 years of life to **dorifto.racing**.

**To the users:** Thank you for using my tool! I appreciate every single one of you!

[View the source code here.](https://github.com/AideTechBot/dorifto.racing)
