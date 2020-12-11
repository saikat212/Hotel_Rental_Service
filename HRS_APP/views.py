from django.http import HttpResponse
from django.shortcuts import render,redirect
import cx_Oracle

from django.contrib import messages

import HelperClass.Encrypt_Decrypt_Pass as ED_Operation
import datetime

# login
user_info = {}  # holds user data across pages
customer_info_list =[]
admin_info_list =[]
customer_info_dict={}
selected_room_id=[]
modified_reservation_id=[]
modified_reservation_room_id=[]
updated_room_id=[]
selected_reservation_id_in_view_details=[]
input_checkin_date=[]
input_checkout_date=[]
verified_gmail=[]
verified_usertype=[]


# Create your views here.
def login(request):
    return render(request, "auth/LogInOrSignUp.html")

def signup(request):
    return render(request, "auth/SignUp.html")



# homepage URLs
def admin_home(request):
    return render(request, "Homepage/AdminHomePage.html")
    

def customer_home(request):
    return render(request, "Homepage/only_customer_home.html")
    


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
        x = c.fetchone()
        if x is not None:
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
            user_info['username'] = admin_username
            


      
          
            decoded_password=ED_Operation.Encrypt_Decrypt_Passwords(return_password).decryptPassword()
            admin_password=decoded_password
            user_info['admin_password'] = admin_password
           
            if decoded_password == password:
                row={'admin_id':admin_id,'admin_f_name':admin_f_name,'admin_l_name':admin_l_name,'admin_gmail':admin_gmail,'admin_city':admin_city,'admin_country':admin_country,'admin_username':admin_username,'admin_password':admin_password}
                
                admin_info_list.append(row)
                return render(request, "Homepage/AdminHomePage.html",{'name': user_info['f_name'] + ' ' + user_info['l_name']})
                
            else:
                 messages.error(request,'username or password or usertype not correct')
                 return redirect("login")

                
        else:

            messages.error(request,'username or password or usertype not correct')
            return redirect("login")

    elif usertype == "customer":
        statement = "SELECT CUSTOMER_ID, PASSWORD, FIRST_NAME, LAST_NAME,GMAIL,CITY,COUNTRY from HRS_OURDATABASE.CUSTOMER WHERE USERNAME=" + "\'" + username + "\'"
       
        c.execute(statement)

        x = c.fetchone()
        if x is not None:
            
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
                return redirect("customer_home")
                
            else:

                messages.error(request,'username or password or usertype not correct')
                return redirect("login")
        else:
            messages.error(request,'username or password or usertype not correct')
            return redirect("login")
           
           
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


def forgot_password(request):
    return render(request,"auth/verify_gmail.html")
def reset_password(request):
    gmail=request.POST['gmail']
    usertype=request.POST['usertype']
    verified_gmail.append(gmail)
    verified_usertype.append(usertype)


    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='xe')
    conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)

    c = conn.cursor()
    if usertype == "admin":
        statement = "SELECT ADMIN_ID from HRS_OURDATABASE.ADMIN WHERE GMAIL=" + "\'" + gmail + "\'"
        c.execute(statement)
        x = c.fetchone()
        if x is not None:

            return render(request,"auth/reset_password_page.html")
        else:
            verified_gmail.clear()
            verified_usertype.clear()
            return redirect("signup")
    if usertype == "customer":
        statement = "SELECT CUSTOMER_ID from HRS_OURDATABASE.CUSTOMER WHERE GMAIL=" + "\'" + gmail + "\'"
        c.execute(statement)
        x = c.fetchone()
        if x is not None:

            return render(request,"auth/reset_password_page.html")
        else:
            verified_gmail.clear()
            verified_usertype.clear()
            return redirect("signup")



