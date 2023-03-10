from django.shortcuts import render,redirect
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.core import serializers
from django.http import JsonResponse, HttpResponse, HttpRequest
from django.db.models import Count
from . import models
from . import forms
import stripe
import pickle
from sklearn.preprocessing import StandardScaler
import numpy as np

from datetime import timedelta
from django.utils.dateparse import parse_datetime

# Create your views here.
def home(request):
	banners=models.Banners.objects.all()
	services=models.Service.objects.all()[:3]
	gimgs=models.GalleryImage.objects.all().order_by('-id')[:9]
	return render(request, 'home.html',{'banners':banners,'services':services,'gimgs':gimgs})

# PageDetail
def page_detail(request,id):
	page=models.Page.objects.get(id=id)
	return render(request, 'page.html',{'page':page})

# FAQ
def faq_list(request):
	faq=models.Faq.objects.all()
	return render(request, 'faq.html',{'faqs':faq})

# Contact
def contact_page(request):
	return render(request, 'contact_us.html')

# Show galleries
def gallery(request):
	gallery=models.Gallery.objects.all().order_by('-id')
	return render(request, 'gallery.html',{'gallerys':gallery})

# Show gallery photos
def gallery_detail(request,id):
	gallery=models.Gallery.objects.get(id=id)
	gallery_imgs=models.GalleryImage.objects.filter(gallery=gallery).order_by('-id')
	return render(request, 'gallery_imgs.html',{'gallery_imgs':gallery_imgs,'gallery':gallery})

# Subscription Plans
def pricing(request):
	pricing=models.SubPlan.objects.annotate(total_members=Count('subscription__id')).all().order_by('price')
	dfeatures=models.SubPlanFeature.objects.all();
	return render(request, 'pricing.html',{'plans':pricing,'dfeatures':dfeatures})

# SignUp
def signup(request):
	msg=None
	if request.method=='POST':
		form=forms.SignUp(request.POST)
		if form.is_valid():
			form.save()
			msg='Thank you for register.'
	form=forms.SignUp
	return render(request, 'registration/signup.html',{'form':form,'msg':msg})

# Checkout
def checkout(request,plan_id):
	planDetail=models.SubPlan.objects.get(pk=plan_id)
	return render(request, 'checkout.html',{'plan':planDetail})

stripe.api_key='sk_test_51M5SQuBbzOxKyHAibVpQzhACTKKVAAXCt135xyLo1RFDagwwN8ltY4m87H9W8WkXleFcwDBCXHBVV7mUqMzZBxse00QxlbudQo'
def checkout_session(request,plan_id):
	plan=models.SubPlan.objects.get(pk=plan_id)
	session=stripe.checkout.Session.create(
		payment_method_types=['card'],
		line_items=[{
	      'price_data': {
	        'currency': 'usd',
	        'product_data': {
	          'name': plan.title,
	        },
	        'unit_amount': plan.price*100,
	      },
	      'quantity': 1,
	    }],
	    mode='payment',

	    success_url='http://127.0.0.1:8000/pay_success?session_id={CHECKOUT_SESSION_ID}',
	    cancel_url='http://127.0.0.1:8000/pay_cancel',
	    client_reference_id=plan_id
	)
	return redirect(session.url, code=303)

# Success
def pay_success(request):
	session = stripe.checkout.Session.retrieve(request.GET['session_id'])
	plan_id=session.client_reference_id
	plan=models.SubPlan.objects.get(pk=plan_id)
	user=request.user
	models.Subscription.objects.create(
		plan=plan,
		user=user,
		price=plan.price
	)
	subject='Order Email'
	html_content=get_template('orderemail.html').render({'title':plan.title})
	from_email='n19dccn055@student.ptithcm.edu.vn'
	msg = EmailMessage(subject, html_content, from_email, ['n19dccn055@student.ptithcm.edu.vn'])
	msg.content_subtype = "html"
	msg.send()
	return render(request, 'success.html')


# Cancel
def pay_cancel(request):
	return render(request, 'cancel.html')

