=====
Usage
=====

Folder structure
================

A Melthon project has following folder structure.
Folder names can be changed as option to the melthon command.

templates
  This is the only mandatory folder. It contains your Mako tempates (\*.mako) which
  will be rendered into HTML pages. This folder supports subfolders.
  To prevent a file from rendering, like base template or reusable parts, name your
  template ``*.template.mako`` or ``*.part.mako``.

  If you want to render the same template multiple times, use suffix ``*.repeat.mako``.
  See `Repeated templates`_ for more info.

static
  This folder contents will be copied to the root of the output folder.
  You can use this folder for static assets like CSS, JavaScript, images, ...

data
  If you want to have certain information available in a template, e.g. a telephone
  number, you can provide this information in YAML files. Each YAML file inside the
  ``data`` folder will be available as ``data['<FILENAME>']`` in your templates.
  E.g. ``general.yml`` will become ``data['general']``.

middleware
  In this folder, you can provide custom middleware. The middleware will run before
  and after the rendering of your site. It has access to the context. Please use
  following template::

    from melthon.middleware import Middleware


    class Middleware1(Middleware):
      def before(self, context):
        # <YOUR CUSTOM CODE>
        return context
        
      def after(self, context):
        # <YOUR CUSTOM CODE>
        return context

  You can define multiple middlewares (classes) in the same file. Method ``before``
  or ``after`` can be omitted in case it's not required.

output
  This folder will contain the rendered result


Command options
===============

Melthon currently supports 2 commands: ``melthon build`` and ``melthon clean``.
Please use ``melthon --help`` and ``melthon <command> --help`` to list the available options.


Repeated templates
==================
To render the same template multiple times, use suffix ``*.repeat.mako`` for your template.
Next to this, you'll have to supply a ``repeat.yml`` in the root of your site.

This file contains the mapping between your template and the collection in the data files.
E.g. to use the list ``events`` in file ``data/general.yml`` for template ``events.repeat.mako``,
you have to provide following ``repeat.yml``:

    events: "/general/events"

Melthon expects an attribute ``slug`` for each item in the repeat collection.
The slug defines the output name of the repeated page.
The whole item will be passed in variable ``page`` inside the template.

**Tip**: To have an index page for your repeated pages, you can specify a template with the same name.
E.g. ``events.mako`` and ``events.repeat.mako``

You can check https://github.com/JenswBE/python-melthon/tree/master/tests/test_site if you want an example of repeated pages.