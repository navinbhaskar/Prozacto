from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)
	profile_pic = models.ImageField(default="profile1.png", null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.name

class Clinic(models.Model):
    name = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=400, null=True)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    clinic = models.ForeignKey(Clinic, null=True, on_delete= models.SET_NULL)
    profile_pic = models.ImageField(default="profile1.png", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class Assistant(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    clinic = models.ForeignKey(Clinic, null=True, on_delete= models.SET_NULL)
    profile_pic = models.ImageField(default="profile1.png", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class Appointment(models.Model):
    STATUS = (
			('Pending', 'Pending'),
			('Declined', 'Declined'),
			('Approved', 'Approved'),
			)

    patient = models.ForeignKey(Patient, null=True, on_delete= models.SET_NULL)
    doctor = models.ForeignKey(Doctor, null=True, on_delete= models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)

    def __str__(self):
	       return self.patient.name + " - " + self.doctor.name

class Medical_Records(models.Model):
    title = models.CharField(max_length=200, null=True)
    document = models.FileField(default="document.zip", null=True, blank=True)
    patient = models.ForeignKey(Patient, null=True, on_delete= models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    shared_with = models.ManyToManyField(Doctor,  blank=True)

    #def __str__(self):
    #    return self.title + " " + self.patient.name