def update_reset_password(request):
    new_password=request.POST['new_password']
    confirm_password=request.POST['confirm_password']
    if new_password==confirm_password:
        if verified_usertype[0]=='admin':
            dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='xe')
            conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
            c = conn.cursor()
            new_encoded_password=ED_Operation.Encrypt_Decrypt_Passwords(confirm_password).encryptPassword()

            statement = "UPDATE HRS_OURDATABASE.ADMIN SET PASSWORD = " + "\'" + new_encoded_password + "\'" + "WHERE GMAIL = " +"\'"+verified_gmail[0]+"\'"
           

            c.execute(statement)
            conn.commit()

        if verified_usertype[0]=='customer':
            dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='xe')
            conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
            c = conn.cursor()
            new_encoded_password=ED_Operation.Encrypt_Decrypt_Passwords(confirm_password).encryptPassword()

            statement = "UPDATE HRS_OURDATABASE.CUSTOMER SET PASSWORD = " + "\'" + new_encoded_password + "\'" + "WHERE GMAIL = " +"\'"+verified_gmail[0]+"\'"
           

            c.execute(statement)
            conn.commit()
        verified_usertype.clear()
        verified_gmail.clear()
        return redirect("login")
    else:
        
        return render(request,"auth/reset_password_page.html")

        




#CustomerHome 
def customer_profile_details(request):
    
    return render(request,"Customer/profile_page.html",{'first_name':user_info['f_name'],'last_name':user_info['l_name'],'gmail':user_info['gmail'],'username':user_info['username']})


def my_booking_status(request):
    dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='xe')
    conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
    c = conn.cursor()
    
    
    statement = "SELECT RESERVATION_ID,STATUS,BOOKING_DATE FROM HRS_OURDATABASE.RESERVATION WHERE CUSTOMER_ID=" + str(user_info['pk'])
    
    c.execute(statement)
    result = c.fetchall()
    c.close()
    dict_result=[]
    for x in result:
        reservation_id=x[0]
        status=x[1]
        booking_date=x[2]
        row={'reservation_id':reservation_id,'name':user_info['f_name']+" "+user_info['l_name'],'gmail':user_info['gmail'],'status':status,'booking_date':booking_date}
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

def filtering_page(request):
    return render(request,"New_Booking/filtering_page.html")

def search_for_booking(request):
    selected_room_type=request.POST['selected_room_type']
    cid=request.POST['searched_checkin_date']
    cod=request.POST['searched_checkout_date']
    input_checkin_date.append(cid)
    input_checkout_date.append(cod)
    info=[]


    dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='xe')
    conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
    c = conn.cursor()
    statement="SELECT RM.ROOM_ID FROM HRS_OURDATABASE.ROOM RM LEFT OUTER JOIN HRS_OURDATABASE.RESERVATION RN ON (RM.ROOM_ID=RN.ROOM_ID) WHERE ((("+"TO_DATE("+"\'"+cod+"\',"+"'YYYY/MM/DD')"+"<=RN.CHECK_IN OR "+"TO_DATE("+"\'"+cid+"\',"+"'YYYY/MM/DD')"+">=RN.CHECK_OUT) OR (RN.ROOM_ID IS NULL)) AND (RM.ROOM_TYPE = "+"\'"+selected_room_type+"\'"+"))"
    
    
   
    c.execute(statement)
    result = c.fetchall()
    c.close()
    for x in result:
        available_room_id=x[0]
        dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='xe')
        conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
        c = conn.cursor()
        statement="SELECT DESCRIPTION,CAPACITY,PRICE,ROOM_TYPE,ROOM_ID FROM HRS_OURDATABASE.ROOM WHERE ROOM_ID="+str(available_room_id)
        c.execute(statement)
        result = c.fetchall()
        c.close()

        for x in result:
            description=x[0]
            capacity=x[1]
            price=x[2]
            room_type=x[3]
            room_id=x[4]
           
            row={'room_id':room_id,'room_type':room_type,'description':description,'capacity':capacity,'price':price}

            info.append(row)
    return render(request,"New_Booking/room_details.html",{'room_info':info})




def single_room(request):
    dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='xe')
    conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
    c = conn.cursor()
    RoomType = "SINGLE_ROOM"
    
    statement = "SELECT * from HRS_OURDATABASE.ROOM WHERE ROOM_TYPE=" + "\'" + RoomType+ "\'"
    c.execute(statement)
    result = c.fetchall()
    c.close()
    dict_result=[]
    single_room_id_list=[]
    for x in result:
        single_room_id_list.append(x[0])

        description=x[0]
        capacity=x[1]
        price=x[2]
    
        image_code=x[3]
        room_id=x[4]
        room_type="SINGLE_ROOM"
        row={'room_id':room_id,'room_type':room_type,'description':description,'capacity':capacity,'price':price,'image_code':image_code}

        dict_result.append(row)
    return render(request,"New_Booking/room_details.html",{'room_info':dict_result})

    