# User Dashboard Section Start
def user_dashboard(request):
	try:
		current_plan=models.Subscription.objects.get(user=request.user)
		my_trainer=models.AssignSubscriber.objects.get(user=request.user)
	except:
		msg_err = "You haven't assigned to any trainer!"
		return render(request, 'user/dashboard.html', {'msg_err' : msg_err})
	else:
		enddate=current_plan.reg_date + timedelta(days=current_plan.plan.validity_days)  # type: ignore

		# Notification
		data=models.Notify.objects.all().order_by('-id')
		notifStatus=False
		jsonData=[]
		totalUnread=0
		for d in data:
			try:
				notifStatusData=models.NotifUserStatus.objects.get(user=request.user,notif=d)
				if notifStatusData:
					notifStatus=True
			except models.NotifUserStatus.DoesNotExist:
				notifStatus=False
			if not notifStatus:
				totalUnread=totalUnread+1

		return render(request, 'user/dashboard.html',{
			'current_plan':current_plan,
			'my_trainer':my_trainer,
			'total_unread':totalUnread,
			'enddate':enddate
		})
	
# Edit Profile Form
def update_profile(request):
	msg=None
	if request.method=='POST':
		form=forms.ProfileForm(request.POST,instance=request.user)
		if form.is_valid():
			form.save()
			msg='Data has been saved'
	form=forms.ProfileForm(instance=request.user)
	return render(request, 'user/update-profile.html',{'form':form,'msg':msg})

# Trainer Login
def trainerlogin(request):
	msg=''
	name = 'username'
	if request.method=='POST':
		username=request.POST['username']
		pwd=request.POST['pwd']
		trainer=models.Trainer.objects.filter(username=username,pwd=pwd).count()
		if trainer > 0:
			trainer=models.Trainer.objects.filter(username=username,pwd=pwd).first()
			request.session['trainerLogin']=True
			request.session['trainerid']=trainer.id  # type: ignore
			return redirect('/trainer_dashboard')
		else:
			msg='Invalid!!'
	form=forms.TrainerLoginForm
	return render(request, 'trainer/login.html',{'form':form,'msg':msg})

# Trainer Logout
def trainerlogout(request):
	del request.session['trainerLogin']
	return redirect('/trainerlogin')

# Trainer Dashboard
def trainer_dashboard(request):
	return render(request, 'trainer/dashboard.html')

# Trainer Profile
def trainer_profile(request):
	t_id=request.session['trainerid']
	trainer=models.Trainer.objects.get(pk=t_id)
	msg=None
	if request.method=='POST':
		form=forms.TrainerProfileForm(request.POST,request.FILES,instance=trainer)
		if form.is_valid():
			form.save()
			msg='Profile has been updated'
	form=forms.TrainerProfileForm(instance=trainer)
	return render(request, 'trainer/profile.html',{'form':form,'msg':msg})

# Trainer Subscribers
def trainer_subscribers(request):
	trainer=models.Trainer.objects.get(pk=request.session['trainerid'])
	trainer_subs=models.AssignSubscriber.objects.filter(trainer=trainer).order_by('-id')
	return render(request, 'trainer/trainer_subscribers.html',{'trainer_subs':trainer_subs})

# Trainer Payment
def trainer_payments(request):
	trainer=models.Trainer.objects.get(pk=request.session['trainerid'])
	trainer_pays=models.TrainerSalary.objects.filter(trainer=trainer).order_by('-id')
	return render(request, 'trainer/trainer_payments.html',{'trainer_pays':trainer_pays})

# Trainer Change Password
def trainer_changepassword(request):
	msg=None
	if request.method=='POST':
		new_password=request.POST['new_password']
		updateRes=models.Trainer.objects.filter(pk=request.session['trainerid']).update(pwd=new_password)
		if updateRes:
			del request.session['trainerLogin']
			return redirect('/trainerlogin')
		else:
			msg='Something is wrong!!'
	form=forms.TrainerChangePassword
	return render(request, 'trainer/trainer_changepassword.html',{'form':form})

