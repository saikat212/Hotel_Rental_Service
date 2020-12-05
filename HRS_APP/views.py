from django.http import HttpResponse
from django.shortcuts import render,redirect
import cx_Oracle

import HelperClass.Encrypt_Decrypt_Pass as ED_Operation


# login
user_info = {}  # holds user data across pages
customer_info_list =[]
admin_info_list =[]
customer_info_dict={}



# Create your views here.
def login(request):
    return render(request, "auth/LogInOrSignUp.html")

def signup(request):
    return render(request, "auth/SignUp.html")



# homepage URLs
def admin_home(request):
    return render(request, "Homepage/AdminHomePage.html", {'name': user_info['f_name'] + ' ' + user_info['l_name']})
    

def customer_home(request):
    return render(request, "Homepage/CustomerHomePage.html")
    


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
            user_info['username'] =customer_username

            decoded_password=ED_Operation.Encrypt_Decrypt_Passwords(return_password).decryptPassword()
            customer_password=decoded_password
            user_info['customer_password'] = customer_password

            if decoded_password == password:
                customer_info_dict={'customer_id':customer_id,'customer_f_name':customer_f_name,'customer_l_name':customer_l_name,'customer_gmail':customer_gmail,'customer_city':customer_city,'customer_country':customer_country,'customer_username':customer_username,'customer_password':customer_password}
                customer_info_list.append(customer_info_dict)
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
        dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='xe')
        conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
        c = conn.cursor()
        
        
        
        
        statement = "INSERT INTO HRS_OURDATABASE.ADMIN(FIRST_NAME, LAST_NAME, GMAIL,CITY,COUNTRY,USERNAME,PASSWORD) VALUES (" + "\'" + firstname + \
                    "\', " + "\'" + lastname + "\'," + "\'" + email + "\', " + "\'" +city + "\', " + "\'" + country + "\'," + "\'" + username + "\', " + "\'" +encoded_password+ "\'" + ")"
        
        c.execute(statement)
        conn.commit()

    elif usertype == 'customer':
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='xe')
        conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
        c = conn.cursor()
        statement = "INSERT INTO HRS_OURDATABASE.CUSTOMER(FIRST_NAME, LAST_NAME, GMAIL, CITY,COUNTRY,USERNAME,PASSWORD) VALUES (" + "\'" + firstname + \
                    "\', " + "\'" + lastname + "\'," + "\'" + email + "\', " + "\'" + city + "\', " + "\'" +country+ "\'," + "\'" + username + "\', " + "\'" +encoded_password+ "\'" + ")"
        c.execute(statement)
        conn.commit()
        
    return redirect("login")
#CustomerHome 
def customer_profile_details(request):
    
    return render(request,"Customer/profile_page.html",{'first_name':user_info['f_name'],'last_name':user_info['l_name'],'gmail':user_info['gmail'],'username':user_info['username']})


def my_booking_status(request):
    dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='xe')
    conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
    c = conn.cursor()
    
    
    statement = "SELECT RESERVATION_ID,STATUS FROM HRS_OURDATABASE.RESERVATION WHERE CUSTOMER_ID=" + str(user_info['pk'])
    
    c.execute(statement)
    result = c.fetchall()
    c.close()
    dict_result=[]
    for x in result:
        reservation_id=x[0]
        status=x[1]
        row={'reservation_id':reservation_id,'name':user_info['f_name']+" "+user_info['l_name'],'gmail':user_info['gmail'],'status':status}
        dict_result.append(row)
    return render(request,"Customer/My_Booking_Status.html",{'booking_info':dict_result})




def update_customer_profile(request):
    fname=request.POST['fname']
    lname=request.POST['lname']
    gmail=request.POST['gmail']
    username=request.POST['username']
    if fname != user_info['f_name']:
        user_info['f_name']=fname


        dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='xe')
        conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
        c = conn.cursor()

        statement = "UPDATE HRS_OURDATABASE.CUSTOMER SET FIRST_NAME = " + "\'" + fname + "\'" + "WHERE CUSTOMER_ID = " + str(
            user_info['pk'])

        c.execute(statement)
        conn.commit()
    if lname != user_info['l_name']:

        user_info['l_name']=lname


        dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='xe')
        conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
        c = conn.cursor()

        statement = "UPDATE HRS_OURDATABASE.CUSTOMER SET LAST_NAME = " + "\'" + lname + "\'" + "WHERE CUSTOMER_ID = " + str(
            user_info['pk'])

        c.execute(statement)
        conn.commit()
    if gmail != user_info['gmail']:

        user_info['gmail']=gmail


        dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='xe')
        conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
        c = conn.cursor()

        statement = "UPDATE HRS_OURDATABASE.CUSTOMER SET GMAIL = " + "\'" + gmail + "\'" + "WHERE CUSTOMER_ID = " + str(
            user_info['pk'])

        c.execute(statement)
        conn.commit()
    
    if username != user_info['username']:

        user_info['username']=username


        dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='xe')
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

            dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='xe')
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