def double_room(request):
    dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='xe')
    conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
    c = conn.cursor()
    RoomType = "DOUBLE_ROOM"
    
    statement = "SELECT DESCRIPTION,CAPACITY,PRICE,ROOM_AVAILABILITY,IMAGE_CODE,ROOM_ID from HRS_OURDATABASE.ROOM WHERE ROOM_TYPE=" + "\'" + RoomType+ "\'"
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
        room_id=x[5]
        room_type="DOUBLE_ROOM"
        row={'room_id':room_id,'room_type':room_type,'description':description,'capacity':capacity,'price':price,'room_availability':room_availability,'image_code':image_code}

        dict_result.append(row)
    return render(request,"New_Booking/room_details.html",{'room_info':dict_result})

def triple_room(request):
    dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='xe')
    conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
    c = conn.cursor()
    RoomType = "TRIPLE_ROOM"
    
    statement = "SELECT DESCRIPTION,CAPACITY,PRICE,ROOM_AVAILABILITY,IMAGE_CODE,ROOM_ID from HRS_OURDATABASE.ROOM WHERE ROOM_TYPE=" + "\'" + RoomType+ "\'"
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
        room_id=x[5]
        room_type="TRIPLE_ROOM"
        row={'room_id':room_id,'room_type':room_type,'description':description,'capacity':capacity,'price':price,'room_availability':room_availability,'image_code':image_code}

        dict_result.append(row)
    return render(request,"New_Booking/room_details.html",{'room_info':dict_result})


def quad_room(request):
    dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='xe')
    conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
    c = conn.cursor()
    RoomType = "QUAD_ROOM"
    
    statement = "SELECT DESCRIPTION,CAPACITY,PRICE,ROOM_AVAILABILITY,IMAGE_CODE,ROOM_ID from HRS_OURDATABASE.ROOM WHERE ROOM_TYPE=" + "\'" + RoomType+ "\'"
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
        room_id=x[5]
        room_type="QUAD_ROOM"
        row={'room_id':room_id,'room_type':room_type,'description':description,'capacity':capacity,'price':price,'room_availability':room_availability,'image_code':image_code}

        dict_result.append(row)
    return render(request,"New_Booking/room_details.html",{'room_info':dict_result})
def book(request):
    val=request.POST['selected_room_id']
    selected_room_id.append(val)
    return render(request,"New_Booking/provide_booking_info.html")
def confirm_book(request):
    booking_room_id=request.POST['room_id']
    checkin_date=input_checkin_date[0]
    checkout_date=input_checkout_date[0]
    dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='xe')
    conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
    c = conn.cursor()
    c.execute("SELECT SYSDATE FROM HRS_OURDATABASE.ROOM")
    r=c.fetchall()
    c.close()
    for x1 in r:
        bid=x1[0]
    status="PENDING"
    booking_date=str(bid.date())

    dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='xe')
    conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
    c = conn.cursor()
    customer_id=str(user_info['pk'])
    

    
    statement = "INSERT INTO HRS_OURDATABASE.RESERVATION(CHECK_IN,CHECK_OUT,BOOKING_DATE,STATUS,CUSTOMER_ID,ROOM_ID) VALUES (" + "TO_DATE("+"\'"+checkin_date+"\',"+"'YYYY/MM/DD')"+","+"TO_DATE("+"\'"+checkout_date+"\',"+"'YYYY/MM/DD')"+","+"TO_DATE("+"\'"+booking_date+"\',"+"'YYYY/MM/DD')"+","+"\'"+status+"\',"+"\'"+customer_id+"\',"+"\'"+str(booking_room_id)+"\'"+")"
    
    c.execute(statement)
    conn.commit()
    selected_room_id.clear()
    return redirect("my_booking_status")