# Trainer Notifications
def trainer_notifs(request):
	data=models.TrainerNotification.objects.all().order_by('-id')
	trainer=models.Trainer.objects.get(id=request.session['trainerid'])
	jsonData=[]
	totalUnread=0
	notifStatus = False
	for d in data:
		try:
			notifStatusData=models.NotifTrainerStatus.objects.get(trainer=trainer,notif=d)
			if notifStatusData:
				notifStatus=True
		except models.NotifTrainerStatus.DoesNotExist:
			notifStatus=False
		if not notifStatus:
			totalUnread=totalUnread+1
		jsonData.append({
			'pk':d.id,  # type: ignore
			'notify_detail':d.notif_msg,
			'notifStatus':notifStatus
		})
	return render(request, 'trainer/notifs.html',{'notifs':jsonData,'totalUnread':totalUnread})

# Mark Read By trainer
def mark_read_trainer_notif(request):
	notif=request.GET['notif']
	notif=models.TrainerNotification.objects.get(pk=notif)
	trainer=models.Trainer.objects.get(id=request.session['trainerid'])
	models.NotifTrainerStatus.objects.create(notif=notif,trainer=trainer,status=True)

	# Count Unread
	totalUnread=0
	data=models.TrainerNotification.objects.all().order_by('-id')
	notifStatus = False
	for d in data:
		try:
			notifStatusData=models.NotifTrainerStatus.objects.get(trainer=trainer,notif=d)
			if notifStatusData:
				notifStatus=True
		except models.NotifTrainerStatus.DoesNotExist:
			notifStatus=False
		if not notifStatus:
			totalUnread=totalUnread+1

	return JsonResponse({'bool':True,'totalUnread':totalUnread})

# Trainer Messages
def trainer_msgs(request):
	data=models.TrainerMsg.objects.all().order_by('-id')
	return render(request, 'trainer/msgs.html',{'msgs':data})

# Notifications
def notifs(request):
	data=models.Notify.objects.all().order_by('-id')
	return render(request, 'notifs.html')

# Get all notifications
def get_notifs(request):
	data=models.Notify.objects.all().order_by('-id')
	notifStatus=False
	jsonData=[]
	totalUnread=0
	for d in data:
		try:
			notifStatusData=models.NotifUserStatus.objects.get(user=request.user,notif=d)
			if notifStatusData:
				notifStatus=True
		except models.NotifUserStatus.DoesNotExist:
			notifStatus=False
		if not notifStatus:
			totalUnread=totalUnread+1
		jsonData.append({
				'pk':d.pk,
				'notify_detail':d.notify_detail,
				'notifStatus':notifStatus
			})
	# jsonData=serializers.serialize('json', data)
	return JsonResponse({'data':jsonData,'totalUnread':totalUnread})

# Mark Read By user
def mark_read_notif(request):
	notif=request.GET['notif']
	notif=models.Notify.objects.get(pk=notif)
	user=request.user
	models.NotifUserStatus.objects.create(notif=notif,user=user,status=True)
	return JsonResponse({'bool':True})

# Enquiry
def enquiry(request):
	msg=''

	if request.method=='POST':
		form=forms.EnquiryForm(request.POST)
		print(form.data)
		if form.is_valid():
			w = form.cleaned_data['weight']
			h = form.cleaned_data['height']/100.0
			form_bmi = round(w / (h * h), 2)
			print(f'weight {w}, height {h}, bmi {form_bmi}')
			new_form=form.save(commit=False)
			new_form.enquiry_from_user=request.user
			new_form.bmi = form_bmi
			new_form.save()
			msg='Data has been saved'
		else:
			msg='Invalid Response!!'

	# l???y l???ch s??? ch??? s??? c???a user ????
	timelines = models.Enquiry.objects.filter(enquiry_from_user=request.user).order_by('-date_modified').values('bmi', 'age', 'weight', 'height','date_modified')
	try:
		user = models.Enquiry.objects.filter(enquiry_from_user=request.user).latest('date_modified')
	except:
		form = forms.EnquiryForm()
		msg = 'There is no data about your circumstance, please update your data!'
		return render(request, 'user/enquiry.html', {'form':form, 'msg': msg})
	else:
		form=forms.EnquiryForm(instance=user)
		w = models.Enquiry.objects.filter(enquiry_from_user=request.user).values('weight').latest('date_modified')['weight']
		h = models.Enquiry.objects.filter(enquiry_from_user=request.user).values('height').latest('date_modified')['height']/100.0
		bmi = round(w / (h * h), 2)
		return render(request, 'user/enquiry.html',{'form':form,'msg':msg, 'bmi': bmi, 'timelines':timelines})
		



