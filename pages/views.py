from django.shortcuts import render
from django.http import HttpResponse


def home_view(request, *args, **kwargs):
	context = {
		"title": "Sky Eye Home"
	}
	return render(request,"index.html",context)