def view_details(request):
    selected_reservation_id_in_view_details.append(request.POST['reservation_id'])

    dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='xe')
    conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
    c1 = conn.cursor()
    statement = "SELECT * FROM HRS_OURDATABASE.RESERVATION WHERE RESERVATION_ID="+str(selected_reservation_id_in_view_details[0])
    c1.execute(statement)
    
    result = c1.fetchall()
    c1.close()
    
    booking_info=[]
    for x in result:
        reservation_id=x[0]
        checkin_date=x[1]
        checkout_date=x[2]
        booking_customer_id=x[3]
        total_day_in_date_formate=checkout_date-checkin_date
        total_day=total_day_in_date_formate.days
        bin=x[4]
        
        booking_date=bin

        status=x[5]
        phone_number=x[6]
        guest_no=x[7]
        reserved_room_id=x[8]
        

        row={'reservation_id':reservation_id,'checkin_date':checkin_date,'checkout_date':checkout_date,'guest_no':guest_no,'name':user_info['f_name']+" "+user_info['l_name'],'gmail':user_info['gmail'],'status':status,'booking_date':booking_date,'phone_number':phone_number}
        booking_info.append(row)
    
    dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='xe')
    conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
    c1 = conn.cursor()
    statement = "SELECT * FROM HRS_OURDATABASE.ROOM WHERE ROOM_ID="+str(reserved_room_id)
    c1.execute(statement)
    
    result = c1.fetchall()
    c1.close()
    room_info=[]
    for x in result:
        room_id=x[0]
        building=x[1]
        floor=x[2]
        capacity=x[3]
        number_of_bed=x[4]

        price=x[5]
        room_type=x[6]
        description=x[7]
        image_code=x[8]
        total_bill=int(total_day*price)
        row={'room_type':room_type,'capacity':capacity,'number_of_bed':number_of_bed,'price':price,'building':building,'floor':floor,'description':description,'image_code':image_code,'total_bill':total_bill}
        room_info.append(row)
    

    selected_reservation_id_in_view_details.clear()
    return render(request,"New_Booking/view_booking_details.html",{'booking_info':booking_info,'room_info':room_info})
def invoice(request):


    return render(request,"New_Booking/invoice.html")

def contact_submit(request):
    rating_number=request.POST['rate']
    customer_id=user_info['pk']
    name=user_info['f_name']+" "+user_info['l_name']
    message=request.POST['message']

    dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='xe')
    conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
    c = conn.cursor()
    c.execute("SELECT SYSDATE FROM HRS_OURDATABASE.ROOM")
    r=c.fetchall()
    c.close()
    for x1 in r:
        bid=x1[0]
        date_of_feedback=str(bid.date())
    

    dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='xe')
    conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
    c = conn.cursor()

    statement = "INSERT INTO HRS_OURDATABASE.FEEDBACK(CUSTOMER_ID,NAME,MESSAGE,RATING,DATE_OF_FEEDBACK) VALUES (" + "\'" +str(customer_id)+"\',"+"\'" +name+"\',"+"\'" +message+"\',"+"\'" +str(rating_number)+"\',"+"TO_DATE("+"\'"+date_of_feedback+"\',"+"'YYYY/MM/DD'))"
   
        
    c.execute(statement)
    conn.commit()
    return redirect("customer_home")








###admin home
def admin_profile_details(request):
    return render(request,"admin/profile_page.html",{'first_name':user_info['f_name'],'last_name':user_info['l_name'],'gmail':user_info['gmail'],'username':user_info['username']})

  

def update_admin_profile(request):
    fname=request.POST['fname']
    lname=request.POST['lname']
    gmail=request.POST['gmail']
    username=request.POST['username']
    if fname != user_info['f_name']:
        user_info['f_name']=fname


        dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='xe')
        conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
        c = conn.cursor()

        statement = "UPDATE HRS_OURDATABASE.ADMIN SET FIRST_NAME = " + "\'" + fname + "\'" + "WHERE ADMIN_ID = " + str(
            user_info['pk'])

        c.execute(statement)
        conn.commit()
    if lname != user_info['l_name']:

        user_info['l_name']=lname


        dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='xe')
        conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
        c = conn.cursor()

        statement = "UPDATE HRS_OURDATABASE.ADMIN SET LAST_NAME = " + "\'" + lname + "\'" + "WHERE ADMIN_ID = " + str(
            user_info['pk'])

        c.execute(statement)
        conn.commit()
    if gmail != user_info['gmail']:

        user_info['gmail']=gmail


        dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='xe')
        conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
        c = conn.cursor()

        statement = "UPDATE HRS_OURDATABASE.ADMIN SET GMAIL = " + "\'" + gmail + "\'" + "WHERE ADMIN_ID = " + str(
            user_info['pk'])

        c.execute(statement)
        conn.commit()

    if username != user_info['username']:

        user_info['username']=username


        dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='xe')
        conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
        c = conn.cursor()

        statement = "UPDATE HRS_OURDATABASE.ADMIN SET USERNAME = " + "\'" + username + "\'" + "WHERE ADMIN_ID = " + str(
            user_info['pk'])

        c.execute(statement)
        conn.commit()

    return redirect("admin_profile_details")

