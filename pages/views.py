from django.shortcuts import render
from django.http import HttpResponse


def home_view(request, *args, **kwargs):
	context = {
		"title": "Sky Eye Home"
	}
	return render(request,"index.html",context)

def about_view(request, *args, **kwargs):
	context = {
		"title": "Sky Eye About"
	}
	return render(request,"about.html",context)

def contact_view(request, *args, **kwargs):
	context = {
		"title": "Sky Eye Contact"
	}
	return render(request,"contact.html",context)

def agreement_view(request, *args, **kwargs):
	context = {
		"title": "Sky Eye User Agreement"
	}
	return render(request,"agreement.html",context)
