---
layout: page
permalink: /publications/
title: Publications
description:
nav: true
nav_order: 1
---
<!-- _pages/publications.md -->

<!-- Bibsearch Feature -->

{% include bib_search.liquid %}

<div class="publications">
<h2>First author</h2>
{% bibliography -f {{ site.scholar.bibliography }} %}

<br>
<hr style="height:2px;border-width:0;color:black;background-color:gray">
<br>

<h2>Significative contribution</h2>
{% bibliography -f {{ site.scholar.coauth_papers }} %}

<br>
<hr style="height:2px;border-width:0;color:black;background-color:gray">
<br>

<h2>Collaboration papers</h2>
{% bibliography -f {{ site.scholar.other_papers }} %}


</div>