def admin_change_password(request):
    return render(request,"admin/adminchangepassword.html",{'admin_password_from_database':user_info['admin_password']})
def update_admin_password(request):
    current_password=request.POST['current_password']
    new_password=request.POST['new_password']
    confirm_password=request.POST['confirm_password']
    if current_password==user_info['admin_password']:
        if new_password==confirm_password:
            new_encoded_password=ED_Operation.Encrypt_Decrypt_Passwords(confirm_password).encryptPassword()

            dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='xe')
            conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
            c = conn.cursor()

            statement = "UPDATE HRS_OURDATABASE.ADMIN SET PASSWORD = " + "\'" + new_encoded_password + "\'" + "WHERE ADMIN_ID = " + str(
                user_info['pk'])

            c.execute(statement)
            conn.commit()
            return render(request, "Homepage/AdminHomePage.html",{'name': user_info['f_name'] + ' ' + user_info['l_name']})
        else:
            return HttpResponse("Give similiar Password with new password")
        return redirect("update_admin_password")
    else:
        return HttpResponse("Provide correct password of previous")

def hotel_review(request):
    dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='xe')
    conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
    c1 = conn.cursor()
    statement = "SELECT * FROM HRS_OURDATABASE.FEEDBACK ORDER BY DATE_OF_FEEDBACK ASC"
    c1.execute(statement)
    
    result = c1.fetchall()
    c1.close()
    
    feedback_info=[]
    for x in result:
        msg=x[1]
        rating=x[2]
        name=x[3]
        date_of_feedback=(x[4]).date()

       
        row={'msg':msg,'rating':rating,'name':name,'date_of_feedback':date_of_feedback}
        feedback_info.append(row)

    return render(request,"Homepage/hotel_review.html",{'feedback_info':feedback_info})

# Booking management in admin

def all_booking(request):
    dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='xe')
    conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
    c1 = conn.cursor()
    statement = "SELECT * FROM HRS_OURDATABASE.RESERVATION "
    c1.execute(statement)
    
    result = c1.fetchall()
    c1.close()
    
    booking_info=[]
    for x in result:
        reservation_id=x[0]
        checkin_date=(x[1]).date()
        checkout_date=(x[2]).date()
        booking_customer_id=x[3]
       
        booking_date=(x[4]).date()

        status=x[5]
        phone_number=x[6]
        guest_no=x[7]
        reserved_room_id=x[8]

        conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
        c2 = conn.cursor()
        statement = "SELECT FIRST_NAME,LAST_NAME,GMAIL FROM HRS_OURDATABASE.CUSTOMER WHERE CUSTOMER_ID="+str(booking_customer_id)
        c2.execute(statement)
    
        result1 = c2.fetchall()
        c2.close()
        for x1 in result1:

            fname=x1[0]
            lname=x1[1]
            gmail=x1[2]


        row={'reservation_id':reservation_id,'checkin_date':checkin_date,'checkout_date':checkout_date,'guest_no':guest_no,'status':status,'booking_date':booking_date,'phone_number':phone_number,'name':fname+" "+lname,'gmail':gmail}
        booking_info.append(row)
    
    return render(request,"admin/all_booking.html",{'booking_info':booking_info})