def show_timeline_info(request, enquiry_time):
	time = parse_datetime(enquiry_time)
	print('Time is ',time)
	data = models.Enquiry.objects.get(date_modified=time)
	if time != None:
		time = time.strftime('%Y-%m-%d %H:%M:%S')
	return HttpResponse(f'''
		<div class="row">
			<div class="h4 text-primary text-center">Datetime: {time}</div>
		</div>
		<div class="row">
			<div class="col-md">
				<label class="text-capitalize" for="age">age</label>
				<input id="age" type="number" class="form-control" value={data.age} readonly/>

				<label class="text-capitalize" for="weight">weight</label>
				<input id="weight" type="number" class="form-control" value={data.weight} readonly/>

				<label class="text-capitalize" for="height">height</label>
				<input id="height" type="number" class="form-control" value={data.height} readonly/>

				<label class="text-capitalize" for="neck">neck</label>
				<input id="neck" type="number" class="form-control" value={data.neck} readonly/>

				<label class="text-capitalize" for="chest">chest</label>
				<input id="chest" type="number" class="form-control" value={data.chest} readonly/>

				<label class="text-capitalize" for="abdomen">abdomen</label>
				<input id="abdomen" type="number" class="form-control" value={data.abdomen} readonly/>

				<label class="text-capitalize" for="hip">hip</label>
				<input id="hip" type="number" class="form-control" value={data.hip} readonly/>
			</div>
			<div class="col-md">
				<label class="text-capitalize" for="thigh">thigh</label>
				<input id="thigh" type="number" class="form-control" value={data.thigh} readonly/>

				<label class="text-capitalize" for="knee">knee</label>
				<input id="knee" type="number" class="form-control" value={data.knee} readonly/>

				<label class="text-capitalize" for="ankle">ankle</label>
				<input id="ankle" type="number" class="form-control" value={data.ankle} readonly/>

				<label class="text-capitalize" for="biceps">biceps</label>
				<input id="biceps" type="number" class="form-control" value={data.biceps} readonly/>

				<label class="text-capitalize" for="forearm">forearm</label>
				<input id="forearm" type="number" class="form-control" value={data.forearm} readonly/>

				<label class="text-capitalize" for="wrist">wrist</label>
				<input id="wrist" type="number" class="form-control" value={data.wrist} readonly/>

				<label class="text-capitalize" for="bmi">bmi</label>
				<input id="bmi" type="number" class="form-control" value={data.bmi} readonly/>
			</div>
		</div>
	''')


def show_latest_info(request):
	user = request.user
	data = models.Enquiry.objects.latest('date_modified')
	return HttpResponse(
		f'''
		<div class="row">
			<div class="col-md">
				<label class="text-capitalize" for="age">age</label>
				<input id="age" type="number" class="form-control" value={data.age} readonly/>

				<label class="text-capitalize" for="weight">weight</label>
				<input id="weight" type="number" class="form-control" value={data.weight} readonly/>

				<label class="text-capitalize" for="height">height</label>
				<input id="height" type="number" class="form-control" value={data.height} readonly/>

				<label class="text-capitalize" for="neck">neck</label>
				<input id="neck" type="number" class="form-control" value={data.neck} readonly/>

				<label class="text-capitalize" for="chest">chest</label>
				<input id="chest" type="number" class="form-control" value={data.chest} readonly/>

				<label class="text-capitalize" for="abdomen">abdomen</label>
				<input id="abdomen" type="number" class="form-control" value={data.abdomen} readonly/>

				<label class="text-capitalize" for="hip">hip</label>
				<input id="hip" type="number" class="form-control" value={data.hip} readonly/>
			</div>
			<div class="col-md">
				<label class="text-capitalize" for="thigh">thigh</label>
				<input id="thigh" type="number" class="form-control" value={data.thigh} readonly/>

				<label class="text-capitalize" for="knee">knee</label>
				<input id="knee" type="number" class="form-control" value={data.knee} readonly/>

				<label class="text-capitalize" for="ankle">ankle</label>
				<input id="ankle" type="number" class="form-control" value={data.ankle} readonly/>

				<label class="text-capitalize" for="biceps">biceps</label>
				<input id="biceps" type="number" class="form-control" value={data.biceps} readonly/>

				<label class="text-capitalize" for="forearm">forearm</label>
				<input id="forearm" type="number" class="form-control" value={data.forearm} readonly/>

				<label class="text-capitalize" for="wrist">wrist</label>
				<input id="wrist" type="number" class="form-control" value={data.wrist} readonly/>

				<label class="text-capitalize" for="bmi">bmi</label>
				<input id="bmi" type="number" class="form-control" value={data.bmi} readonly/>
			</div>
		</div>
	'''
	)



