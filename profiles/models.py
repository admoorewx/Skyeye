from django.db import models
from django.urls import reverse

# Create your models here.
class Profile(models.Model):
	user_id  = models.IntegerField("Profile Owner",blank=False, default=1)
	phone    = models.IntegerField(blank=False)
	location_name = models.CharField(max_length=120)
	carrier  = models.CharField(blank=False,max_length=15,default="att")
	lat      = models.FloatField(null=True,blank=False,default=40.0)
	lon      = models.FloatField(null=True,blank=False,default=-98.0)

	def get_absolute_url(self):
		return reverse("profile",kwargs={"id":self.id})

	def __str__(self):
		text = f'User ID: {self.user_id}\nPhone: {self.phone}\nLocation Name: {self.location_name}\nLat, Lon: {self.lat}, {self.lon}'
		return text