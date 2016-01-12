# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db.models import signals

class Post(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created = models.DateTimeField(u'发表时间', auto_now_add = True)
    updated = models.DateTimeField(u'最后修改时间', auto_now = True)
    
    events = generic.GenericRelation('Event')

    def __unicode__(self):
        return self.title
    
    def description(self):
        return u'%s 发表了日志《%s》' % (self.author, self.title)
   

class Event(models.Model):
    user = models.ForeignKey(User)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    
    event = generic.GenericForeignKey('content_type', 'object_id')
    
    created = models.DateTimeField(u'事件发生时间', auto_now_add = True)
    
    def __unicode__(self):
        return  u"%s的事件: %s" % (self.user, self.description())
    
    def description(self):
        return self.event.description()
    


def post_post_save(sender, instance, signal, *args, **kwargs):
    post = instance
    print sender,'\n', instance, '\n',signal
    print post.created ,post.updated
    event = Event(user=post.author,event = post)
    event.save()

signals.post_save.connect(post_post_save, sender=Post)

