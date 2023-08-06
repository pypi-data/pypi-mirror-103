.. _installing:

Installing Afterburner Software
===============================

The latest version of the Afterburner software is already installed on the
Linux-based scientific desktop environment at the Met Office. Please contact
the `Afterburner team <mailto:afterburner@metoffice.gov.uk>`_ for details of how
to access and work with this locally-installed version.

Outside of the Met Office, please use the instructions provided below to obtain
and a build a copy of the Afterburner software.

System Requirements
-------------------

Afterburner software has been developed for Linux-based systems and, at the time
of writing, has primarily been tested using Red Hat Enterprise Linux v7 (RHEL7)
It is envisaged, however, that Afterburner, being a pure Python implementation,
should function as expected on similar Linux-based operating systems.

The Afterburner software suite depends upon the following tools and packages:

`GNU Bash <https://www.gnu.org/software/bash/>`_
   Recommended version: 4.2 or later.

`Python <https://www.python.org/>`_
   Recommended version: 3.x. Afterburner software is now compatible with both
   Python 2.7 and Python 3.x. At the time of writing (Feb 2020), however, a small
   number of prerequisite packages, notably Rose and Cylc, are not yet Python 3
   compatible. Accordingly it may be necessary to run Afterburner software against
   Python 2.7 if those packages are needed for a given processing task.

`Iris <https://scitools.org.uk/iris/>`_
   Recommended version: 2.2 or later. Afterburner makes extensive use of Iris,
   the popular Python package for manipulating and visualising meteorological and
   climate datasets.

`Rose <https://github.com/metomi/rose/>`_
   Recommended version: 2019.01.2 or later. A number of Afterburner applications
   are invoked via the Rose and Cylc utilities used for running scientific suites.
   Afterburner also utilises Rose's Python package, hence the ``rose`` executable
   must normally be in a user's command search path so that the location of this
   package can be discovered.

`Cylc <https://cylc.github.io/cylc/>`_
   Recommended version: 7.8 or later (most earlier versions should also work)

**Optional Packages**

Although the following packages are listed as optional, it is likely that many
of them will get installed as a result of installing the Iris package.

`Pyparsing <http://pyparsing.wikispaces.com/>`_
   The pyparsing package is currently used by Afterburner's derived diagnostic
   classes.

`Sphinx <http://www.sphinx-doc.org/en/stable/>`_
   The Afterburner documentation set is built from source using the Sphinx
   documentation generator. Accordingly, the Sphinx package will need to be
   installed if you wish to build and install Afterburner documentation.

`Windspharm <https://github.com/ajdawson/windspharm>`_
   The windspharm package, which provides a selection of spherical harmonic
   functions applicable to vector wind analysis, is currently used by a small
   number of Afterburner diagnostic processor classes.

Downloading
-----------

To install Afterburner outside of the Met Office, the latest source code should
be obtained from the Met Office `Science Repository Service <https://code.metoffice.gov.uk/>`_.
A user account is required to access the repository: information on how to obtain an
account can be found `here <https://code.metoffice.gov.uk/trac/home/wiki/FAQ#Requestinganaccount>`_.

To download the latest Afterburner software, first change to a suitable working
directory, then run the following command::

    % svn export https://code.metoffice.gov.uk/svn/afterburner/turbofan/trunk afterburner

As can be seen, this command retrieves the *latest* code from the trunk of the
Afterburner code repository. To retrieve a *tagged* version of the code base,
replace the aforementioned URL with that of the desired version (available tags
can be viewed at https://code.metoffice.gov.uk/trac/afterburner/browser/turbofan/tags).

Building and Installing
-----------------------

The Afterburner software is packaged using the `Setuptools <https://setuptools.readthedocs.io/en/latest/>`_
Python packaging toolkit. The following commands should be used to build the software and
install it into the directory specified by ``$INSTALL_DIR``. These commands should
be run within the same working directory as used for the ``svn export`` command above.
::

    % cd afterburner
    % INSTALL_DIR=<install-dir>
    % ROSE_DIR=$(rose --version | sed 's/^.*(\(.*\))$/\1/')/lib/python
    % export PYTHONPATH=$PYTHONPATH:$ROSE_DIR
    % python setup.py build

Once built, Afterburner's extensive test suite can, if desired, be run as follows::

    % python setup.py test

The software can then be installed into ``$INSTALL_DIR`` as follows::

    % python setup.py install --home=$INSTALL_DIR

To confirm that the software was installed successfully, enter::

    % $INSTALL_DIR/bin/abconfig --version

This should display the version number of the installed software.

If desired, the following commands may be used to build Afterburner's HTML
documentation set and and install it into the ``<doc_dir>`` directory. As noted
in the `System Requirements`_ section above, the `Sphinx <http://www.sphinx-doc.org/en/stable/>`_
package is required in order to build the documentation.
::

    % python setup.py build_docs
    % python setup.py install_docs --dst-dir=<doc_dir>

If the documentation was built and installed, it can be viewed through your
preferred web browser. In the case of Firefox, for example, one could invoke::

    % firefox <doc_dir>/html/index.html

Finally, if everything was successful, the directory into which the Afterburner
software was originally downloaded may be deleted::

    % cd ..
    % rm -rf afterburner
