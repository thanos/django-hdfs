=============================
django-hdfs
=============================

.. image:: https://badge.fury.io/py/django-hdfs.png
    :target: https://badge.fury.io/py/django-hdfs

.. image:: https://travis-ci.org/thanos/django-hdfs.png?branch=master
    :target: https://travis-ci.org/thanos/django-hdfs

HFDS interafce utilities of Django including file storage.

Documentation
-------------

The full documentation is at https://django-hdfs.readthedocs.org.

Quickstart
----------

Install django-hdfs::

    pip install django-hdfs

Then use it in a project::

    from django_hdfs.storages import HDFSStorage
    
    # then use it in for FileField 
    some_doc = models.FileField('Upload Some Doc', null=True, blank=True, storage=HDFSStorage(),
                                       upload_to='some/path')

Features
--------

* TODO

Running Tests
--------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install -r requirements_test.txt
    (myenv) $ python runtests.py

Credits
---------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
