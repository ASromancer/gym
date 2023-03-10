from django.contrib import admin
from . import models
# Register your models here.
class BannerAdmin(admin.ModelAdmin):
	list_display=('alt_text','image_tag')
admin.site.register(models.Banners,BannerAdmin)

class ServiceAdmin(admin.ModelAdmin):
	list_display=('title','image_tag')
admin.site.register(models.Service,ServiceAdmin)

class PageAdmin(admin.ModelAdmin):
	list_display=('title',)
admin.site.register(models.Page,PageAdmin)

class FaqAdmin(admin.ModelAdmin):
	list_display=('quest',)
admin.site.register(models.Faq,FaqAdmin)

class EnquiryAdmin(admin.ModelAdmin):
	list_display=('id','enquiry_from_user', 'date_modified','age', 'weight', 'height', 'bmi')
admin.site.register(models.Enquiry,EnquiryAdmin)

class GalleryAdmin(admin.ModelAdmin):
	list_display=('title','image_tag')
admin.site.register(models.Gallery,GalleryAdmin)

class GalleryImageAdmin(admin.ModelAdmin):
	list_display=('alt_text','image_tag')
admin.site.register(models.GalleryImage,GalleryImageAdmin)

class SubPlanAdmin(admin.ModelAdmin):
	list_editable=('highlight_status','max_member')
	list_display=('title','price','max_member','validity_days','highlight_status')
admin.site.register(models.SubPlan,SubPlanAdmin)

class SubPlanFeatureAdmin(admin.ModelAdmin):
	list_display=('title','subplans')
	def subplans(self,obj):
		return " | ".join([sub.title for sub in obj.subplan.all()])
admin.site.register(models.SubPlanFeature,SubPlanFeatureAdmin)

class PlanDiscountAdmin(admin.ModelAdmin):
	list_display=('subplan','total_months','total_discount')
admin.site.register(models.PlanDiscount,PlanDiscountAdmin)

class SubscriberAdmin(admin.ModelAdmin):
	list_display=('user','image_tag','mobile')
admin.site.register(models.Subscriber,SubscriberAdmin)


class SubscriptionAdmin(admin.ModelAdmin):
	list_display=('user','plan','reg_date','price')
admin.site.register(models.Subscription,SubscriptionAdmin)

class TrainerAdmin(admin.ModelAdmin):
	list_editable=('is_active',)
	list_display=('full_name','mobile','salary','is_active','image_tag')
admin.site.register(models.Trainer,TrainerAdmin)

class NotifyAdmin(admin.ModelAdmin):
	list_display=('notify_detail','read_by_user','read_by_trainer')
admin.site.register(models.Notify,NotifyAdmin)

class NotifUserStatusAdmin(admin.ModelAdmin):
	list_display=('notif','user','status')
admin.site.register(models.NotifUserStatus,NotifUserStatusAdmin)

class AssignSubscribersAdmin(admin.ModelAdmin):
	list_display=('user','trainer')
admin.site.register(models.AssignSubscriber,AssignSubscribersAdmin)

class TrainerSalaryAdmin(admin.ModelAdmin):
	list_display=('trainer','amt','amt_date')
admin.site.register(models.TrainerSalary,TrainerSalaryAdmin)

class TrainerNotificationAdmin(admin.ModelAdmin):
	list_display=('notif_msg',)
admin.site.register(models.TrainerNotification,TrainerNotificationAdmin)

# SubscriberMsg
class TrainerMsgAdmin(admin.ModelAdmin):
	list_display=('user','trainer','message')
admin.site.register(models.TrainerMsg,TrainerMsgAdmin)

# App Setting
class AppSettingAdmin(admin.ModelAdmin):
	list_display=('image_tag',)
admin.site.register(models.AppSetting,AppSettingAdmin)

# Fitness type
class FitnessTypeAdmin(admin.ModelAdmin):
	list_display=('type_name','fitness_type_img',)
admin.site.register(models.Fitness_type,FitnessTypeAdmin)

# Fitness Exercises
class FitnessExercisesAdmin(admin.ModelAdmin):
	list_display=('exercise_name','exercise_img','type', 'times')
admin.site.register(models.Fitness_exercises,FitnessExercisesAdmin)

# Body type
class BodyTypeAdmin(admin.ModelAdmin):
	list_display=('body_type', 'body_type_img' ,'description', )
admin.site.register(models.Body_type,BodyTypeAdmin)

# User Exercies
class UserExerciesAdmin(admin.ModelAdmin):
	list_display=('body_type','fitness_type','times',)
admin.site.register(models.User_exercies,UserExerciesAdmin)

