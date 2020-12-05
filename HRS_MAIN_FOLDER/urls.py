"""HRS_MAIN_FOLDER URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from HRS_APP import views as HRS_APP_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('submit',HRS_APP_views.submit, name='submit'),
    path('signup',HRS_APP_views.signup, name='signup'),
    path('signupSubmit',HRS_APP_views.signupSubmit, name='submit'),
    #path('RoomListView', HRS_APP_views.RoomListView, name='RoomListView'),
   ## path('admin/see_admin_details/', HRS_APP_views.see_admin_details, name='see_admin_details'),

   #path('admin/edit_profile_details/', HRS_APP_views.admin_edit_profile, name='admin_edit_profile'),

    path('', HRS_APP_views.login, name='login'),
    path('admin/logout', HRS_APP_views.logout, name='log_out'),

    # ADMIN Page Part
    path('HOME', HRS_APP_views.admin_home, name='admin_home'),
    path('admin_profile_details', HRS_APP_views.admin_profile_details, name='admin_profile_details'),
    path('admin_change_password', HRS_APP_views.admin_change_password, name='admin_change_password'),
    path('update_your_password', HRS_APP_views.update_your_password, name='update_your_password'),
    path('logout', HRS_APP_views.logout, name='logout'),
    path('update_admin_profile', HRS_APP_views.update_admin_profile, name='update_admin_profile'),

















    #Customer Page Part
    path('customer_profile',HRS_APP_views.customer_profile_details, name='profile'),

   

]