def booking_modify(request):
    selected_reservation_id=request.POST['reservation_id']
    modified_reservation_id.append(selected_reservation_id)


    dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='xe')
    conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
    c1 = conn.cursor()
    statement = "SELECT * FROM HRS_OURDATABASE.RESERVATION WHERE RESERVATION_ID="+str(selected_reservation_id)
    c1.execute(statement)
    
    result = c1.fetchall()
    c1.close()
    
    booking_info=[]
    for x in result:
        reservation_id=x[0]
        checkin_date=(x[1]).date()
        checkout_date=(x[2]).date()
        booking_customer_id=x[3]
        total_day_in_date_formate=checkout_date-checkin_date
        total_day=total_day_in_date_formate.days
        
        
        booking_date=(x[4]).date()

        status=x[5]
        phone_number=x[6]
        guest_no=x[7]
        reserved_room_id=x[8]
        

        row={'reservation_id':reservation_id,'checkin_date':checkin_date,'checkout_date':checkout_date,'name':user_info['f_name']+" "+user_info['l_name'],'gmail':user_info['gmail'],'status':status,'booking_date':booking_date}
        booking_info.append(row)
    
    dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='xe')
    conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
    c1 = conn.cursor()
    statement = "SELECT * FROM HRS_OURDATABASE.ROOM WHERE ROOM_ID="+str(reserved_room_id)
    c1.execute(statement)
    
    result = c1.fetchall()
    c1.close()
    room_info=[]
    for x in result:
        room_id=x[0]
        building=x[1]
        floor=x[2]
        capacity=x[3]
        number_of_bed=x[4]

        price=x[5]
        
        room_type=x[6]
        description=x[7]
        image_code=x[8]
        total_bill=int(total_day*price)
        row={'room_type':room_type,'capacity':capacity,'price':price,'building':building,'floor':floor,'description':description,'total_bill':total_bill}
        room_info.append(row)



    dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='xe')
    conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
    c1 = conn.cursor()
    statement = "SELECT * FROM HRS_OURDATABASE.CUSTOMER WHERE CUSTOMER_ID="+str(booking_customer_id)
    c1.execute(statement)
    
    result = c1.fetchall()
    c1.close()
    customer_info=[]
    for x in result:
        fname=x[1]
        lname=x[2]
        name=fname+" "+lname
        gmail=x[3]
        city=x[4]
        country=x[5]
        
        
        row={'name':name,'gmail':gmail,'city':city,'country':country}
        customer_info.append(row)

    return render(request,"admin/edit_status.html",{'booking_info':booking_info,'room_info':room_info,'customer_info':customer_info})

def edit_status(request):
    modified_status=request.POST['modified_status']

    dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='xe')
    conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
    c = conn.cursor()
    statement = "UPDATE HRS_OURDATABASE.RESERVATION SET STATUS = " + "\'" + modified_status + "\'" + "WHERE RESERVATION_ID = " + str(modified_reservation_id[0])
    c.execute(statement)
    conn.commit()
    modified_reservation_id.clear()
    modified_reservation_room_id.clear()
    if(modified_status=="PENDING"):
        return redirect("pending_booking")
    if(modified_status=="APPROVED"):
        return redirect("approved_booking")
    if(modified_status=="CANCELLED"):
        return redirect("cancelled_booking")
def approved_booking(request):
    dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='xe')
    conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
    c1 = conn.cursor()
    expected_status="APPROVED"
    statement = "SELECT * FROM HRS_OURDATABASE.RESERVATION WHERE STATUS="+"\'"+expected_status+"\'"
    c1.execute(statement)
    
    result = c1.fetchall()
    c1.close()
    
    booking_info=[]
    for x in result:
        reservation_id=x[0]
        checkin_date=(x[1]).date()
        checkout_date=(x[2]).date()
        booking_customer_id=x[3]
        booking_date=(x[4]).date()

        status=x[5]
        phone_number=x[6]
        guest_no=x[7]
        reserved_room_id=x[8]

        conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
        c2 = conn.cursor()
        statement = "SELECT FIRST_NAME,LAST_NAME,GMAIL FROM HRS_OURDATABASE.CUSTOMER WHERE CUSTOMER_ID="+str(booking_customer_id)
        c2.execute(statement)
    
        result1 = c2.fetchall()
        c2.close()
        for x1 in result1:

            fname=x1[0]
            lname=x1[1]
            gmail=x1[2]


        row={'reservation_id':reservation_id,'checkin_date':checkin_date,'checkout_date':checkout_date,'guest_no':guest_no,'status':status,'booking_date':booking_date,'phone_number':phone_number,'name':fname+" "+lname,'gmail':gmail}
        booking_info.append(row)
    return render(request,"admin/approved_booking.html",{'booking_info':booking_info})