#=====================================================================================================================================================================

# BodyFat Prediction
model = pickle.load(open('main/model.pkl', 'rb'))
def predict_body_fat(model, X_test):
    density = model.predict(X_test)
    fat = ((4.95/density[0]) - 4.5)*100
    return fat

def predict(request):  
    user = request.user
    try:
        data = models.Enquiry.objects.filter(enquiry_from_user_id=user).values_list('age', 'neck', 'chest', 'abdomen', 'hip', 'thigh', 'knee', 'ankle', 'biceps', 'forearm', 'wrist', 'bmi').latest('date_modified')
        bmi = models.Enquiry.objects.filter(enquiry_from_user_id=user).latest('date_modified').bmi
    except:
        msg_err = 'Please back to update your circumstance data!'
        return render(request, 'user/predict.html', {'msg_err': msg_err})
    else:
        if bmi != None:
           bmi = round(bmi , 2)
        fat = round(predict_body_fat(model, [data]), 2)
        body_type_code = get_body_type(fat, bmi)
        body_type_name = get_name_of_body_type(body_type_code)
        body_types=models.Body_type.objects.all()


        ratios = {}

        para = []
        for i in data:
                para.append(i)
        para.pop(0)

	    # t??nh h??? s??? b??i t???p c???a t???ng ideal body type so v???i currently
        for body_type in body_types:
                ideal_para = []
                ideal_para.append(body_type.neck)
                ideal_para.append(body_type.chest)
                ideal_para.append(body_type.abdomen)
                ideal_para.append(body_type.hip)
                ideal_para.append(body_type.thigh)
                ideal_para.append(body_type.knee)
                ideal_para.append(body_type.ankle)
                ideal_para.append(body_type.biceps)
                ideal_para.append(body_type.forearm)
                ideal_para.append(body_type.wrist)
                ideal_para.append(body_type.bmi)
	            #ideal_para.append(body_type.fat)

                ratio = []

                for i in range(0,len(para)):
                                ratio.append(para[i]/ideal_para[i])

                sum_ratio = 0
                for i in range(0,len(ratio)):
                                sum_ratio += ratio[i]

                sum_ratio=sum_ratio/len(ratio)
                # get_correclation_coefficient
                bmi = para[-1]
                user_body_type = get_body_type(fat,bmi)
                fat_ratio = get_correclation_coefficient(user_body_type,body_type.body_type)
                times_ratio = round(100*((sum_ratio + fat_ratio*3)/4))
                type_name = body_type.body_type
                ratios[type_name] = times_ratio

        print(ratios)
        min_ratio= min(ratios.values())
        max_ratio= max(ratios.values())

        return render(request, 'user/predict.html' , {'body_type_name':body_type_name, 
												'body_types':body_types, 'fat':fat, "bmi": bmi, 'ratios': ratios,
												'min_ratio': min_ratio, 'max_ratio': max_ratio})
    

# Calculate percentage of user


# =======body fat==================
# 1 essential = np.arange(2.0, 5.0)
# 2 athletes = np.arange(6.0, 13.0)
# 3 fitness = np.arange(14.0, 17.0)
# 4 average = np.arange(18.0, 24.0)
# 5 obese > 25.0

