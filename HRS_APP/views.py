from django.http import HttpResponse
from django.shortcuts import render,redirect
import cx_Oracle

import HelperClass.Encrypt_Decrypt_Pass as ED_Operation

from .models import Room


#EDIT
# login
user_info = {}  # holds user data across pages
customer_info_list =[]
admin_info_list =[]



# Create your views here.
def login(request):
    return render(request, "auth/LogInOrSignUp.html")

def signup(request):
    return render(request, "auth/SignUp.html")
def demo(request):
    return render(request, "demo.html")


# homepage URLs
def admin_home(request):
    return render(request, "Homepage/AdminHomePage.html", {'name': user_info['f_name'] + ' ' + user_info['l_name']})
    

def customer_home(request):
    return render(request, "Homepage/CustomerHomePage.html", {'name': user_info['f_name'] + ' ' + user_info['l_name']})
    


 # log in

def submit(request):
    username = request.POST['username']
    password = request.POST['pass']
    usertype = request.POST['usertype']
   
    
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)

    c = conn.cursor()

    # TODO: connect database and verify
    if usertype == "admin":
        statement = "SELECT ADMIN_ID,PASSWORD,FIRST_NAME, LAST_NAME,GMAIL,CITY,COUNTRY from HRS_OURDATABASE.ADMIN WHERE USERNAME=" + "\'" + username + "\'"
        c.execute(statement)
        if c:
            x = c.fetchone()
            admin_id = x[0]
            return_password = x[1]
            admin_f_name = x[2]
            admin_l_name = x[3]
            admin_gmail=x[4]
            admin_city=x[5]
            admin_country=x[6]
            admin_username=username


            user_info['pk'] = admin_id
            user_info['f_name'] = admin_f_name
            user_info['l_name'] = admin_l_name
            user_info['gmail'] = admin_gmail
            user_info['city'] = admin_city
            user_info['country'] = admin_country
            user_info['username'] = admin_gmail
            


      
          
            decoded_password=ED_Operation.Encrypt_Decrypt_Passwords(return_password).decryptPassword()
            admin_password=decoded_password
            user_info['admin_password'] = admin_password
           
            if decoded_password == password:
                row={'admin_id':admin_id,'admin_f_name':admin_f_name,'admin_l_name':admin_l_name,'admin_gmail':admin_gmail,'admin_city':admin_city,'admin_country':admin_country,'admin_username':admin_username,'admin_password':admin_password}
                
                admin_info_list.append(row)
                return render(request, "Homepage/AdminHomePage.html",{'name': user_info['f_name'] + ' ' + user_info['l_name']})
                
            else:
                return HttpResponse("Wrong Pass")
        else:
            return HttpResponse("Database Error or You don't exist")

    elif usertype == "customer":
        statement = "SELECT CUSTOMER_ID, PASSWORD, FIRST_NAME, LAST_NAME,GMAIL,CITY,COUNTRY from HRS_OURDATABASE.CUSTOMER WHERE USERNAME=" + "\'" + username + "\'"
       
        c.execute(statement)
        if c:
            x = c.fetchone()
            
            customer_id = x[0]
            return_password = x[1]
            customer_f_name = x[2]
            customer_l_name = x[3]
            customer_gmail=x[4]
            customer_city=x[5]
            customer_country=x[6]
            customer_username=username
            user_info['pk'] = customer_id 
            user_info['f_name'] = customer_f_name
            user_info['l_name'] = customer_l_name
            user_info['gmail'] = customer_gmail
            user_info['city'] = customer_city
            user_info['country'] = customer_country
            user_info['username'] =customer_gmail

            decoded_password=ED_Operation.Encrypt_Decrypt_Passwords(return_password).decryptPassword()
            customer_password=decoded_password
            user_info['customer_password'] = customer_password

            if decoded_password == password:
                #row={'customer_id':customer_id,'customer_f_name':customer_f_name,'customer_l_name':customer_l_name,'customer_gmail':customer_gmail,'customer_city':customer_city,'customer_country':customer_country,'customer_username':customer_username,'customer_password':customer_password}
                #customer_info_list.append(row)
                return render(request, "Homepage/CustomerHomePage.html",{'name': user_info['f_name'] + ' ' + user_info['l_name']})
                
            else:
                return HttpResponse("Wrong Pass")
        else:
            return HttpResponse("Database Error or You don't exist")
    return render(request, "auth/LogInOrSignUp.html")


#SignUpSubmit

def signupSubmit(request):
    usertype = request.POST['User']
    firstname = request.POST['fname']
    lastname = request.POST['lname']
    email = request.POST['email']
    
   
    
    city =request.POST['city']
    country=request.POST['country']
    username=request.POST['username']

    input_password = request.POST['pass']

    confirm_in = request.POST['cpass']
    if input_password != confirm_in:
        return HttpResponse("password and confirm password does not match!")

    encoded_password=ED_Operation.Encrypt_Decrypt_Passwords(input_password).encryptPassword()
    if usertype == 'admin':
        dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
        conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
        c = conn.cursor()
        
        
        
        
        statement = "INSERT INTO HRS_OURDATABASE.ADMIN(FIRST_NAME, LAST_NAME, GMAIL,CITY,COUNTRY,USERNAME,PASSWORD) VALUES (" + "\'" + firstname + \
                    "\', " + "\'" + lastname + "\'," + "\'" + email + "\', " + "\'" +city + "\', " + "\'" + country + "\'," + "\'" + username + "\', " + "\'" +encoded_password+ "\'" + ")"
        
        c.execute(statement)
        conn.commit()

    elif usertype == 'customer':
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
        c = conn.cursor()
        statement = "INSERT INTO HRS_OURDATABASE.CUSTOMER(FIRST_NAME, LAST_NAME, GMAIL, CITY,COUNTRY,USERNAME,PASSWORD) VALUES (" + "\'" + firstname + \
                    "\', " + "\'" + lastname + "\'," + "\'" + email + "\', " + "\'" + city + "\', " + "\'" +country+ "\'," + "\'" + username + "\', " + "\'" +encoded_password+ "\'" + ")"
        c.execute(statement)
        conn.commit()
        
    return redirect("login")
