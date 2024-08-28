---
layout: page
title: Blog Archive
---

<section class="blog archive">
    {% assign sorted = site.posts | sort: 'date' | reverse %}
    {% for post in sorted %}
        <div class="links">
            <div class="link-date">{{ post.date | date: "%Y/%m/%d" }}</div>
            <div class="link-title">{{ post.title }}</div>
            <a class="blue" href="{{ post.url | prepend: site.baseurl | prepend: site.url }}">
                Read	
            </a>
            <a class="blue small" href="{{ post.url | prepend: site.baseurl | prepend: site.url }}">
                &rarr;	
            </a>
        </div>
        {% if forloop.last %}
            <div class="section-footer">
                <span>Showing {{ forloop.length }} of {{ site.posts.size }} posts</span>
            </div>
        {% endif %}
    {% endfor %}
</section>
