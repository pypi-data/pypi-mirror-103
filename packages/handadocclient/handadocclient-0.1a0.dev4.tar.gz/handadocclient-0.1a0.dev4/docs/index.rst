=============================================================================
Welcome to 'Handadoc Client' documentation!
=============================================================================

**handadoc_client** is the command line tool for a minimalistic documentation
webserver based on django.

.. image:: ../handadoc_client-icon.svg
   :height: 196px
   :width: 196px
   :alt: Handing over a documentation.
   :align: center

Installation
============

Install the latest release from pip.

.. code-block:: shell

   $ pip install handadocclient

.. toctree::
   :maxdepth: 3

   api_reference/index

Basic Usage
===========

Setup file
----------

The client is configured by using a *.handadoc.yml* configuration file. Mandatory fields
are name, title, description and doc_location.

.. autoattribute:: handadoc_client.DocuSetup.NAME
.. autoattribute:: handadoc_client.DocuSetup.DESCRIPTION
.. autoattribute:: handadoc_client.DocuSetup.TITLE
.. autoattribute:: handadoc_client.DocuSetup.DOC_LOCATION
.. autoattribute:: handadoc_client.DocuSetup.SERVER_URL

.. code-block:: yaml

   name: handadoc-client
   title: Handadoc Client Documentation
   description: >
       Documentation on how to use the handadoc-client within local repositories to
       package and post the build documentation to the handadoc webserver.
   doc_location: docs/_build/html
   # The server url is optional.
   server_url: https://hand-over-a-doc


Commandline Utility
-------------------

Make a configuration file within the current directory.

.. code-block:: shell

   $ handadoc init

Make a configuration in another destination.

.. code-block:: shell

   $ handadoc init --project-root-path=<another path>


Package and upload the current build documentation.

.. code-block:: shell

   $ handadoc over
   Username: user_at_handadoc
   Password:

   $


Indices and tables
==================

* :ref:`genindex`