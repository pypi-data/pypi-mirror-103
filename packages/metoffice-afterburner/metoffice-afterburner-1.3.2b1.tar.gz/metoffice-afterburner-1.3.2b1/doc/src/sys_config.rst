Configuring Afterburner Software
================================

Environment Variables
---------------------

AFTERBURNER_HOME_DIR
   This environment variable will often be the only one that you will need to
   specify in order to run Afterburner applications. It defines the pathname of
   the top-level directory that contains Afterburner software and its associated
   artifacts (within it you should see a fairly standard set of UNIX subdirectories
   called ``bin``, ``doc``, ``etc``, ``lib`` and so on).

   Your local site administrator or system manager should be able to advise you of
   the appropriate setting for this environment variable if the Afterburner
   software has been installed centrally. If you have installed Afterburner
   yourself then instructions on setting this environment variable are provided
   in :doc:`installing`.

AFTERBURNER_LOG_LEVEL
   This environment variable may be used to set the initial log level assigned
   to the 'afterburner' logger object, which gets created when the ``afterburner``
   package (or one of its subpackages/submodules) is imported.
   
   The default log level (WARNING) can be overridden by setting AFTERBURNER_LOG_LEVEL
   either to one of the level names recognised by Python's `logging <https://docs.python.org/2/library/logging.html>`_
   module (e.g. 'INFO'), or else to the equivalent integer constant (20 in the
   case of 'INFO'). If a name is specified then it's case is not significant,
   i.e. 'debug' is equivalent to 'DEBUG'.

Configuration Files
-------------------

A number of Afterburner software settings can be specified using ini-style
configuration files. The Afterburner system checks for the presence of two
configuration files: a *site configuration file*, and a *user configuration file*.

The site configuration file, if used, is located at ``$AFTERBURNER_HOME_DIR/etc/afterburner.conf``.
This file will typically be maintained by your local site administrator or
system manager.

The user configuration file, if used, should be located at ``$HOME/.config/afterburner/afterburner.conf``.
You'll need to create this file if you want to specify configuration options.

Both configuration files are optional. If a particular configuration option
is specified in both files, then the setting in the user configuration file normally
takes precedence (there may be instances where users cannot override a site-wide
setting).

As is common with ini files, most options are defined under particular sections,
which are identified by a section name within square brackets.

Configuration Section: [DEFAULT]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

No options at present for this section.

Configuration Section: [python]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Option: extra_site_dirs
   May be used to specify extra site-specific directories that contain Python
   packages and modules required to run Afterburner applications. The value of
   this option should be a *colon-separated* list of directory paths which will
   get appended to Python's module search path at run-time.

   This option, if it's needed at all, will usually be specified in the site
   configuration file. If at your site the location of Python modules is always
   determined through the use of PYTHONPATH and/or .pth files, then it should
   not be necessary to use this configuration option.

   Example::

       [python]
       extra_site_dirs=/our/custom/python/dir:/janedoe/lib/python