# =======BMI=======================
# 1 underweight < 18.5
# 2 normal = np.arange(18.5, 24.9)
# 3 overweight = np.arange(25.0, 29.9)
# 4 obese = np.arange(30.0, 34.9)
# 5 extremely_obese > 35

def get_bodyfat_category(x):
    if 2.0 <= x <= 5.0:
        return 1
    elif 6.0 <= x <= 13.0:
        return 2
    elif 14.0 <= x <= 17.0:
        return 3
    elif 18.0 <= x <= 24.0:
        return 4
    else:
        return 5

def get_bmi_category(bmi):
    if 0.0 < bmi < 18.5:
        return 1
    elif 18.5 <= bmi <= 24.9:
        return 2
    elif 25.0 <= bmi <= 29.9:
        return 3
    elif 30.0 <= bmi <= 34.9:
        return 4
    else:
        return 5

def get_body_type(fat, bmi):
    fat = get_bodyfat_category(fat)
    bmi = get_bmi_category(bmi)
    if (fat in (2, 3, 4) and bmi == 2) or (fat == 2 and bmi == 3) or (fat == 3 and bmi == 4):
        return 'A'
    elif (fat in (2, 3) and bmi == 1) or (fat == 1 and bmi == 2):
        return 'B'
    elif (fat == 5 and bmi == 2) or (fat in (3, 4, 5) and bmi == 3) or (fat in (4, 5) and bmi == 4) or (fat == 4 and bmi == 4):
        return 'C'
    elif fat == 1 and bmi == 1:
        return 'D'
    elif fat == 5 and bmi == 5:
        return 'E'

def get_name_of_body_type(body_type_code):
	bodyTypeNameDict = {
		'A': 'Normal',
		'B': 'Slightly thinner',
		'C': 'slightly fatter',
		'D': 'A lot thinner',
		'E': 'A lot fatter'
	}

	return bodyTypeNameDict[body_type_code]

def get_correclation_coefficient(user_body_type, choosed_body_type):
	if user_body_type == 'A' and choosed_body_type == 'Slim':
		return 1.1
	elif user_body_type == 'A' and choosed_body_type == 'Normal':
		return 0.95
	elif user_body_type == 'A' and choosed_body_type == 'Muscular':
		return 1.31
	elif user_body_type == 'B' and choosed_body_type == 'Slim':
		return 0.82
	elif user_body_type == 'B' and choosed_body_type == 'Normal':
		return 0.7
	elif user_body_type == 'B' and choosed_body_type == 'Muscular':
		return 0.97
	elif user_body_type == 'C' and choosed_body_type == 'Slim':
		return 1.32
	elif user_body_type == 'C' and choosed_body_type == 'Normal':
		return 1.14
	elif user_body_type == 'C' and choosed_body_type == 'Muscular':
		return 1.56
	elif user_body_type == 'D' and choosed_body_type == 'Slim':
		return 0.53
	elif user_body_type == 'D' and choosed_body_type == 'Normal':
		return 0.45
	elif user_body_type == 'D' and choosed_body_type == 'Muscular':
		return 0.63
	elif user_body_type == 'E' and choosed_body_type == 'Slim':
		return 1.53
	elif user_body_type == 'E' and choosed_body_type == 'Normal':
		return 1.32
	elif user_body_type == 'E' and choosed_body_type == 'Muscular':
		return 1.81
	else:
		return 0
	

# Show Exercises Type
def fitness_type(request):
	fitness_type=models.Fitness_type.objects.all().order_by('-type_name')
	return render(request, 'user/fitness_type.html',{'fitness_types':fitness_type})

# Show Exercises images
def fitness_ex(request, type_name):
	fitness_type=models.Fitness_type.objects.get(type_name=type_name)
	fitness_ex_imgs=models.Fitness_exercises.objects.filter(type=fitness_type).order_by('-id')
	return render(request, 'user/fitness_ex.html',{'fitness_ex_imgs':fitness_ex_imgs, 'fitness_type':fitness_type})