def pending_booking(request):
    dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='xe')
    conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
    c1 = conn.cursor()
    expected_status="PENDING"
    statement = "SELECT * FROM HRS_OURDATABASE.RESERVATION WHERE STATUS="+"\'"+expected_status+"\'"
    c1.execute(statement)
    
    result = c1.fetchall()
    c1.close()
    
    booking_info=[]
    for x in result:
        reservation_id=x[0]
        checkin_date=(x[1]).date()
        checkout_date=(x[2]).date()
        booking_customer_id=x[3]
        booking_date=(x[4]).date()

        status=x[5]
        phone_number=x[6]
        guest_no=x[7]
        reserved_room_id=x[8]

        conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
        c2 = conn.cursor()
        statement = "SELECT FIRST_NAME,LAST_NAME,GMAIL FROM HRS_OURDATABASE.CUSTOMER WHERE CUSTOMER_ID="+str(booking_customer_id)
        c2.execute(statement)
    
        result1 = c2.fetchall()
        c2.close()
        for x1 in result1:

            fname=x1[0]
            lname=x1[1]
            gmail=x1[2]


        row={'reservation_id':reservation_id,'checkin_date':checkin_date,'checkout_date':checkout_date,'guest_no':guest_no,'status':status,'booking_date':booking_date,'phone_number':phone_number,'name':fname+" "+lname,'gmail':gmail}
        booking_info.append(row)
    
    return render(request,"admin/pending_booking.html",{'booking_info':booking_info})

def cancelled_booking(request):
    dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='xe')
    conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
    c1 = conn.cursor()
    expected_status="CANCELLED"
    statement = "SELECT * FROM HRS_OURDATABASE.RESERVATION WHERE STATUS="+"\'"+expected_status+"\'"
    c1.execute(statement)
    
    result = c1.fetchall()
    c1.close()
    
    booking_info=[]
    for x in result:
        reservation_id=x[0]
        checkin_date=(x[1]).date()
        checkout_date=(x[2]).date()
        booking_customer_id=x[3]
        booking_date=(x[4]).date()

        status=x[5]
        phone_number=x[6]
        guest_no=x[7]
        reserved_room_id=x[8]

        conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
        c2 = conn.cursor()
        statement = "SELECT FIRST_NAME,LAST_NAME,GMAIL FROM HRS_OURDATABASE.CUSTOMER WHERE CUSTOMER_ID="+str(booking_customer_id)
        c2.execute(statement)
    
        result1 = c2.fetchall()
        c2.close()
        for x1 in result1:

            fname=x1[0]
            lname=x1[1]
            gmail=x1[2]


        row={'reservation_id':reservation_id,'checkin_date':checkin_date,'checkout_date':checkout_date,'guest_no':guest_no,'status':status,'booking_date':booking_date,'phone_number':phone_number,'name':fname+" "+lname,'gmail':gmail}
        booking_info.append(row)
    return render(request,"admin/cancelled_booking.html",{'booking_info':booking_info})
    
def add_room(request):
    return render(request,"admin/take_room_information.html")
def complete_add_room(request):
    room_type=request.POST['room_type']
    building=request.POST['building']
    floor=request.POST['floor']
    capacity=request.POST['capacity']
    number_of_bed=request.POST['number_of_bed']
    price=request.POST['price']
    description=request.POST['description']


    dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='xe')
    conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
    c = conn.cursor()
        
    statement = "INSERT INTO HRS_OURDATABASE.ROOM(BUILDING,FLOOR,CAPACITY,NUMBER_OF_BED,PRICE,ROOM_TYPE,DESCRIPTION) VALUES (" + "\'" + str(building) + \
                    "\', " + "\'" + str(floor) + "\'," + "\'" +str(capacity)+ "\', " + "\'" +str(number_of_bed) + "\', " + "\'" + str(price) + "\',"  + "\'" +room_type+ "\'," + "\'" +description+ "\'" ")"
        
    c.execute(statement)
    conn.commit()
    return redirect("admin_home")

def manage_room(request):

    dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='xe')
    conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
    c = conn.cursor()
    statement="SELECT * FROM HRS_OURDATABASE.ROOM"

    c.execute(statement)
    
    result = c.fetchall()
    c.close()
    
    room_info=[]
    for x in result:
        room_id=x[0]
 
        building=x[1]
        floor=x[2]
        capacity=x[3]
        number_of_bed=x[4]
        price=x[5]
        room_type=x[6]
        description=x[7]
        img_code=x[8]

        row={'room_id':room_id,'building':building,'floor':floor,'capacity':capacity,'number_of_bed':number_of_bed,'price':price,'room_type':room_type,'description':description}
        room_info.append(row)
    return render(request,"admin/all_room_information.html",{'room_info':room_info})
