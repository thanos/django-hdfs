# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
#
# $Id$
#
#  Developer: Thanos Vassilakis
#

import logging
from json import dumps

import hdfs
import requests
from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound
from hdfs.client import HdfsError

log = logging.getLogger(__name__)


def hdfs_usage(request, root=None):
    host = settings.HDFS_STROAGE['hosts']
    if not root:
        root = settings.HDFS_STROAGE['HDFS_ROOT']

    log.info('http://%s/%s', host, root)
    client = hdfs.InsecureClient('http://%s' % host)
    tree = []
    try:
        for appcode in client.list(root):
            url = 'http://%s/webhdfs/v1%s/%s?op=GETCONTENTSUMMARY' % (host, root, appcode)
            data = requests.get(url).json()
            if data['ContentSummary']['directoryCount']:
                tree.append({
                    'name': appcode,
                    'value': round(data['ContentSummary']['length'] / 1000000.0, 2)
                })
    except HdfsError, e:
        log.warn("hdfs_usage error: %s", e)
        return HttpResponseNotFound(dumps(tree), content_type='application/json')
    return HttpResponse(dumps(tree), content_type='application/json')
