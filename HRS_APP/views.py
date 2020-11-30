from django.http import HttpResponse
from django.shortcuts import render,redirect
import cx_Oracle

import HelperClass.Encrypt_Decrypt_Pass as ED_Operation



# login
user_info = {}  # holds user data across pages


# Create your views here.
def login(request):
    return render(request, "auth/LogInOrSignUp.html")

def signup(request):
    return render(request, "auth/SignUp.html")
def demo(request):
    return render(request, "demo.html")


# homepage URLs
def admin_home(request):
    #return render(request, "homepage/DoctorHome.html", {'name': user_info['f_name'] + ' ' + user_info['l_name']})
    return HttpResponse("add admin_home")


def customer_home(request):
    #return render(request, "homepage/UserHome.html", {'name': user_info['f_name'] + ' ' + user_info['l_name']})
    return HttpResponse("add customer_home")


 # log in

def submit(request):
    username = request.POST['username']
    password = request.POST['pass']
    usertype = request.POST['usertype']
    
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='xe')
    conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)

    c = conn.cursor()

    # TODO: connect database and verify
    if usertype == "admin":
        statement = "SELECT ADMIN_ID,PASSWORD,FIRST_NAME, LAST_NAME from HRS_OURDATABASE.ADMIN WHERE USERNAME=" + "\'" + username + "\'"
        c.execute(statement)
        if c:
            x = c.fetchone()
            return_id = x[0]
            return_password = x[1]
            return_f_name = x[2]
            return_l_name = x[3]

            user_info['pk'] = return_id
            user_info['f_name'] = return_f_name
            user_info['l_name'] = return_l_name
            #user_info['email'] = email
            user_info['usertype'] = usertype
            decoded_password=ED_Operation.Encrypt_Decrypt_Passwords(return_password).decryptPassword()
           
            if decoded_password == password:
                return HttpResponse("Need to add admin_homepage")
            else:
                return HttpResponse("Wrong Pass")
        else:
            return HttpResponse("Database Error or You don't exist")

    elif usertype == "customer":
        statement = "SELECT CUSTOMER_ID, PASSWORD, FIRST_NAME, LAST_NAME from HRS_OURDATABASE.CUSTOMER WHERE USERNAME=" + "\'" + username + "\'"

        c.execute(statement)
        if c:
            x = c.fetchone()
            return_id = x[0]
            return_password = x[1]
            return_f_name = x[2]
            return_l_name = x[3]

            #user_info['pk'] = return_id
            user_info['f_name'] = return_f_name
            user_info['l_name'] = return_l_name
            #user_info['email'] = email
            user_info['usertype'] = "customer"

            decoded_password=ED_Operation.Encrypt_Decrypt_Passwords(return_password).decryptPassword()

            if decoded_password == password:
                return HttpResponse("Need to add customer_homepage")
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
    #phone = request.POST['phone']
    
    city =request.POST['city']
    country=request.POST['country']
    username=request.POST.get('username',False)

    encoded_password = request.POST['pass']

    confirm_in = request.POST['cpass']

    #encoded_password=ED_Operation.Encrypt_Decrypt_Passwords(input_password).encryptPassword()
    if usertype == 'admin':
        dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='xe')
        conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
        c = conn.cursor()
        c2 = conn.cursor()
        # Check here 
        statement = "INSERT INTO HRS_OURDATABASE.ADMIN(FIRST_NAME, LAST_NAME, GMAIL,CITY,COUNTRY,USERNAME,PASSWORD) VALUES (" + "\'" + firstname + \
                    "\', " + "\'" + lastname + "\'," + "\'" + email + "\', " + "\'" +city + "\', " + "\'" + country + "\'," + "\'" + username + "\', " + "\'" +encoded_password+ "\'" + ")"
        
        c.execute(statement)
        conn.commit()
        statement = "SELECT ADMIN_ID, FIRST_NAME, LAST_NAME from HRS_OURDATABASE.ADMIN WHERE USERNAME=" + "\'" + username+ "\'"
        c2.execute(statement)
       
        if c2:
            x = c2.fetchone()
            return_id = x[0]
            return_f_name = x[1]
            return_l_name = x[2]

            user_info['pk'] = return_id
            user_info['f_name'] = return_f_name
            user_info['l_name'] = return_l_name
            #user_info['email'] = email
            user_info['type'] = "admin"
            #return redirect("doctor_home")
            
            #return HttpResponse("Go to adminhome or login page")
        #else:
            #return HttpResponse("Error")
    elif usertype == 'customer':
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='xe')
        conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
        c = conn.cursor()
        statement = "INSERT INTO HRS_OURDATABASE.CUSTOMER(FIRST_NAME, LAST_NAME, GMAIL, CITY,COUNTRY,USERNAME,PASSWORD) VALUES (" + "\'" + firstname + \
                    "\', " + "\'" + lastname + "\'," + "\'" + email + "\', " + "\'" + city + "\', " + "\'" +country+ "\'," + "\'" + username + "\', " + "\'" +encoded_password+ "\'" + ")"
        c.execute(statement)
        conn.commit()

        c2 = conn.cursor()

        statement = "SELECT CUSTOMER_ID, FIRST_NAME, LAST_NAME from HRS_OUTDATABASE WHERE USERNAME=" + "\'" + username + "\'"

        c2.execute(statement)
        if c2:
            x = c2.fetchone()
            return_id = x[0]
            return_f_name = x[1]
            return_l_name = x[2]

            user_info['pk'] = return_id
            user_info['f_name'] = return_f_name
            user_info['l_name'] = return_l_name
            #user_info['email'] = email
            user_info['type'] = "customer"

            #return redirect("user_home")
            #return HttpResponse("Go to customer login page")
        #else:
           #return HttpResponse("Error")
    return HttpResponse("complete registration")
        





    
   

       
        
    
        
        