# Show Exercies types
def user_exercises_type(request, body_type):
	body_type=models.Body_type.objects.get(body_type=body_type)
	u_e_t = models.User_exercies.objects.filter(body_type=body_type).values_list('fitness_type_id')
	user_exercises_type =[]
	for x in u_e_t:
		user_exercises_type.extend(x)
	img_dic = {}
	for x_img in user_exercises_type:
		img_dic[x_img] = (models.Fitness_type.objects.get(type_name = x_img).fitness_type_img.url) 
	print(img_dic)
	# user parameter calculate
	user = request.user
	data = models.Enquiry.objects.filter(enquiry_from_user_id=user).values_list('age', 'neck', 'chest', 'abdomen', 'hip', 'thigh', 'knee', 'ankle', 'biceps', 'forearm', 'wrist', 'bmi').latest('date_modified')
	fat = round(predict_body_fat(model, [data]), 2)
	para = []
	for i in data:
		para.append(i)
	para.pop(0)
	#para.append(fat)
	#ideal=models.Body_type.objects.get(body_type=body_type)
	ideal_para = []
	ideal_para.append(body_type.neck)
	ideal_para.append(body_type.chest)
	ideal_para.append(body_type.abdomen)
	ideal_para.append(body_type.hip)
	ideal_para.append(body_type.thigh)
	ideal_para.append(body_type.knee)
	ideal_para.append(body_type.ankle)
	ideal_para.append(body_type.biceps)
	ideal_para.append(body_type.forearm)
	ideal_para.append(body_type.wrist)
	ideal_para.append(body_type.bmi)
	#ideal_para.append(body_type.fat)

	ratio = []

	for i in range(0,len(para)):
		ratio.append(para[i]/ideal_para[i])
	
	sum_ratio = 0
	for i in range(0,len(ratio)):
		sum_ratio += ratio[i]

	sum_ratio = sum_ratio/len(ratio)
	# get_correclation_coefficient
	bmi = para[-1]
	user_body_type = get_body_type(fat,bmi)
	fat_ratio = get_correclation_coefficient(user_body_type,body_type.body_type)
	times_ratio = (sum_ratio + fat_ratio*3)/4
	request.session['token'] = times_ratio 
	return render(request, 'user/user_exercises_type.html',{ 'body_type':body_type, 'user_exercises_types':user_exercises_type, 'img_dic': img_dic})
	


	
	# bodyType_content = '''<section class="container my-4" id="userFitness"><div class="row">'''

	# for ex_type in user_exercises_type:
	# 	bodyType_content += (f'''
	# 		<div class="col-md-4 mb-4">
	# 			<div class="card">
	# 				<div class="card-body">
	# 				<h5 class="card-title text-capitalize">{ex_type.get('fitness_type_id')}</h5>
	# 				<div
	# 					hx-get="/userexcercises/{ex_type.get('fitness_type_id')}"
	# 					hx-trigger="click"
	# 					hx-swap="innerHTML"
	# 					hx-target="#userFitness"
						
	# 					href="#" class="btn btn-primary">View All</div>
	# 				</div>
	# 			</div>
	# 		</div>
	# 	''')


	# bodyType_content.join('''</div></section>''')

	# return HttpResponse(bodyType_content)


def user_exercises(request, type_name):
	fitness_ex=models.Fitness_exercises.objects.filter(type = type_name).order_by('-id')
	ratio = request.session['token']
	return render(request, 'user/user_excercises.html',{'fitness_ex':fitness_ex, 'ratio':ratio})

	# exercise_content = f'''
	# 	<a 
	# 	href="/predict" class="btn btn-primary mb-4" role="button">Back</a>
	# '''
	# exercise_content += '''<div class="row">'''
	

	# for exercise in fitness_ex:
	# 	exercise_content += (f'''
	# 		<div class="col-md-4 mb-4">
	# 			<div class="card">
	# 				<img src="{exercise.exercise_img.url}" class="card-img-top" alt="">
	# 			</div>
	# 			<h5 class="text-center mb-4 section-heading border-bottom pb-2">{exercise.exercise_name}</h1>
	# 		</div>
	# 	''')

	# exercise_content.join('''</div>''')

	
	# return HttpResponse(exercise_content)