def update_room_info(request):
    update_room_id=request.POST['room_id']
    updated_room_id.append(update_room_id)

    dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='xe')
    conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
    c = conn.cursor()
    statement="SELECT * FROM HRS_OURDATABASE.ROOM WHERE ROOM_ID="+str(update_room_id)

    c.execute(statement)
    
    result = c.fetchall()
    c.close()
    
    room_info=[]
    for x in result:
        room_id=x[0]
 
        building=x[1]
        floor=x[2]
        capacity=x[3]
        number_of_bed=x[4]
        price=x[5]
        room_type=x[6]
        description=x[7]
        img_code=x[8]

    return render(request,"admin/room_editing_page.html",{'room_id':room_id,'building':building,'floor':floor,'capacity':capacity,'number_of_bed':number_of_bed,'price':price,'room_type':room_type,'description':description})

def complete_update_room_info(request):

    room_type=request.POST['room_type']
    building=request.POST['building']
    floor=request.POST['floor']
    capacity=request.POST['capacity']
    number_of_bed=request.POST['number_of_bed']
    price=request.POST['price']
    description=request.POST['description']


    dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='xe')
    conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
    c = conn.cursor()
    statement = "UPDATE HRS_OURDATABASE.ROOM SET BUILDING = " + "\'" + building + "\'," + "FLOOR = " + "\'" + str(floor)+ "\'," +"CAPACITY = " + "\'" + str(capacity)+ "\'," +"NUMBER_OF_BED = " + "\'" + str(number_of_bed)+ "\'," +"PRICE = " + "\'" + str(price)+ "\'," +"ROOM_TYPE = " + "\'" +room_type+ "\'," +"DESCRIPTION = " + "\'" +description+ "\'" + "WHERE ROOM_ID = " + str(updated_room_id[0])
          
    c.execute(statement)
    conn.commit()
    updated_room_id.clear()
    return redirect("admin_home")

    
    
#edited design

def about(request):
    return render(request, "Customer/about.html")

def contact(request):
    return render(request, "Customer/contact.html")



def search_by_reservation_id(request):
    searched_reservation_id=request.POST['searched_reservation_id']
    dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='xe')
    conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
    c1 = conn.cursor()
    statement = "SELECT * FROM HRS_OURDATABASE.RESERVATION WHERE RESERVATION_ID="+str(searched_reservation_id)
    if statement:

        c1.execute(statement)
    
        result = c1.fetchall()
        c1.close()
    
        booking_info=[]
        for x in result:
            reservation_id=x[0]
            checkin_date=x[1]
            checkout_date=x[2]
            booking_customer_id=x[3]
            booking_date=x[4]

            status=x[5]
            phone_number=x[6]
            guest_no=x[7]
            reserved_room_id=x[8]

            dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='xe')
            conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
            c1 = conn.cursor()
            statement = "SELECT FIRST_NAME,LAST_NAME,GMAIL FROM HRS_OURDATABASE.CUSTOMER WHERE CUSTOMER_ID="+str(booking_customer_id)
            c1.execute(statement)
    
            result = c1.fetchall()
            c1.close()
            for x in result:

                fname=x[0]
                lname=x[1]
                gmail=x[2]
    


            row={'reservation_id':reservation_id,'checkin_date':checkin_date,'checkout_date':checkout_date,'guest_no':guest_no,'status':status,'booking_date':booking_date,'phone_number':phone_number,'name':fname+" "+lname,'gmail':gmail}
            booking_info.append(row)
        
        
    
        return render(request,"admin/all_booking.html",{'booking_info':booking_info})
    else:
        return render(request,"admin/not_found_msg.html")
    

def notification(request):
    dsn_tns=cx_Oracle.makedsn('localhost','1521',service_name='xe')
    conn = cx_Oracle.connect(user='HRS_OURDATABASE', password='12345', dsn=dsn_tns)
    c = conn.cursor()
    statement="SELECT * FROM HRS_OURDATABASE.CONTACT"

    c.execute(statement)
    
    result = c.fetchall()
    c.close()
    
    contact_info=[]
    for x in result:
        gmail=x[0]
        reason=x[1]
        message=x[2]

        row={'gmail':gmail,'reason':reason,'message':message}
        contact_info.append(row)
    return render(request,"admin/all_notification.html",{'contact_info':contact_info})

    

    





    





       
        





    
   

       
        
    
        
        
