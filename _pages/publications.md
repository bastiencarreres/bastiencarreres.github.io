---
layout: pub_page
permalink: /publications/
title: Publications
publist_pdf: Pub_list.pdf
description:
nav: true
nav_order: 1
---
<!-- _pages/publications.md -->

<!-- Bibsearch Feature -->

{% include bib_search.liquid %}

<div class="publications">
<h2>First author</h2>
{% bibliography -f {{ site.scholar.bibliography }} -q @*[keywords=FirstAuth] %}

<br>
<hr style="height:2px;border-width:0;color:black;background-color:gray">
<br>

<h2>Significant contribution</h2>
{% bibliography -f {{ site.scholar.bibliography }} -q @*[keywords=SignContrib] %}

<br>
<hr style="height:2px;border-width:0;color:black;background-color:gray">
<br>

<h2>Co-author</h2>
{% bibliography -f {{ site.scholar.bibliography }} -q @*[keywords=Other] %}
</div>


