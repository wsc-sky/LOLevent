from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from PIL import Image
from django.utils import timezone
# Create your models here.

class UserProfile(models.Model):
    user        	= models.OneToOneField(User)
    debug       	= models.BooleanField(default=True)
    past_events 	= models.CharField(max_length=200, default=';')
    future_events	= models.CharField(max_length=200, default=';')
    like_events		= models.CharField(max_length=200, default=';')
    photo 			= models.ImageField(upload_to='',null =True, blank=True)

    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    post_save.connect(create_user_profile, sender=User)

class UserUsage(models.Model):
    user        = models.ForeignKey(User)
    datetime    = models.DateTimeField(auto_now=True)
    page        = models.CharField(max_length=50)

    class Meta:
        ordering = ['-datetime']

    def __unicode__(self):
        return self.user.get_full_name() + ' last accessed ' + self.page + ' ' + timesince(self.datetime) + ' ago'

class Event(models.Model):
	title		= models.CharField(max_length=100)
	organizer	= models.CharField(max_length=20)
	test		= models.CharField(max_length=200) #location
	pub_date    = models.CharField(max_length=100,default=timezone.now)
	p_sort		= models.IntegerField(max_length=100,default=0)
	date        = models.CharField(max_length=100,default=timezone.now)
	d_sort		= models.IntegerField(max_length=100,default=0)
	description = models.CharField(max_length=500)
	content 	= models.CharField(max_length=3000)
	like		= models.IntegerField(default=0)
	like_list	= models.CharField(max_length=1000)
	participant = models.IntegerField(default=0)
	p_email 	= models.CharField(default=0, max_length=50) 
	p_list		= models.CharField(max_length=1000)
	image		= models.ImageField(upload_to='',null =True, blank=True)


	def __str__(self):
		return self.title


class Comment(models.Model):
	event_id 	= models.IntegerField(max_length=50)
	user_name 	= models.CharField(max_length=100)
	user_id		= models.ForeignKey(User)
	content		= models.CharField(max_length=300)
	date 		= models.CharField(max_length=100,default=timezone.now)




#class user(models.Model):
	
	