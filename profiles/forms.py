from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile


class RegisterUserForm(UserCreationForm):
	email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
	class Meta:
		model = User
		fields = ('username','email','password1','password2')

	def __init__(self,*args,**kwargs):
		super(RegisterUserForm,self).__init__(*args,**kwargs)
		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['class'] = 'form-control'


class CreateProfileForm(forms.ModelForm):
	class Meta: 
		model = Profile
		fields = [
			'phone',
			'carrier',
			'location_name',
			'lat',
			'lon',
		]

class EditUserForm(forms.ModelForm):
	# username = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control'}))
	# email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))
	class Meta:
		model = User
		fields = ['username','email']

class EditProfileForm(forms.ModelForm):
	# carrier_options = {
	# 	"att": "AT&T",
	# 	"verizon": "Verizon",
	# 	"sprint": "Sprint",
	# 	"tmobile": "T-Mobile",
	# 	"boostmobile": "Boost Mobile"
	# }
	# carrier = forms.CharField(label='Phone Carrier:', widget=forms.Select(choices=carrier_options))
	class Meta:
		model = Profile 
		fields = [
			'phone',
			'carrier',
			'location_name',
			'lat',
			'lon',
		]