#New booking part
def single_room(request):
    dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='xe')
    conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
    c = conn.cursor()
    RoomType = "SINGLE_ROOM"
    
    statement = "SELECT DESCRIPTION,CAPACITY,PRICE,ROOM_AVAILABILITY,IMAGE_CODE from HRS_OURDATABASE.ROOM WHERE ROOM_TYPE=" + "\'" + RoomType+ "\'"
    c.execute(statement)
    result = c.fetchall()
    c.close()
    dict_result=[]
    for x in result:
        description=x[0]
        capacity=x[1]
        price=x[2]
        room_availability=x[3]
        image_code=x[4]
        room_type="SINGLE_ROOM"
        row={'room_type':room_type,'description':description,'capacity':capacity,'price':price,'room_availability':room_availability,'image_code':image_code}

        dict_result.append(row)
    return render(request,"New_Booking/room_details.html",{'room_info':dict_result})

    
def double_room(request):
    dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='xe')
    conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
    c = conn.cursor()
    RoomType = "DOUBLE_ROOM"
    
    statement = "SELECT DESCRIPTION,CAPACITY,PRICE,ROOM_AVAILABILITY,IMAGE_CODE from HRS_OURDATABASE.ROOM WHERE ROOM_TYPE=" + "\'" + RoomType+ "\'"
    c.execute(statement)
    result = c.fetchall()
    c.close()
    dict_result=[]
    for x in result:
        description=x[0]
        capacity=x[1]
        price=x[2]
        room_availability=x[3]
        image_code=x[4]
        room_type="DOUBLE_ROOM"
        row={'room_type':room_type,'description':description,'capacity':capacity,'price':price,'room_availability':room_availability,'image_code':image_code}

        dict_result.append(row)
    return render(request,"New_Booking/room_details.html",{'room_info':dict_result})

def triple_room(request):
    dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='xe')
    conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
    c = conn.cursor()
    RoomType = "TRIPLE_ROOM"
    
    statement = "SELECT DESCRIPTION,CAPACITY,PRICE,ROOM_AVAILABILITY,IMAGE_CODE from HRS_OURDATABASE.ROOM WHERE ROOM_TYPE=" + "\'" + RoomType+ "\'"
    c.execute(statement)
    result = c.fetchall()
    c.close()
    dict_result=[]
    for x in result:
        description=x[0]
        capacity=x[1]
        price=x[2]
        room_availability=x[3]
        image_code=x[4]
        room_type="TRIPLE_ROOM"
        row={'room_type':room_type,'description':description,'capacity':capacity,'price':price,'room_availability':room_availability,'image_code':image_code}

        dict_result.append(row)
    return render(request,"New_Booking/room_details.html",{'room_info':dict_result})


def quad_room(request):
    dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='xe')
    conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
    c = conn.cursor()
    RoomType = "QUAD_ROOM"
    
    statement = "SELECT DESCRIPTION,CAPACITY,PRICE,ROOM_AVAILABILITY,IMAGE_CODE from HRS_OURDATABASE.ROOM WHERE ROOM_TYPE=" + "\'" + RoomType+ "\'"
    c.execute(statement)
    result = c.fetchall()
    c.close()
    dict_result=[]
    for x in result:
        description=x[0]
        capacity=x[1]
        price=x[2]
        room_availability=x[3]
        image_code=x[4]
        room_type="QUAD_ROOM"
        row={'room_type':room_type,'description':description,'capacity':capacity,'price':price,'room_availability':room_availability,'image_code':image_code}

        dict_result.append(row)
    return render(request,"New_Booking/room_details.html",{'room_info':dict_result})
def book(request):
    return render(request,"New_Booking/provide_booking_info.html")
def confirm_book(request):
    booking_date=request.POST['booking_date']
    checkin_date=request.POST['checkin_date']
    checkout_date=request.POST['checkout_date']
    phone_number=request.POST['phone_number']
    guest_no=request.POST['guest_no']
    status="PENDING"

    dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='xe')
    conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
    c = conn.cursor()
    customer_id=str(user_info['pk'])


    statement = "INSERT INTO HRS_OURDATABASE.RESERVATION(CHECK_IN,CHECK_OUT,BOOKING_DATE,STATUS,PHONE_NUMBER,GUEST_NO,CUSTOMER_ID) VALUES (" + "TO_DATE("+"\'"+checkin_date+"\',"+"'YYYY/MM/DD')"+","+"TO_DATE("+"\'"+checkout_date+"\',"+"'YYYY/MM/DD')"+","+"TO_DATE("+"\'"+booking_date+"\',"+"'YYYY/MM/DD')"+","+"\'"+status+"\',"+"\'"+phone_number+"\',"+"\'"+guest_no+"\',"+"\'"+customer_id+"\'"+")"

    c.execute(statement)
    conn.commit()
    return redirect("my_booking_status")

def view_details(request):
    return 











    





       
        





    
   

       
        
    
        
        
