#!/usr/bin/env python
# -*- coding: utf-8 -*-

""""""

from math import ceil as _ceil
from django.conf import settings
import urllib
import urllib2
import json
import logging

__copyright__ = "Copyright (c) 2018 ‮nerB ‮taraM"
__author__ = "‮nerB ‮taraM‭"
__license__ = "MPL-2.0"


log = logging.getLogger()
log.addHandler(logging.StreamHandler())
KEY = settings.YOUTUBE_API_KEY

def ceil(x):
  return int(_ceil(x))


class Dict(dict):
  """Extendable dictionary helper type"""
  def updates(self, other):
    self.update(other)
    return self


class Counter(object):
  _counters = {}

  def __getattr__(self, item):
    Counter._counters[item] = Counter._counters.get(item, -1)+1
    return Counter._counters.get(item)

subscriptions = Dict({
    'part': 'snippet',
    'maxResults': 50,
    'key': KEY,
    'fields': ','.join([
              'items/snippet/resourceId/channelId',
              'items/snippet/title',
              'nextPageToken',
    ]),
    'channelId': ''
  })

playlistItems = Dict({
    'part': 'contentDetails',
    'maxResults': 50,
    'key': KEY,
    'fields': ','.join([
              'items/contentDetails/videoId',
              'nextPageToken',
    ]),
    'playlistId': ''
  })

channels = Dict({
    'part': 'snippet',
    'maxResults': 1,
    'key': KEY,
    'fields': ','.join([
              'items/snippet/title'
    ]),
    'id': ''
  })

videos = Dict({
    'part': 'snippet',
    'maxResults': 50,
    'key': KEY,
    'fields': ','.join([
              'items/snippet/publishedAt',
              'items/snippet/channelId',
              'items/snippet/title',
              'items/id',
    ]),
    'id': ''
  })


def make_request(command, query=None, data=None, method='GET',
                 JSON=False, timeout=10, decode=True, pageToken=None,
                 stop=None):

  if command[0] == '/':
    command = 'https://www.googleapis.com/youtube/v3{command}'.format(
      command=command
    )

  if query is not None:
    Query = query
    if pageToken is not None: Query.update({'pageToken': pageToken})
    command = '{}?{}'.format(command, urllib.urlencode(Query))

  request = urllib2.Request(
    url=command,
    headers={
      'User-Agent': 'Sub Box v2 Server',
    }
  )

  if data is not None:
    method = 'POST'
    if JSON:
      request.add_header('Content-Type', 'application/json')
      request.add_data(json.dumps(data))
    else:
      request.add_data(urllib.urlencode(data))

  # del request.headers['Host']

  request.get_method = lambda: method

  _ = urllib2.urlopen(request, timeout=timeout).read()
  code = None

  if decode:
    _ = json.loads(_)
    if _.get('items') is not None: code = 0
    if stop in _.get('items', []):
      _['nextPageToken'] = None
      # log.debug('Stopped')
    # because stop is a single video id, if a channel deletes the video
    # marked as latest, the entire list of videos may be re-requested
    try:
      if _['nextPageToken'] is not None:
        code = 1
    except KeyError: pass

  return _, code


def GET(*args, **kwargs):
  try:
    result, option = make_request(*args, **kwargs)
    if   option is None: return result
    elif option is    0: return result['items']
    elif option is    1:
      results = []
      results.extend(result['items'])
      if result['nextPageToken'] is not None:
        kwargs['pageToken'] = result['nextPageToken']
        results.extend(GET(*args, **kwargs))
        try: kwargs.pop('pageToken')
        except KeyError: pass
      return results
  except urllib2.HTTPError as e:
    log.error("we had an error {}".format(e.code)),
    log.error(e.__dict__)
    if e.code in [400, 401, 403, 404]: raise e
    return GET(*args, **kwargs)
  except urllib2.URLError as e:
    log.error(e)
    return GET(*args, **kwargs)
