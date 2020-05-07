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
from .decorators import unauthenticated_user, allowed_users

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
@allowed_users(allowed_roles=['patient', 'doctor', 'assistant'])
def home(request):
    if(hasattr(request.user, 'patient')):
        name = request.user.patient.name
        phone = request.user.patient.phone
        email = request.user.patient.email

        total_appointments = request.user.patient.appointment_set.all()

        approved = total_appointments.filter(status='Approved').count()
        pending = total_appointments.filter(status='Pending').count()

        clinic = Clinic.objects.all();
        context = {'clinics':clinic, 'name': name, 'phone': phone, 'email': email, 'approved': approved, 'pending': pending, 'greeting': name, 'appointments': total_appointments }
        return render(request, 'customers/user.html', context)
    elif(hasattr(request.user, 'doctor')):
        appointments = request.user.doctor.appointment_set.all()
        medical_record = Medical_Records.objects.filter(shared_with__id=request.user.doctor.id)
        context = {'medical_record_list': medical_record, 'appointments': appointments, 'greeting': request.user.doctor.name }
        return render(request, 'customers/doctor_dashboard.html', context)
    elif(hasattr(request.user, 'assistant')):
        clinic_name = request.user.assistant.clinic
        doctors_list = Doctor.objects.filter(clinic=clinic_name)
        appointments = Appointment.objects.filter(doctor__in=doctors_list)
        context = {'doctors': doctors_list, 'clinic': clinic_name, 'appointments': appointments, 'greeting': request.user.assistant.name }
        return render(request, 'customers/assistant_dashboard.html', context)
    else:
        return HttpResponse("You are not authorized to view this page!")

@login_required(login_url='login')
@allowed_users(allowed_roles=['patient'])
def get_doctors(request, clinic_id):
    doctors_list = Doctor.objects.filter(clinic__id=clinic_id)
    my_records = request.user.patient.medical_records_set.all()
    context = {'doctors': doctors_list, 'records': my_records, "greeting": request.user.patient.name }
    return render(request, 'customers/doctors_list.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['patient'])
def view_records(request):
    my_records = request.user.patient.medical_records_set.all()
    context = {'records': my_records, "greeting": request.user.patient.name }
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
    context = {'records': my_records, 'doc': doc, "greeting": request.user.patient.name }
    return render(request, 'customers/share_records.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['patient'])
def share_record(request, doc_id, record_id):
    doc = Doctor.objects.get(id=doc_id)
    Medical_Record= Medical_Records.objects.get(id=record_id)
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
@allowed_users(allowed_roles=['doctor'])
def view_appointments(request):
    appointments = request.user.doctor.appointment_set.all()
    medical_record = Medical_Records.objects.filter(shared_with__id=request.user.doctor.id)
    context = {'medical_record_list': medical_record, 'appointments': appointments }
    return render(request, 'customers/appointments.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['doctor'])
def get_report(request, patient_id):
    medical_record = Medical_Records.objects.filter(patient__id=patient_id, shared_with__id=request.user.doctor.id)
    name = Patient.objects.get(id=patient_id).name
    context = {'medical_record_list': medical_record, "name": name, 'greeting': request.user.doctor.name }
    return render(request, 'customers/patient_record.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['doctor'])
def shared_report(request):
    medical_record = Medical_Records.objects.filter(shared_with__id=request.user.doctor.id)
    context = {'medical_record_list': medical_record}
    return render(request, 'customers/patient_record.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['assistant'])
def confirm_appointment(request, appointment_id):
    Appointment.objects.filter(id=appointment_id).update(status='Approved')
    return redirect('home')

@login_required(login_url='login')
@allowed_users(allowed_roles=['assistant'])
def change_appointment_timing(request, appointment_id):
    timing = request.POST.get('timing')
    if(timing):
        Appointment.objects.filter(id=appointment_id).update(timing=timing)
        return redirect('home')
    return render(request, "customers/change_time.html")


@login_required(login_url='login')
@allowed_users(allowed_roles=['patient'])
def shared_with(request):
    all_shares=[]
    for record in Medical_Records.objects.filter(patient=request.user.patient).prefetch_related('shared_with'):
        for doc in record.shared_with.all():
            data={
                "doctor": doc.name,
                "doctor_id": doc.id,
                "document_title": record.title,
                "document": record.document,
                "document_id": record.id
            }
            all_shares.append(data)
    context = {"data": all_shares, "greeting": request.user.patient.name}
    return render(request, 'customers/shared_with.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['patient'])
def revoke_access(request, document_id, doctor_id):
    doc = Doctor.objects.get(id=doctor_id)
    Medical_Record= Medical_Records.objects.get(id=document_id)
    Medical_Record.shared_with.remove(doc)
    return redirect('shared_with')

def download(request, document_id):
    object_name= Medical_Records.objects.get(id=document_id)
    filename = object_name.document.name.split('/')[-1]
    response = HttpResponse(object_name.document, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response