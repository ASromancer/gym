from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver 

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from datetime import datetime

import json



# Banners
class Banners(models.Model):
	img=models.ImageField(upload_to="banners/")
	alt_text=models.CharField(max_length=150)

	class Meta:
		verbose_name_plural='Banners'

	def __str__(self):
		return self.alt_text

	def image_tag(self):
		return mark_safe('<img src="%s" width="80" heigth="30" />' % (self.img.url))

# Services
class Service(models.Model):
	title=models.CharField(max_length=150)
	detail=models.TextField()
	img=models.ImageField(upload_to="services/",null=True)

	def __str__(self):
		return self.title

	def image_tag(self):
		return mark_safe('<img src="%s" width="80" />' % (self.img.url))

# Pages
class Page(models.Model):
	title=models.CharField(max_length=200)
	detail=models.TextField()

	def __str__(self):
		return self.title

# FAQ
class Faq(models.Model):
	quest=models.TextField()
	ans=models.TextField()

	def __str__(self):
		return self.quest

# Enquiry Model
class Enquiry(models.Model):
	enquiry_from_user=models.ForeignKey(User, on_delete=models.CASCADE,null=True,related_name='report_from_user',blank=True)
	date_modified = models.DateTimeField(default=datetime.now, blank=True)
	age=models.IntegerField(null=True, blank=True)
	weight=models.FloatField(null=True, blank=True)
	height=models.FloatField(null=True, blank=True)
	neck=models.FloatField(null=True, blank=True)
	chest=models.FloatField(null=True, blank=True)
	abdomen=models.FloatField(null=True, blank=True)
	hip=models.FloatField(null=True, blank=True)
	thigh=models.FloatField(null=True, blank=True)
	knee=models.FloatField(null=True, blank=True)
	ankle=models.FloatField(null=True, blank=True)
	biceps=models.FloatField(null=True, blank=True)
	forearm=models.FloatField(null=True, blank=True)
	wrist=models.FloatField(null=True, blank=True)
	bmi=models.FloatField(null=True, blank=True)


# Gallery Model
class Gallery(models.Model):
	title=models.CharField(max_length=150)
	detail=models.TextField()
	img=models.ImageField(upload_to="gallery/",null=True)

	class Meta:
		verbose_name_plural='Galleries'

	def __str__(self):
		return self.title

	def image_tag(self):
		return mark_safe('<img src="%s" width="80" />' % (self.img.url))

# Gallery Images
class GalleryImage(models.Model):
	gallery=models.ForeignKey(Gallery, on_delete=models.CASCADE,null=True)
	alt_text=models.CharField(max_length=150)
	img=models.ImageField(upload_to="gallery_imgs/",null=True)

	def __str__(self):
		return self.alt_text

	def image_tag(self):
		return mark_safe('<img src="%s" width="80" />' % (self.img.url))


# Subscription Plans
class SubPlan(models.Model):
	title=models.CharField(max_length=150)
	price=models.IntegerField()
	max_member=models.IntegerField(null=True)
	highlight_status=models.BooleanField(default=False,null=True)
	validity_days=models.IntegerField(null=True)

	def __str__(self):
		return self.title

# Subscription Plans Features
class SubPlanFeature(models.Model):
	# subplan=models.ForeignKey(SubPlan, on_delete=models.CASCADE,null=True)
	subplan=models.ManyToManyField(SubPlan)
	title=models.CharField(max_length=150)

	def __str__(self):
		return self.title

# Package Discounts
class PlanDiscount(models.Model):
	subplan=models.ForeignKey(SubPlan, on_delete=models.CASCADE,null=True)
	total_months=models.IntegerField()
	total_discount=models.IntegerField()

	def __str__(self):
		return str(self.total_months)

# Subscriber
class Subscriber(models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE,null=True)
	mobile=models.CharField(max_length=20)
	address=models.TextField()
	img=models.ImageField(upload_to="subs/",null=True)

	def __str__(self):
		return str(self.user)

	def image_tag(self):
		if self.img:
			return mark_safe('<img src="%s" width="80" />' % (self.img.url))
		else:
			return 'no-image'

@receiver(post_save,sender=User)
def create_subscriber(sender,instance,created,**kwrags):
	if created:
		Subscriber.objects.create(user=instance)

# Subscription
class Subscription(models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE,null=True)
	plan=models.ForeignKey(SubPlan, on_delete=models.CASCADE,null=True)
	price=models.CharField(max_length=50)
	reg_date=models.DateField(auto_now_add=True,null=True)

