import time
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.manager import Manager



class NewsManager(Manager):
    
    def get_item_by_pk(self,pk):
        return self.get(pk=pk, deleted=True)


    def get_items_by_id(self, pk:list[int]):
        return self.filter(pk__in=pk).exclude(deleted=True).order_by('-time')


    def get_stories(self):
        return self.filter(type='story').exclude(deleted=True).order_by('-time')


    def get_jobs(self):
        return self.filter(type='job').exclude(deleted=True).order_by('-time')


    def get_polls(self):
        return self.filter(type='poll').exclude(deleted=True).order_by('-time')

    
    def get_search(self, query:str, type:str=None):
        if type:
            return self.filter(type=type, title__contains=query).exclude(deleted=True).order_by('-time')
        return self.filter(title__contains=query).exclude(deleted=True).order_by('-time')

    def get_comments(self, ids):
        try:
            kids = [int(i) for i in ids.split(',')]
            return self.filter(parent__in=kids).exclude(deleted=True).order_by('-time')
        except Exception as ex:
            return None


class News(models.Model):

    NEWS_TYPES = ( 
        ('comment', 'Comment'),
        ('story', 'Story'),
        ('job', 'Job'),
        ('poll', 'Poll'),
    )


    by = models.CharField(verbose_name='By', max_length=500, null=True, blank=True)
    descendants = models.PositiveIntegerField(default=0)
    id = models.BigAutoField( primary_key=True,
        unique=True, null=False,auto_created=True)
    score = models.PositiveIntegerField(default=0)
    time = models.PositiveBigIntegerField(default=0)
    title = models.CharField(max_length=200, null=True, blank=True)
    type = models.CharField(max_length=200, null=False, default='comment', choices=NEWS_TYPES)
    url = models.URLField(null=True, blank=True)
    deleted = models.BooleanField(default=False, null=True, blank=True)
    dead = models.BooleanField(default=False, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    parent = models.PositiveBigIntegerField(default=0, null=True, blank=True)
    APICreated = models.BooleanField(default=False, null=True, blank=False)
    kids = models.TextField(null=True,blank=True, default=None)
    # kid, parts array[int]

    object = NewsManager()

    def __str__(self) -> str:
        return "ID -> " + str(self.id) + ", Type -> " + self.type.capitalize()

    def save(self, *args, **kwargs):
        if self.time == 0:
            self.time = int(time.time())
        super(News, self).save(*args, **kwargs)


    def delete(self):
        if self.APICreated == False:
            self.dead = True
            self.deleted = True
            return self.save()
        return super(News, self).delete()

