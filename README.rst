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

Features
--------

* Store all your uploaded media in HDFS


Quickstart
----------

Install django-hdfs::

    pip install git+https://github.com/thanos/django-hdfs.git
    
    
Add storages to your settings.py file::

    INSTALLED_APPS = (
        ...
        'django_hdfs',
        ...
    )

while you are at it set your configurations in the settings.py file::

    HDFS_STROAGE = {
        'hosts': 'http://somehost:50070',
        'root': 'your_media'
    }
    
Also set up the media constants::

    MEDIA_ROOT = os.path.join(BASE_DIR, 'UPLOADS')
    MEDIA_URL = '/media/'    


Then use it in a project::

    from django_hdfs.storage import HDFSStorage
    
    # then use it in for FileField 
    some_doc = models.FileField('Upload Some Doc', null=True, blank=True, storage=HDFSStorage(),
                                       upload_to='some/path')



