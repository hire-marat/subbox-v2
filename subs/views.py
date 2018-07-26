#!/usr/bin/env python
# -*- coding: utf-8 -*-

""""""

import logging
import datetime

from django import http
from django.template import loader

from google.appengine.ext.ndb import put_multi
from subs import models
from dep import *

__copyright__ = "Copyright (c) 2018 ‮nerB ‮taraM"
__author__ = "‮nerB ‮taraM‭"
__license__ = "MPL-2.0"

log = logging.getLogger()
log.addHandler(logging.StreamHandler())
log.setLevel(logging.INFO)
log.setLevel(logging.DEBUG)


def grablast(channelId, start, count):
  """Pretty simple function to collect a group of YouTube videos

  Could definitely be improved by storing the data differently."""
  if channelId is not None:
    user = models.User.get_by_id(channelId)
    if user is None: raise KeyError

    step = 32
    subs = list(user.Subscriptions)
    videos = []

    # what do we want to see?
    for i in range(ceil(len(subs)/float(step))):
      videos.extend(
        models.Video.query(
          # we only want the videos from channels we watch
          models.Video.Channel.IN(subs[step*i:step*(i+1)])
        ).fetch()
      )

    # we want them in reverse chronological order, too
    videos.sort(key=lambda video: video.Published)

    # we only need so many
    videos = videos[start:start+count]

    # we want them now please
    return videos


def home(request):
  try:
    g = request.GET
    t = loader.get_template('web/videos.html')
    c = {'videos': grablast(
      start=int(g.get('start', 0)),
      count=int(g.get('count', 100)),
      channelId=g.get('plat'),
    )}
    return http.HttpResponse(t.render(c))

  except KeyError:
    return http.HttpResponseBadRequest(
      'User not found, please visit <a href="calibrate">calibrate</a>.')


def getSubscriptions(channelId):
  _channels = GET('/subscriptions',
    query=subscriptions
    .updates({'channelId': channelId}))
  Channels = []
  for channel in _channels:
    Channels.append(models.Channel.SET(
      key=channel['snippet']['resourceId']['channelId'],
      Name=channel['snippet']['title'],
    ))
  return Channels


def getVideos(channel, counter=None, total=None):
  playlist = channel.KEY
  log.debug('Grabbing videos for channel {counter} of {total}...'
            .format(counter=counter, total=total))
  stop = models.Video.query(
    models.Video.Channel == channel.key
  ).order(-models.Video.Published).fetch(1)
  try:
    stop = str(stop[0].KEY)
    log.debug('{channel.NAME}\'s latest video is {stop}'.format(
      channel=channel, stop=stop))
  except IndexError: stop = None

  playlist = playlist[0] + 'U' + playlist[2:]

  Videos = GET('/playlistItems',
    query=playlistItems.updates({'playlistId': playlist}),
    stop={u'contentDetails': {u'videoId': u'{}'.format(stop)}},
    pageToken='')
  Videos = [_['contentDetails']['videoId'] for _ in Videos]

  try: Videos = Videos[:Videos.index(stop)]
  except (ValueError, IndexError): pass

  PUT = []

  for i in range(ceil(len(Videos)/50.)):
    _ = GET('/videos', query=videos.updates({
      'id': ','.join(Videos[50*i:50*(i+1)])}))

    PUT.extend([
      models.Video(
        id=response['id'], Title=response['snippet']['title'],
        Channel=channel.key,
        Published=datetime.datetime.strptime(
          response['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%S.%fZ'),
      )
      for response in _
    ])

  Return = int(len(PUT))
  log.debug('{} videos grabbed in total.'.format(Return))
  put_multi(PUT)
  del PUT
  return Return, stop


def updatevideos(request):
  channelId = request.GET.get('plat')

  if channelId is None:
    return http.HttpResponseBadRequest(
      'Please supply channel ID via the query key "plat".')

  def updatevideoroutine(_channelId):
    """This didn't really work like I expected it to...

    I thought it would feed the browser data in real time, but it turns
    out that GAE doesn't support streamed responses, or if it does, I
    could find how to do it."""
    yield 'Grabbing subscriptions...'
    _subscriptions = getSubscriptions(_channelId)
    yield ' Done.<br>'

    yield 'Keying subscriptions...'
    subs = [_.key for _ in _subscriptions]
    yield ' Done.<br>'

    yield 'Updating subscriptions record...'
    user = models.User.SET(key=_channelId, Subscriptions=subs)
    user.Subscriptions = subs
    user.put()
    yield ' Done.<br>'

    total = len(_subscriptions)
    for counter, channel in enumerate(_subscriptions):
      yield ('Parsing channel '
             '<a href="{channel.playlistURL}">'
             '{channel.NAME}</a>...').format(channel=channel)
      count, stop = getVideos(channel, counter=counter, total=total)
      yield ' Grabbed {} videos'.format(count)
      # if stop is not None: yield (' stopped at '
      #                 '<a href="//youtu.be/{}">{}</a>').format(stop)
      yield '. Done.<br>'

  stream = updatevideoroutine(channelId)
  return http.HttpResponse(stream, status=200)
