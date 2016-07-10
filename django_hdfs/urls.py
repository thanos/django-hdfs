# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^hdfs-usage/(.+)$', views.hdfs_usage, name="hdfs-usage"),
]
