from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .models import *
from .forms import *
#from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users#, admin_only

# Create your views here.
@unauthenticated_user
def registerPage(request):

    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='patient')
            user.groups.add(group)

            Patient.objects.create(
				user=user,
				name=user.username,
				)

            messages.success(request, 'Account was created for ' + username)

            return redirect('login')


    context = {'form':form}
    return render(request, 'customers/register.html', context)

@unauthenticated_user
def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'customers/login.html', context)


def logoutUser(request):
	logout(request)
	return redirect('login')


@login_required(login_url='login')
@allowed_users(allowed_roles=['patient'])
def home(request):
    #orders = request.user.doctor.appointment_set.all()
    #return HttpResponse(orders.count())
    name = request.user.patient.name
    phone = request.user.patient.phone
    email = request.user.patient.email

    total_appointments = request.user.patient.appointment_set.all()

    approved = total_appointments.filter(status='Approved').count()
    pending = total_appointments.filter(status='Pending').count()

    clinic = Clinic.objects.all();
    context = {'clinics':clinic, 'name': name, 'phone': phone, 'email': email, 'approved': approved, 'pending': pending }
    return render(request, 'customers/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['patient'])
def get_doctors(request, clinic_id):
    doctors_list = Doctor.objects.filter(clinic__id=clinic_id)
    my_records = request.user.patient.medical_records_set.all()
    context = {'doctors': doctors_list, 'records': my_records }
    return render(request, 'customers/doctors_list.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['patient'])
def view_records(request):
    my_records = request.user.patient.medical_records_set.all()
    context = {'records': my_records }
    return render(request, 'customers/my_records.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['patient'])
def request_appointment(request, doc_id):
    doc = Doctor.objects.get(id=doc_id)
    appointment_obj = Appointment(patient=request.user.patient, doctor=doc, status='Pending')
    appointment_obj.save()
    return redirect('home')


@login_required(login_url='login')
@allowed_users(allowed_roles=['patient'])
def show_record_list(request, doc_id):
    my_records = request.user.patient.medical_records_set.all()
    doc = Doctor.objects.get(id=doc_id)
    context = {'records': my_records, 'doc': doc }
    return render(request, 'customers/share_records.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['patient'])
def share_record(request, doc_id, record_id):
    doc = Doctor.objects.get(id=doc_id)
    print(doc)
    print(record_id)
    Medical_Record= Medical_Records.objects.get(id=record_id)
    print(Medical_Record)
    Medical_Record.shared_with.add(doc)
    return redirect('home')


@login_required(login_url='login')
@allowed_users(allowed_roles=['patient'])
def upload_record(request):
    patient = request.user.patient
    form = MedicalRecordsForm()

    if request.method == 'POST':
        form = MedicalRecordsForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.patient = patient
            task.save()
            return redirect('home')

    context = {'form':form}
    return render(request, 'customers/upload_record.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['doctor', 'assistant'])
def view_appointments(request):
    appointments = request.user.doctor.appointment_set.all()
    print(appointments)
    return HttpResponse("Yaay")
