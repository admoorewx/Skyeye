from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile 
from .forms import RegisterUserForm, CreateProfileForm, EditUserForm, EditProfileForm
# Create your views here.

def profile_view(request, *args, **kwargs):
	profile = Profile.objects.get(id=1)
	context = {
		'profile': profile
	}
	return render(request,"profile/profile.html",context)

def login_user(request,*args,**kwargs):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request,user)
			return redirect('home')
		else: 
			messages.success(request,"Invalid username and/or password.")
			return redirect('login')
	else: 
		return render(request,"authenticate/login.html",{})


def logout_user(request, *args, **kwargs):
	logout(request)
	messages.success(request,"You have been logged out.")
	return redirect('home')

def register_user(request,*args,**kwargs):
	if request.method == "POST":
		form = RegisterUserForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(request, username=username, password=password)
			login(request,user)
			return redirect('create_profile')
		else: 
			messages.success(request,"There was an error during registration.")
			return redirect('register_user')
	else: 
		form = RegisterUserForm()
	context = {
		'form': form,
	}
	return render(request,"authenticate/register_user.html",context)

def create_profile(request,*args,**kwargs):
	if request.method == "POST":
		form = CreateProfileForm(request.POST)
		if form.is_valid():
			profile = form.save(commit=False)
			profile.user_id = request.user.id
			profile.save()
			messages.success(request,"Profile creation successful! You will now receive Sky Eye alerts.")
			return redirect('home')
		else: 
			messages.success(request,"There was an error during profile creation.")
			return redirect('create_profile')
	else: 
		form = CreateProfileForm()
	context = {
		'form': form,
	}
	return render(request,"profiles/create_profile.html",context)

def edit_profile(request,*args,**kwargs):
	profile = Profile.objects.get(user_id=request.user.id)
	initial_dict1 = {
		'username': request.user, 
		'email': request.user.email
	}
	initial_dict2 = {
		'phone': profile.phone,
		'carrier': profile.carrier,
		'location_name': profile.location_name,
		'lat': profile.lat,
		'lon': profile.lon,
	}
	if request.method == "POST":
		form1 = EditUserForm(request.POST,initial=initial_dict1)
		form2 = EditProfileForm(request.POST,initial=initial_dict2)
		# Handle form1/User form manually
		user = User.objects.get(username=request.user)
		newusername = form1.data['username']
		if user.username != newusername:  
			# Check to make sure the new username does not already exist.
			if User.objects.filter(username=newusername).exists():
				messages.success(request,"Sorry, this username has already been taken!")
				return redirect('edit_profile')
			else: 
				user.username = newusername
				user.save()
		if form1.data['email'] != user.email:
			user.email = form1.data['email']
			user.save()
		profile = Profile.objects.get(user_id=request.user.id)
		if form2.data['phone'] != profile.phone:
			profile.phone = int(form2.data['phone'])
		if form2.data['location_name'] != profile.location_name:
			profile.location_name = form2.data['location_name']
		if form2.data['carrier'] != profile.carrier: 
			profile.carrier = form2.data['carrier']
		print(form1.data)
		print(form2.data)
		if form2.data['lat'] != profile.lat or form2.data['lon'] != profile.lon:
			profile.lat = float(form2.data['lat'])
			profile.lon = float(form2.data['lon'])
		messages.success(request,"Profile update successful!")
		profile.save()
		return redirect('view_profile')
		# except: 
		# 	messages.success(request,"An error occurred while updating your profile. Ensure that all fields are filled correctly.")
		# 	return redirect('edit_profile')
	else: 
		form1 = EditUserForm(initial=initial_dict1)
		form2 = EditProfileForm(initial=initial_dict2)
	context = {
		'form1': form1,
		'form2': form2,
		'profile': profile,
	}
	return render(request,"profiles/edit_profile.html",context)


def view_profile(request,*args,**kwargs):
	user_id = request.user.id
	profile = Profile.objects.get(user_id=user_id)
	context = {
		'profile': profile,
		'user': request.user,
	}
	return render(request, "profiles/view_profile.html",context)