# Trainer
class Trainer(models.Model):
	full_name=models.CharField(max_length=100)
	username=models.CharField(max_length=100,null=True)
	pwd=models.CharField(max_length=50,null=True)
	mobile=models.CharField(max_length=100)
	address=models.TextField()
	is_active=models.BooleanField(default=False)
	detail=models.TextField()
	img=models.ImageField(upload_to="trainers/")
	salary=models.IntegerField(default=0)

	facebook=models.CharField(max_length=200,null=True)
	twitter=models.CharField(max_length=200,null=True)
	pinterest=models.CharField(max_length=200,null=True)
	youtube=models.CharField(max_length=200,null=True)

	def __str__(self):
		return str(self.full_name)

	def image_tag(self):
		if self.img:
			return mark_safe('<img src="%s" width="80" />' % (self.img.url))
		else:
			return 'no-image'

# Notifications Json Response Via Ajax
class Notify(models.Model):
	notify_detail=models.TextField()
	read_by_user=models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
	read_by_trainer=models.ForeignKey(Trainer, on_delete=models.CASCADE,null=True,blank=True)

	def __str__(self):
		return str(self.notify_detail)

# Markas Read Notification By User
class NotifUserStatus(models.Model):
	notif=models.ForeignKey(Notify, on_delete=models.CASCADE)
	user=models.ForeignKey(User, on_delete=models.CASCADE)
	status=models.BooleanField(default=False)

	class Meta:
		verbose_name_plural='Notification Status'

# Assign Subscriber to Trainer
class AssignSubscriber(models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE,null=True)
	trainer=models.ForeignKey(Trainer, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.user)


# TrainerSalary Model
class TrainerSalary(models.Model):
	trainer=models.ForeignKey(Trainer, on_delete=models.CASCADE)
	amt=models.IntegerField()
	amt_date=models.DateField()
	remarks=models.TextField(blank=True)

	class Meta:
		verbose_name_plural='Trainer Salary'

	def __str__(self):
		return str(self.trainer.full_name)

# Trainer Notifications
class TrainerNotification(models.Model):
	notif_msg=models.TextField()

	def __str__(self):
		return str(self.notif_msg)

	# def save(self,*args,**kwargs):
	# 	super(TrainerNotification, self).save(*args,**kwargs)
	# 	channel_layer=get_channel_layer()
	# 	notif=self.notif_msg
	# 	total=TrainerNotification.objects.all().count()
	# 	async_to_sync(channel_layer.group_send)(
	# 		'noti_group_name',{
	# 			'type':'send_notification',
	# 			'value':json.dumps({'notif':notif,'total':total})
	# 		}
	# 	)

# Markas Read Notification By Trainer
class NotifTrainerStatus(models.Model):
	notif=models.ForeignKey(TrainerNotification, on_delete=models.CASCADE)
	trainer=models.ForeignKey(Trainer, on_delete=models.CASCADE)
	status=models.BooleanField(default=False)

	class Meta:
		verbose_name_plural='Trainer Notification Status'

# SubscriberMsg
class TrainerMsg(models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE,null=True)
	trainer=models.ForeignKey(Trainer, on_delete=models.CASCADE,null=True)
	message=models.TextField()

	class Meta:
		verbose_name_plural='Messages For Trainer'

# App setting
class AppSetting(models.Model):
	logo_img=models.ImageField(upload_to='app_logos/')

	def image_tag(self):
		return mark_safe('<img src="%s" width="80" />' % (self.logo_img.url))

# Fitness type
class Fitness_type(models.Model):
	type_name = models.CharField(primary_key=True ,max_length=50)

	class Meta:
		verbose_name_plural='Fitness type'

# Fitness Exercies
class Fitness_exercises(models.Model):
	exercise_name = models.CharField(max_length=50)
	exercise_img = models.ImageField(upload_to="Fitness_exercises/")
	description = models.TextField(null=True, blank=True)
	type = models.ForeignKey(Fitness_type, on_delete=models.CASCADE,null=True)
	class Meta:
		verbose_name_plural='Fitness Exercies' 

class Body_type(models.Model):
	body_type = models.CharField(primary_key=True,max_length=50)
	description = models.TextField(null=True, blank=True)
	class Meta:
		verbose_name_plural='Body types' 
		
# User Exercies
class User_exercies(models.Model):
	body_type = models.ForeignKey(Body_type, on_delete=models.CASCADE,null=True)
	fitness_type = models.ForeignKey(Fitness_type, on_delete=models.CASCADE,null=True)
	times = models.IntegerField(null=True, blank=True)
	class Meta:
		verbose_name_plural='User Exercies' 
