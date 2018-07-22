#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module contains the ndb models that make this all possible."""

from google.appengine.ext import ndb
from google.appengine.api import memcache

__copyright__ = "Copyright (c) 2018 ‮nerB ‮taraM"
__author__ = "‮nerB ‮taraM‭"
__license__ = "MPL-2.0"

# Why I use properties instead of functions:
# It makes working with the django template system easier.


class Model(ndb.Model):
  @property
  def KEY(self):
    return self.key.id()

  @property
  def NAME(self):
    return self.__getattribute__('Name').encode('utf-8')

  @classmethod
  def SET(cls, key, **kwargs):

    name = cls.__name__

    # make three attempts at fetching to reduce error
    _ = (memcache.get(key=key, namespace=name) or
         memcache.get(key=key, namespace=name) or
         memcache.get(key=key, namespace=name))

    if _ is not None: return _

    kwargs['id'] = key
    _ = cls(**kwargs)
    _.put()

    (memcache.set(key=key, value=_, namespace=name) or
     memcache.set(key=key, value=_, namespace=name) or
     memcache.set(key=key, value=_, namespace=name))
    # make three attempts at storing to reduce error

    return _

  @classmethod
  def GET(cls, key):

    name = cls.__name__

    _ = (memcache.get(key=key, namespace=name) or
         memcache.get(key=key, namespace=name) or
         memcache.get(key=key, namespace=name))
    if _ is not None: return _

    _ = cls.get_by_id(key)
    (memcache.set(key=key, value=_, namespace=name) or
     memcache.set(key=key, value=_, namespace=name) or
     memcache.set(key=key, value=_, namespace=name))

    return _


class Channel(Model):
  @property
  def playlistURL(self):
    return '//youtube.com/playlist?list={key}'.format(
      key=self.KEY[0]+'U'+self.KEY[2:])
  Name = ndb.StringProperty()


class Video(Model):
  Published = ndb.DateTimeProperty(required=True)
  Title = ndb.StringProperty(required=True)
  Channel = ndb.KeyProperty(required=True, kind=Channel)


class User(Model):
  Subscriptions = ndb.KeyProperty(repeated=True, kind=Channel)
