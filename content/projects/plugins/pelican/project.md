Title: Pelican Plugins
Logo: {static images/logo.png}
Project_Start: 2014/07
Project_Authors: Alexandre Fonseca
Project_Status: Maintained

For the port of my site from Drupal to [Pelican](http://getpelican.com), the
Python-based static site generator, I developed a series of plugins,
adding increased flexibility to the Pelican site structure and workflow.

<!-- PELICAN_END_SUMMARY -->

The developed plugins were:

* [pelican-autostatic](https://github.com/AlexJF/pelican-autostatic): Dynamically
  identify static resources referenced in content files without having to hardcode
  paths into the configuration files.
* [pelican-advthumbnailer](https://github.com/AlexJF/pelican-advthumbnailer):
  More flexible thumbnailer plugin that scans the output folder for images matching
  the thumbnail pattern and creates said thumbnails on-demand.
* [pelican-entities](https://github.com/AlexJF/pelican-entities): Allow the definition
  of new content types that behave as the original article content type in Pelican and
  support custom per-type configuration.
* [pelican-metadataparsing](https://github.com/AlexJF/pelican-metadataparsing): Allow
  definition of custom metadata parsers to make template code more readable.
