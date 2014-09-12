Title: Website ported to Pelican
Logo: {static images/logo.png}

I have finished porting the site from Drupal to Pelican. I'm happy to inform
that the results of this port are a threefold improvement in page load time
as well as a big reduction in the overhead to my small little dedicated server.
<!-- PELICAN_END_SUMMARY -->

# Intro
For those who might not know what [Pelican](http://blog.getpelican.com/) is,
it's a static site generator coded in Python (similar to the more widely known
[Jekyll](http://jekyllrb.com/), coded in Ruby). The philosophy behind these 
static site generators is that some sites (e.g. personal sites) do not really
need the dynamic content generation provided by the Ruby/Python/PHP runtimes.
Usually, these runtimes are only there to support one form or another of Content
Management System (e.g. Drupal, Joomal, Wordpress, Rails) which does indeed
provide some facilities for site administration and content editing. 

By relying on [Markdown](http://daringfireball.net/projects/markdown/) or
[rST](http://docutils.sourceforge.net/rst.html) to write the content,
and some form of content versioning system like [Git](http://git-scm.com/) to
keep track of changes, static site generators reconcile ease of management and
speed by compiling a static (as in only .html files) of your site from your
Markdown content, metadata and themes.

Not only are these sites usually faster to load as they can be served directly
by the web server without having to pass through a runtime or connect to a database,
they can also be hosted just about anywhere. There's no shortage of free hosting
for static sites, including the popular [GitHub Pages](https://pages.github.com/).

# Drupal Migration

## Nodes
Alas, you do lose some flexibility when migrating Drupal to Pelican. In particular,
Drupal has the notion of nodes and diferent content types in which you can easily
customize its fields and appearance. In my site, for instance, I had 3 content types:

* Pages: Home, About Me, Contact.
* Articles: A blog post like this one.
* Projects: A project description page like any of the ones you can see in the
  projects section.

Each one of these content types has its own creation and modification dates,
list of authors, support for pagination and syndication (e.g. RSS), etc.

By default, Pelican supports only 2 types of content: pages -- which can be
linked to but not paginated or syndicated -- and articles -- which can be
linked to, listed, paginated and syndicated. I could port my site over by
treating projects as a specific type of article, perhaps by giving them a
special category but that never seemed natural to me as it would require extra
logic at the theme/template level. What I wanted was to be able to recycle the
generation code for articles and be able to use it for any content type I wanted,
with its own custom settings. This led me to the creation of 
[Pelican-entities](https://pypi.python.org/pypi/pelican-entities), a plugin for
Pelican that allows you to define your own content types (aka entity types) and
have their instances (aka entities) be paginated and syndicated with custom
settings (e.g. urls, metadata).

## Organized resources
With that out of the way, the other thing that bothered me about Pelican is that,
by default, it forces you to put all your static resources such as images and other
non-content files in specific directories which you then have to add to the
configuration option ``STATIC_PATHS``. This setup makes it easy to have a central
folder containing all the images in yourt articles, projects and pages and link
them to it. However, I prefer things a little more organized: have all the data about
an article/project be on its own folder:

* ``article/<article id>/post.md``
* ``article/<article id>/images/*``
* ``article/<article id>/files/*``

To do this with vanilla Pelican, you'd need to add all the ``article/<article id>``
paths to the ``STATIC_PATHS`` setting which is not very manageable. To solve this,
I coded [Pelican-autostatic](https://pypi.python.org/pypi/pelican-autostatic) which
allows you to dinamically reference images and other static resources from your
content and have those resources be directly copied to the output folder, preserving
their path. Unfortunately, the existing Thumbnailer plugin relied on the
single-folder philosophy so I also had to come up with
[Pelican-advthumbnailer](https://pypi.python.org/pypi/pelican-advthumbnailer) which
allows thumbnail generation for any image referenced by a content file, independent
of the location of the image.

## Structured metadata
Finally, the one last thing bothering me was the metadata. I like to be able to
simply define a list of attachments or list of images and have the site automatically
put them in a structure common to all content types. One way to do this in
Pelican would be to add these structures directly in the content Markdown.
However, if I then wanted to change it, I'd have to replicate these changes
over every article/project I have ever written. 

What I'd prefer is to associate lists of images and files to an article/project and
have them be accessible by the theme templates as something like
``article.gallery`` or ``article.attachments`` which the template could then iterate
through when generating the output.

Pelican does support definition of custom metadata so it could theoretically be
as simple as adding the following to the top of a Markdown file:

```
Attachments: files/1.pdf
			 files/2.pdf
			 files/3.pdf
```

You could then access each one of the lines in the template by referencing
``article.attachments`` or ``entity.attachments`` if using my Pelican-entities
plugin.

However, I usually want to give a friendly name/description to each one of those
files. I could add another metadata field just for the descriptions like so:

```
Attachment_Descriptions: Report
						 Presentation
						 Draft
```

And match them by index with the actual attachments. But this is rather ugly. I
created the
[Pelican-metadataparsing](https://pypi.python.org/pypi/pelican-metadataparsing)
to give more flexibility to metadata in Pelican. You can now add some code that
will allow you to turn the following:

```
Attachments: files/1.pdf || Report
			 files/2.pdf || Presentation
			 files/3.pdf || Draft
```

Directly into Python objects containing a `url` (`files/1.pdf`) and `name`
(`Report`) attribute that you can then reference in your templates.

## Other stuff
As with most static sites, I've ported the comment system to
[Disqus](https://disqus.com/) and the contact form to
[JotForm](http://www.jotform.com/). For the search feature, I'm relying
on [Google Custom Search Engine](https://www.google.com/cse). I'm actually
surprised how well all of these work in terms of integration with the site's
theme with minor customizations.

# Results
After having done all of this and converted my entire content to Pelican, I'm
still hosting my site in my small webserver (a KS-1 in
[Kimsufi](http://www.kimsufi.com)). Initially I wanted to put it in Github pages
but some urls changed from the Drupal version and so, for the time being, I'm
relying on Nginx 301 redirects to not have broken urls.

This also allows me to run direct performance comparisons between the site in
Drupal and Pelican under the same hardware. The pictures below show how Pelican
with my custom theme compares against Drupal with full-page caching and all the
plugins necessary to have the same functionality. The results were obtained
from [WebpageTest](http://www.webpagetest.org/). The static version achieves a
speedup of approximately 3x for first view and almost 5x for repeated view.

<p class="center-text">
<a class="image-box" href="{static images/drupal.png}" title="Drupal performance">
<img src="{static images/drupal.png thumb=220x165}" alt="Drupal performance">
</a>
<a class="image-box" href="{static images/pelican.png}" title="Pelican performance">
<img src="{static images/pelican.png thumb=220x165}" alt="Pelican performance">
</a>
</p>

As for overhead in the system, I haven't performed a lot of tests but some rough
stress experiments have shown that the Pelican site can handle at least 50x as many
clients as Drupal.

# Conclusion
If you currently have a site using some kind of CMS such as Wordpress, Drupal,
Joomla and what not, give careful thought as to whether you really need the
features it provides. If you realize that you don't really need any of the dynamic
stuff you currently have (or if it can be replaced with third parties like Disqus)
and if you don't mind to write your site through Markdown/reStructuredText, I'd strongly
urge you to make the jump. Not only will you be able to potentially save some
money with hosting, you'll also eliminate one of the biggest attack vectors for servers:
server side scripts and databases.

If you're looking for inspiration, you can check the source code of my site
[here](https://github.com/AlexJF/alexjf.net).


*NOTE:* The amazing logo of this article was designed by derry livenski and
borrowed from [Issue#1008](https://github.com/getpelican/pelican/issues/1008)
until such a time as some consensus is reached regarding the official logo for
Pelican.