#CustomerHome 
def customer_profile_details(request):
    return render(request,"Customer/profile_page.html",{'customer_all_info':customer_info_list})

    

def logout(request):
    user_info.clear()
    return redirect("login")



def see_admin_details(request):
    admin_id = request.POST['admin_id']
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
    c = conn.cursor()

    c.execute(
        "SELECT ADMIN_ID,PASSWORD,FIRST_NAME, LAST_NAME,GMAIL,CITY,COUNTRY from HRS_OURDATABASE.ADMIN WHERE ADMIN_ID=" + str(admin_id))



    admin_id =""
    return_password =""
    admin_f_name =""
    admin_l_name =""
    admin_gmail =""
    admin_city =""
    admin_country =""
    admin_username = ""

    for row in c:
        admin_id = x[0]
        return_password = x[1]
        admin_f_name = x[2]
        admin_l_name = x[3]
        admin_gmail = x[4]
        admin_city = x[5]
        admin_country = x[6]
        admin_username = username

    return render(request, "auth/admin_details.html",
                  {'firstname': admin_f_name,
                   'lastname' : admin_l_name,
                   'phone': phone,
                   'location': admin_city,
                   'email': admin_gmail,
                   'country':admin_country,
                   'adminusername': admin_username
                   })


def RoomListView(request):
    room = Room.objects.all()[0]
    room_categories = dict(room.ROOM_AVAILABILITY)
    room_values = room_categories.values()
    room_list = []

    for room_category in room_categories:
        room = room_categories.get(room_category)
        room_url = reverse('hotel:RoomDetailView', kwargs={
                           'category': room_category})

        room_list.append((room, room_url))
    context = {
        "room_list": room_list,
    }
    return render(request, 'room_list_view.html', context)



###admin home


def customer_profile_details(request):
    return render(request,"Customer/profile_page.html",{'customer_all_info':customer_info_list})

    return render(request,"Customer/profile_page.html",{'first_name':user_info['f_name'],'last_name':user_info['l_name'],'gmail':user_info['gmail'],'username':user_info['username']})

def update_customer_profile(request):
    fname=request.POST['fname']
    lname=request.POST['lname']
    gmail=request.POST['gmail']
    username=request.POST['username']
    if fname != user_info['f_name']:
        user_info['f_name']=fname


        dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
        conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
        c = conn.cursor()

        statement = "UPDATE HRS_OURDATABASE.CUSTOMER SET FIRST_NAME = " + "\'" + fname + "\'" + "WHERE CUSTOMER_ID = " + str(
            user_info['pk'])

        c.execute(statement)
        conn.commit()
    if lname != user_info['l_name']:

        user_info['l_name']=lname


        dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
        conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
        c = conn.cursor()

        statement = "UPDATE HRS_OURDATABASE.CUSTOMER SET LAST_NAME = " + "\'" + lname + "\'" + "WHERE CUSTOMER_ID = " + str(
            user_info['pk'])

        c.execute(statement)
        conn.commit()
    if gmail != user_info['gmail']:

        user_info['gmail']=gmail


        dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
        conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
        c = conn.cursor()

        statement = "UPDATE HRS_OURDATABASE.CUSTOMER SET GMAIL = " + "\'" + gmail + "\'" + "WHERE CUSTOMER_ID = " + str(
            user_info['pk'])

        c.execute(statement)
        conn.commit()

    if username != user_info['username']:

        user_info['username']=username


        dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
        conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
        c = conn.cursor()

        statement = "UPDATE HRS_OURDATABASE.CUSTOMER SET USERNAME = " + "\'" + username + "\'" + "WHERE CUSTOMER_ID = " + str(
            user_info['pk'])

        c.execute(statement)
        conn.commit()

    return redirect("profile")

def customer_change_password(request):
    return render(request,"Customer/CustomerChangePassword.html",{'customer_password_from_database':user_info['customer_password']})
def update_your_password(request):
    current_password=request.POST['current_password']
    new_password=request.POST['new_password']
    confirm_password=request.POST['confirm_password']
    if current_password==user_info['customer_password']:
        if new_password==confirm_password:
            new_encoded_password=ED_Operation.Encrypt_Decrypt_Passwords(confirm_password).encryptPassword()

            dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
            conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
            c = conn.cursor()

            statement = "UPDATE HRS_OURDATABASE.CUSTOMER SET PASSWORD = " + "\'" + new_encoded_password + "\'" + "WHERE CUSTOMER_ID = " + str(
                user_info['pk'])

            c.execute(statement)
            conn.commit()
            return render(request, "Homepage/CustomerHomePage.html",{'name': user_info['f_name'] + ' ' + user_info['l_name']})
        else:
            return HttpResponse("Give similiar Password with new password")
    else:
        return HttpResponse("Provide correct password of previous")


def logout(request):
    user_info.clear()
    return redirect("login")


