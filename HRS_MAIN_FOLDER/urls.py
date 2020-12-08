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
    path('',HRS_APP_views.login, name='login'),

    path('submit',HRS_APP_views.submit, name='submit'),
    path('signup',HRS_APP_views.signup, name='signup'),
    path('signupSubmit',HRS_APP_views.signupSubmit, name='submit'),

   
    


    #Customer Page Part
    path('customer_home', HRS_APP_views.customer_home, name='customer_home'),

    path('customer_profile',HRS_APP_views.customer_profile_details, name='profile'),
    path('booking_details',HRS_APP_views.my_booking_status, name='my_booking_status'),
    path('customer_change_password',HRS_APP_views.customer_change_password, name='customer_change_password'),
    path('update_your_password',HRS_APP_views.update_your_password, name='update_your_password'),
    path('logout',HRS_APP_views.logout, name='logout'),
    path('update_customer_profile',HRS_APP_views.update_customer_profile, name='update_customer_profile'),

    #New Booking Part
    path('single_room',HRS_APP_views.single_room, name='single_room'),
    path('double_room',HRS_APP_views.double_room, name='double_room'),
    path('triple_room',HRS_APP_views.triple_room, name='triple_room'),
    path('quad_room',HRS_APP_views.quad_room, name='quad_room'),

    path('book',HRS_APP_views.book, name='book'),
    path('confirm_book',HRS_APP_views.confirm_book, name='confirm_book'),
    path('view_details',HRS_APP_views.view_details, name='view_details'),
    path('invoice',HRS_APP_views.invoice, name='invoice'),
    path('contact_submit',HRS_APP_views.contact_submit, name='contact_submit'),





    #Admin part URL
    # ADMIN Page Part
    path('admin_home', HRS_APP_views.admin_home, name='admin_home'),
    path('admin_profile_details', HRS_APP_views.admin_profile_details, name='admin_profile_details'),
    path('admin_change_password', HRS_APP_views.admin_change_password, name='admin_change_password'),
    path('update_admin_password', HRS_APP_views.update_admin_password, name='update_admin_password'),
    path('logout', HRS_APP_views.logout, name='logout'),
    path('update_admin_profile', HRS_APP_views.update_admin_profile, name='update_admin_profile'),


    #admin part booking control
    path('all_booking', HRS_APP_views.all_booking, name='all_booking'),
    path('approved_booking', HRS_APP_views.approved_booking, name='approved_booking'),
    path('pending_booking', HRS_APP_views.pending_booking, name='pending_booking'),
    path('cancelled_booking', HRS_APP_views.cancelled_booking, name='cancelled_booking'),

    path('booking_modify', HRS_APP_views.booking_modify, name='booking_modify'),
    path('edit_status', HRS_APP_views.edit_status, name='edit_status'),



    #add_room
    path('add_room', HRS_APP_views.add_room, name='add_room'),
    path('complete_add_room', HRS_APP_views.complete_add_room, name='complete_add_room'),

    path('manage_room', HRS_APP_views.manage_room, name='manage_room'),
    path('update_room_info', HRS_APP_views.update_room_info, name='update_room_info'),
    path('complete_update_room_info', HRS_APP_views.complete_update_room_info, name='complete_update_room_info'),


    path('about', HRS_APP_views.about, name='about'),
    path('contact', HRS_APP_views.contact, name='contact'),


    path('search_by_reservation_id', HRS_APP_views.search_by_reservation_id, name='search_by_reservation_id'),
    path('notification', HRS_APP_views.notification, name='notification'),
    

]