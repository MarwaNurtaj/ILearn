from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.


class Students(models.Model):
	user = models.OneToOneField(User, null=True,blank=True, on_delete=models.CASCADE)
	name  =models.CharField(max_length=200, null=True)
	age   =models.CharField(max_length=200, null=True)
	email =models.CharField(max_length=200, null=True)
	phone =models.CharField(max_length=200, null=True)
	profile_pic = models.ImageField(default="student_pro_pic.jpg",null=True, blank=True)
	date_created =models.DateTimeField(auto_now_add=True, null=True)
	def __str__(self):
		return self.name



class TypeCast(models.Model):
	name  =models.CharField(max_length=200, null=True)
	def __str__(self):
		return self.name



class Courses(models.Model):
	CATAGORY =	(
					('CSE','CSE'),
					('EEE','EEE'),
					('English','English'),
					('Math','Math'),
				)
	name  =models.CharField(max_length=200, null=True)
	catagory=models.CharField(max_length=200, null=True,choices=CATAGORY)
	description =models.CharField(max_length=200, null=True,blank=True)
	price =models.CharField(max_length=200, null=True)
	link = models.CharField(max_length=500, null=True)
	date_created =models.DateTimeField(auto_now_add=True, null=True)
	typecast= models.ManyToManyField(TypeCast)

	def __str__(self):
		return self.name





class Order(models.Model):
	STATUS =(
				('Pending','Pending'),
				('Not Available','Not Available'),
				('Deliverd','Deliverd'),
			)
	Students=models.ForeignKey(Students, null=True,on_delete=models.SET_NULL)
	Courses=models.ForeignKey(Courses, null=True,on_delete=models.SET_NULL)
	date_created =models.DateTimeField(auto_now_add=True, null=True)
	status  =models.CharField(max_length=200, null=True,choices=STATUS)
	note =models.CharField(max_length=1000, null=True)


	def __str__(self):
		return self.Courses.name

		
class Room(models.Model):
    name = models.CharField(max_length=1000)

class Massage(models.Model):
    value = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.CharField(max_length=1000000)
    room = models.CharField(max_length=1000000)