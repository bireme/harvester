========================
How to install Harvester
========================

Install pre-requisites
----------------------

Before installing Harvester, install the software listed below.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Server software

 +------------------------+----------------------------------------------+-------------------------+--------------------------+
 |**software**            |**product URL**                               |**installation method**  |**Ubuntu Package name**   |
 +========================+==============================================+=========================+==========================+
 | Python 2.6 or later    | http://www.python.org/                       | OS package manager      | python2.6                |
 +------------------------+----------------------------------------------+-------------------------+--------------------------+
 | GIT                    | http://git-scm.com/                          | OS package manager      | git-core                 |
 +------------------------+----------------------------------------------+-------------------------+--------------------------+
 | Python-lxml            | http://packages.ubuntu.com/natty/python-lxml | OS package manager      | python-lxml              |
 +------------------------+----------------------------------------------+-------------------------+--------------------------+


1. Install each package below using the recommended installation method above.

Note: Python comes pre-installed in most Linux distributions. If Python 2.6 or 2.7 is already installed, there is no need to install a newer version.

System-wide Python libraries
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 +-------------------+-------------------------------------------+------------------------------------------------------------+
 |**software**       |**product URL**                            |**installation method**                                     |
 +===================+===========================================+============================================================+
 | distribute 0.6.10 | http://pypi.python.org/pypi/distribute    | sudo python distribute_setup.py                            |
 +-------------------+-------------------------------------------+------------------------------------------------------------+
 | virtualenv        | http://pypi.python.org/pypi/virtualenv    | sudo easy_install virtualenv                               |
 +-------------------+-------------------------------------------+------------------------------------------------------------+

 2. Download the distribute_setup.py script and use the installed Python interperter to run it as root (this provides the easy_install utility)::

    # wget http://python-distribute.org/distribute_setup.py
    # python distribute_setup.py


3. Use easy_install to download and install virtuaenv::

    # easy_install virtualenv


Install the application environment
-----------------------------------

**Note: all of the remainig steps can be performed by a regular user without root access.**

5. Use virtualenv to create an application environment and activate it::

    $ virtualenv --distribute harvester
    $ source harvester/bin/activate
    (harvester)$   # note that the shell prompt displays the active virtual environment



Install the Harvester application
-----------------------------------

6. Go to a suitable installation directory and check out the application source::

    Development(Recommended):
    Read-only:
    (harvester)$ git clone git://github.com/rafaelnovello/harvester.git
    Read+write:
    (harvester)$ git clone git@github.com:rafaelnovello/harvester.git


7. With the `harvester` environment active, use `setuptools` to automagically download and install all the dependencies::

    (harvester)$ python setup.py install

8. The Harvester application comes with a `settings.py` file that allows somes more configuration.


Running the application
-----------------------

Harvester application is a command line tool. To see all option run:

    (harvester)$ ./harvester.py --help