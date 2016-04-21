from __future__ import unicode_literals

from django.db import models
from jsonfield import JSONField


class MyModel(models.Model):
    json = JSONField()
    first_name = models.CharField(max_length = 30)
    last_name = models.CharField(max_length = 30)
    email = models.EmailField()
    customer_policy = models.BooleanField(default=False)
    FRESHMAN = 'FR'
    SOPHOMORE = 'SO'
    JUNIOR = 'JR'
    SENIOR = 'SR'
    YEAR_IN_SCHOOL_CHOICES = (
        (FRESHMAN, 'Freshman'),
        (SOPHOMORE, 'Sophomore'),
        (JUNIOR, 'Junior'),
        (SENIOR, 'Sevnior'),
    )
    year_in_school = models.CharField(max_length=2,
                                      choices=YEAR_IN_SCHOOL_CHOICES,
                                      default=FRESHMAN)
    people = models.Manager()  


class DahlBookManager(models.Manager):
    def get_queryset(self):
        return super(DahlBookManager, self).get_queryset().filter(author='ravinder singh')

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)

    objects = models.Manager() # The default manager.
    dahl_objects = DahlBookManager() # The Dahl-specific manager.

    def __unicode__(self):
        return self.title

class Reporter(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()

    def __unicode__(self):              # __unicode__ on Python 2
        return "%s %s" % (self.first_name, self.last_name)

class Article(models.Model):
    headline = models.CharField(max_length=100)
    pub_date = models.DateField()

    def __unicode__(self):              # __unicode__ on Python 2
        return self.headline

class Person(models.Model):
    name = models.CharField(max_length=50)
    def __unicode__(self):
        return self.name
# class Group(models.Model):
#     name = models.CharField(max_length=128)
#     members = models.ManyToManyField(
#         Person
#     )
#     def __unicode__(self):
#         return self.name

# class Membership(models.Model):
#     invite_reason = models.CharField(max_length=64)


class Tasklist(models.Model):
    name = models.CharField(max_length=32)

    def __unicode__(self):
        return self.name


class Task(models.Model):
    name = models.TextField(max_length=32)
    tasklist = models.ForeignKey(Tasklist)

    def __unicode__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=32)
    tasklists = models.ManyToManyField(Task, through='TaskState')





class TaskState(models.Model):
    task = models.ForeignKey(Task)
    project = models.ForeignKey(Project)
    done = models.BooleanField(default=False)


class Question(models.Model):
    question_text = models.CharField(max_length=300)
    pub_date = models.DateTimeField('date published')

    def __unicode__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __unicode__(self):
        return self.choice_text


class Country(models.Model):
    country = models.CharField(max_length=200)

    def __unicode__(self):
        return self.country


class City(models.Model):
    country = models.ForeignKey(Country)
    city = models.CharField(max_length=200)

    def __unicode__(self):
        return self.city
