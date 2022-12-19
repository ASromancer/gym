from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from . import models

class EnquiryForm(forms.ModelForm):
	class Meta:
		model=models.Enquiry
		fields=('age', 'weight', 'height' 'neck', 'chest', 'abdomen', 'hip', 'thigh', 'knee', 'ankle', 'biceps', 'forearm', 'wrist', 'bmi')
		widgets = {'EnquiryForm': forms.HiddenInput()}
		fields=("__all__")

class SignUp(UserCreationForm):
	class Meta:
		model=User
		fields=('first_name','last_name','email','username','password1','password2')

class ProfileForm(UserChangeForm):
	class Meta:
		model=User
		fields=('first_name','last_name','email','username')

class TrainerLoginForm(forms.ModelForm):
	class Meta:
		model=models.Trainer
		fields=('username','pwd')

class TrainerProfileForm(forms.ModelForm):
	class Meta:
		model=models.Trainer
		fields=('full_name','mobile','address','detail','img')

class TrainerChangePassword(forms.Form):
	new_password=forms.CharField(max_length=50,required=True)
