---
layout: page
title: Project Archive
---

<section class="projects archive">
    {% assign sorted = site.projects | sort: 'date' | reverse %}
    {% for project in sorted %}
        <div class="links">
            <div class="link-date">{{ project.date | date: "%Y/%m/%d" }}</div>
            <div class="link-title">{{ project.title }}</div>
            <a class="red" href="{{ project.url | prepend: site.baseurl | prepend: site.url }}">
                View	
            </a>
            <a class="red small" href="{{ project.url | prepend: site.baseurl | prepend: site.url }}">
                &rarr;	
            </a>
        </div>
        {% if forloop.last %}
            <div class="section-footer">
                <span>Showing {{ forloop.length }} of {{ site.projects.size }} projects</span>
            </div>
        {% endif %}
    {% endfor %}
</section>
