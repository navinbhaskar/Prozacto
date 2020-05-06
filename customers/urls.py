from django.urls import path

from django.contrib.auth import views as auth_views

from . import views



urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="customers/password_reset.html"), name="reset_password"),
    path('logout/', views.logoutUser, name="logout"),
    path('get_doctors/<str:clinic_id>/', views.get_doctors, name="get_doctors"),
    path('view_records/', views.view_records, name="view_records"),
    path('request_appointment/<str:doc_id>/', views.request_appointment, name="request_appointment"),
    path('show_record_list/<str:doc_id>/', views.show_record_list, name="show_record_list"),
    path('upload_record/', views.upload_record, name="upload_record"),
    path('share_record/<str:doc_id>/<str:record_id>/', views.share_record, name="share_record"),
    path('view_appointments/', views.view_appointments, name="view_appointments"),
]

'''
1 - Submit email form                         //PasswordResetView.as_view()
2 - Email sent success message                //PasswordResetDoneView.as_view()
3 - Link to password Rest form in email       //PasswordResetConfirmView.as_view()
4 - Password successfully changed message     //PasswordResetCompleteView.as_view()
'''
