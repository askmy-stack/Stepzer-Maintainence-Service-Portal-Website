from datetime import datetime
from urllib.request import FileHandler
from django.contrib.auth.models import User
from django.http.response import Http404, HttpResponseForbidden, HttpResponseNotAllowed
from django.shortcuts import render
import reportlab
from django.shortcuts import redirect, render
# from django import  forms
from home import forms
import time
from maintenence_site.settings import RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY
from home import models
from home import views
from django.http import HttpResponse
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as log_auth
from django.contrib import messages
from django.contrib import redirects
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth.models import User
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.core.mail import EmailMessage
# for generating pdf invoice
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import os
from django.http import FileResponse
from datetime import date
from datetime import datetime
import razorpay
from django.conf import settings
import random
import string
from django.contrib import messages

todays_date = date.today()

def about(request):
    return render(request,"about.html",{})
def contact(request):
    return render(request,"contact.html",{})

@login_required
def profile(request):
    m_id = request.session['m_id']
    info = models.members.objects.get(member_id=m_id)
    per_info = models.User.objects.get(id=int(info.user_id))

    return render(request, "profilepage.html", {"personal": per_info, "genral": info})


months = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
          7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}


def login(request):

    if request.method == 'POST':
        uname = request.POST.get('username')
        pswrd = request.POST.get('password')
        re = authenticate(username=uname, password=pswrd)
        print(re)
        if re:
            if re.is_active:
                log_auth(request, re)
                m_id = models.members.objects.raw(
                    "SELECT member_id from home_members where user_id=(select id from auth_user where username='%s')" % (uname))
                print(m_id)
                for id in m_id:
                    request.session['m_id'] = id.member_id
                    # return HttpResponseRedirect('home/%d'%(id.member_id))
                    return HttpResponseRedirect('home')

            else:
                return HttpResponse("User not active")
        else:
            messages.error(request, 'Invalid Credentials ')
            # return HttpResponseRedirect('login')
            # return HttpResponse("username or passwrd doesnt exist")
    return render(request, 'loginpage.html', context={})

from django.db import DatabaseError
from django.core.validators import validate_email

def signup(request):
    er=0
    # form=forms.signupform()
    if request.method == "POST":

        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        name= fname+" "+lname
        print(name)
        phone = request.POST.get('phone')
        block = request.POST.get('enterblock')
        flat = request.POST.get('flat')
        fl_type = request.POST.get('enterflattype')
        email = request.POST.get('email')
        pswrd = request.POST.get('password')
        cnf_pswrd = request.POST.get('cnf_password')

        user = request.POST.get('username')
            
        
        if len(phone) != 10:
            er=1
            messages.error(request,"Phone number must be 10 digits")
        if models.User.objects.filter(username=user).exists():
            er=1
            messages.error(request,"Username already exists")
        if models.User.objects.filter(email=email).exists():
            er=1
            messages.error(request,"Email already exists")
        if models.members.objects.filter(block=block,flat=flat).exists():
            er=1
            messages.error(request,"block and Flat number already exists")
        if pswrd != cnf_pswrd:
            er=1
            messages.error(request,"Password and confirm passqord doesn't match")
        if er:
            print("1")
            return(HttpResponseRedirect("signup"))
        else:
            print("2")

            obj = models.User.objects.create(first_name=name, email=email.lower(), username=user)
            obj.set_password(pswrd)
            print(obj.id)
            obj.save()
            print(obj.id)
            
            user_data=models.User.objects.get(username=user)
            mem_create=models.members.objects.create(user_id=obj.id,flat=flat,flat_type=fl_type,block=block,phone=phone)
            mem_create.save()
            models.transactions.objects.create(room_id_id=mem_create.member_id,From_mon=1,To_mon=3,From_year=2021,
                To_year=2021,status='paid',amount=300000,currency='INR',type='O',timestamp=datetime.now(),order_id=''.join(random.choices(
                string.ascii_letters + string.digits, k=16)))
            messages.success(request, "Registration Successfull. KINDLY LOGIN !")
            return HttpResponseRedirect(reverse('landing'))
            
        
            
        # try:
            

        #     # print("SELECT id from auth_user where username='%s' limit 1"%(user))
            user_data=models.User.objects.get(username=user)
            mem_create=models.members.objects.create(user_id=obj.id,flat=flat,flat_type=fl_type,block=block,phone=phone)
            mem_create.save()
            # id = models.User.objects.raw("SELECT id from auth_user where username='%s' limit 1" % (user))
            # print(id)
            # for u_id in id:
            #     print(u_id.id)

            #     obj1 = models.members.objects.create(
            #         user_id=u_id.id, phone=phone, block=block, flat=flat, flat_type=fl_type, )
            # obj1.save()
            
        # except DatabaseError as e:
        #     # if id:
        #     #     models.User.objects.raw("DELETE FROM auth_user where id =%d "%(id))
        #     #     return HttpResponseRedirect(reverse('landing'))
        #     messages.error(request, "Registration error")
        #     return HttpResponseRedirect(reverse('landing'))
    return render(request, 'signup.html', context={})


def settings(request):
    m_id = request.session['m_id']
    info = models.members.objects.get(member_id=m_id)
    p_info = models.User.objects.get(id=int(info.user_id))
    emp_data = models.employe.objects.all()
    mem_data = models.User.objects.all()
    print("1")
    mem_name = None
    if request.method == "POST":
        if request.POST.get('name'):
            p_info.first_name = request.POST.get('name')
            p_info.save()
            messages.success(request, "Name Updated successfully")
        elif request.POST.get('phone'):
            info.phone = int(request.POST.get('phone'))
            info.save()
            messages.success(request, "Phone number Updated successfully")

        elif request.POST.get('email'):
            p_info.email = request.POST.get('email')
            p_info.save()
            messages.success(request, "Email Updated successfully")

        elif request.POST.get('password'):
            p_info.set_password = request.POST.get('password')
            p_info.save()
            messages.success(request, "Password Updated successfully")

        elif request.POST.get('flat_type'):
            print("1")

            info.flat_type = request.POST.get('flat_type')
            info.save()
            messages.success(request, "Flat type Updated successfully")

        elif request.POST.get('employe_name') or request.POST.get('present') or request.POST.get('available'):

            emp = models.employe.objects.get(
                emp_id=int(request.POST.get('emp_name')))
            if request.POST.get('present') and request.POST.get('available'):
                emp.Available = request.POST.get('available')

                emp.Present = request.POST.get('present')
                emp.save()
                messages.success(request, "Attendance Marked")

        elif request.POST.get('member_name'):
            print("2")

            print(request.POST.get('chng_desig'))
            m1 = models.User.objects.get(
                first_name=request.POST.get('member_name'))
            mem_data1 = models.members.objects.get(user_id=m1.id)
            if request.POST.get('chng_desig'):
                print("3")

                mem_data1.designation = request.POST.get('chng_desig')
                mem_data1.save()
                messages.success(request, "Member status Changed")
        if request.POST.get('sch_name'):
            print("3")
            print(request.POST.get('sch_name'))
            sch_name=request.POST.get('sch_name')
            ftime=request.POST.get('ftime')
            ttime=request.POST.get('ttime')
            dt=request.POST.get('date')
            sch=models.schedule.objects.create(name=sch_name,from_time=ftime,to_time=ttime,date=dt)
            sch.save()
            messages.success(request, "Schedule Added Successfully")

    return render(request, "settings.html", {"p_info": p_info, "emp_data": emp_data, "mem_data": mem_data})


def landingpg(request):
    # messages.success(request, "Registration Successfull. KINDLY LOGIN !")

    return render(request, 'landingpage.html')

def feature(request):

    return render(request, 'features.html')
@login_required
def employe(request):
    m_id = request.session['m_id']

    mem_data=models.members.objects.get(member_id=m_id)
    user_data=models.User.objects.get(id=mem_data.user_id)
    emp_present = models.employe.objects.raw(
        "select emp_id,count() as cnt from  home_employe WHERE Present='Y' ")
    emp_avail = models.employe.objects.raw(
        "select emp_id,count()  as cnt from  home_employe WHERE Present='Y' AND Available='Y' ")
    emp_unavail = models.employe.objects.raw(
        "select emp_id,count() as cnt  from  home_employe WHERE Available='N'")
    emp_absent = models.employe.objects.raw(
        "select emp_id,count() as cnt  from  home_employe WHERE Present='N' ")
    emp_info = models.employe.objects.raw(
        "select *,emp_id  from  home_employe where Present='Y' ")
    schedule = models.schedule.objects.raw(
        "SELECT schedule_id,* from home_schedule  where date='%s'"%(datetime.now().date().strftime("%Y-%m-%d")) )

    for i in schedule:
        print(i.name)
    # for  i,j in emp_cnt,emp_avail:
    #     unavail=i.cnt-j.cnt
    # for  i,j in emp_cnt,emp_present:
    #     leave=i.cnt-j.cnt
    return render(request, 'Dashboard_emp.html', context={"user_data":user_data,"name":user_data.first_name,"leave": emp_absent, "schedule": schedule, "unavail": emp_unavail, "avail": emp_avail, "emp_info": emp_info, "present": emp_present})


@login_required
def offline(request):
    m_id = request.session['m_id']

    mem_data=models.members.objects.get(member_id=m_id)
    user_data=models.User.objects.get(id=mem_data.user_id)
    if user_data.is_staff:

        if request.method == "POST":
            block = request.POST.get("block")
            flat = request.POST.get("flat")
            residence = request.POST.get("residence")
            # print(block,flat,residence)
            user = models.members.objects.raw(
                "SELECT * from home_members WHERE block='%s' and flat=%d and flat_type='%s'" % (block, int(flat), residence))

            if user:
                for i in user:
                    mid = i.member_id + 1124578999

                return HttpResponseRedirect("offline/%d" % (mid))

            else:
                return HttpResponse('<h1>User not found</h1>')
        return render(request, 'offline1.html', {})
    else:
        return HttpResponseForbidden()


def offline_2(request, mid_t):
    mid = mid_t-1124578999
    user_details = models.members.objects.raw(
        "SELECT member_id,flat_type,block,flat,id,first_name,email,phone from home_members INNER JOIN auth_user ON home_members.user_id=auth_user.id where member_id=%d " % (mid))
    month_data = models.transactions.objects.raw(
        "SELECT id,From_mon,To_mon,To_year FROM home_transactions where room_id_id=%d and status='paid' ORDER BY id DESC LIMIT 1" % (mid))
    for i in month_data:
        frm_db = i.To_mon
        year_db = i.To_year
        print(year_db)
    for i in user_details:
        name = i.first_name
        user_data = i
    years = range(year_db, (todays_date.year + 5))
    if frm_db >=12:
        frm=1
        year=year_db+1

    else:
        frm = frm_db+1
        year=year_db
    frm = months[frm]

    if request.method == "POST" and request.POST.get("frmm") and request.POST.get("to_month") and request.POST.get("frmy") and request.POST.get("to_year"):
        print("postfrpm")
        if request.method == "POST" and request.POST.get("confirmed"):
            print("post and confirm")
        else:
            oid = ''.join(random.choices(
                string.ascii_letters + string.digits, k=16))
        print(oid)

        frmm = request.POST.get("frmm")
        tom = request.POST.get("to_month")
        frmy = request.POST.get("frmy")
        toy = request.POST.get("to_year")
        for key, value in months.items():
            if frmm == value:
                frmm = key
        for key, value in months.items():
            if tom == value:
                tom = key
        # print(frmy,toy,tom,frmm)
        print(frmm, frmy, tom, toy)

        nmon = (int(toy)-int(year_db)) * 12 + (int(tom)-int(frm_db))
        total = nmon*1000*100

        models.transactions.objects.create(timestamp=datetime.today(), room_id_id=mid, order_id=oid, amount=total,
                                           From_mon=frmm, From_year=frmy, To_mon=tom, To_year=toy, currency='INR', type='F', status='initiated')
        return HttpResponseRedirect("confirm/%d/%s" % (nmon, oid))
        # return offline_checkout(request,mid,name,oid,nmon,total)

    return render(request, 'offline_2.html', context={"user": user_data, "from": frm, "months": months, "year": year, "years": years})


def offline_checkout(request, nmon, oid):
    dat = models.transactions.objects.get(order_id=oid)
    mem_info = models.members.objects.get(member_id=int(dat.room_id_id))
    name = models.User.objects.get(id=int(mem_info.user_id))
    frmm, frmy, tom, toy = dat.From_mon, dat.From_year, dat.To_mon, dat.To_year
    template = get_template("autoreceipt.html")
    mailed = 0
    done = 0
    print(request.POST.get("confirmed"))
    if request.method == "POST" and request.POST.get("confirmed"):

        try:
            print("1111111111111111")
            print(dat.status)
            dat.status = 'paid'
            dat.save()
            print(dat.status)
            done = 1

            data = {
                'order_id': dat.order_id,
                'transaction_id': "-",
                "fee": "-",
                "tax": "-",
                "method": "Offline Payment",
                "frmm": months[frmm],
                "frmy": frmy,
                "tom": months[tom],
                "toy": toy,
                "time": dat.timestamp,
                "date": datetime.now().strftime("%Y-%m-%d "),
                'amount': dat.amount/100,
                "block": mem_info.block,
                "flat": mem_info.flat,
                "raw_amount": (dat.amount/100),
                "name": name.first_name
            }
            

            #for save
            template = get_template("autoreceipt.html")
            html = template.render(data)
            result_mail = open('static/%s.pdf' % (oid), 'wb')
            pdf_mail = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result_mail)
            result_mail.close()

            mailed = send_email(request, oid, name.email)
            print(mailed)
            # time.sleep(2)
            # content = "Thanks for using stepzer. Please find attached receipt"
            # email = EmailMessage("Your Receipt for recent transaction having order id %s " % (
            #     ""), content, 'stepzer.noreply@gmail.com', ["darshankale11.dk@gmail.com"])
            # # fd = open("static/%s.pdf"%("WNsRqkXJHXHyxsya"), "rb")
            # # email.attach('receipt.pdf', fd.read(), 'application/pdf')
            # email.attach_file("static/%s" % ("WNsRqkXJHXHyxsya.pdf"))
            # res = email.send()
            return render(request, 'offline_checkout.html', context={"done": done,"mailed":mailed})
        except:
            print("22222222222")

            dat.status='failed'
            done=2
            return render(request,'offline_checkout.html',context={"done":done})

    print(done)
    return render(request, 'offline_checkout.html', context={"done": done, "nmon": nmon, "frmm": months[frmm], "frmy": frmy, "tom": months[tom], "toy": toy,"name":name.first_name ,"total": dat.amount/100})


@login_required
def d_bills(request):
    m_id = request.session['m_id']
    mem_data=models.members.objects.get(member_id=m_id)
    user_data=models.User.objects.get(id=mem_data.user_id)
    bills = models.transactions.objects.raw(
        "SELECT * from home_transactions WHERE room_id_id=%d And status='paid' order by id DESC limit 7" % (m_id))
    transact = models.transactions.objects.raw(
        "SELECT * from home_transactions WHERE room_id_id=%d  order by id DESC limit 7" % (m_id))
    # for i in bills[0]:
    if ((bills[0].To_year >= todays_date.year) and (bills[0].To_mon >= todays_date.month)):
        print("1")
        due = 0
    else:
        print("2")

        due_mon = (todays_date.year-bills[0].To_year) * 12 + (todays_date.month-bills[0].To_mon)
        due = due_mon*1000
    for i in bills:
        lst_pay = months[i.To_mon] + " " + str(i.To_year)
        break
    
    curr_month,curr_year= todays_date.month,todays_date.year
    return render(request, 'Dashboard_bills.html', context={"user_data": user_data,"name": user_data.first_name,"months": months,"due":due ,"lst_pay": lst_pay, "bills": bills, "transact": transact, "curr_mon": curr_month,"curr_year": curr_year})


@login_required
def D1(request):
    # mem=models.members.objects.model._meta.db_table
    # print(mem)
    m_id = request.session['m_id']
    # print(m_id)
    query_transact = models.members.objects.raw(
        "SELECT id,member_id,from_mon,To_mon,To_year from home_members INNER JOIN home_transactions ON home_members.member_id=home_transactions.room_id_id where home_members.member_id=%d and status='paid' ORDER BY ID DESC LIMIT 1" % (m_id))
    query_info = models.members.objects.raw(
        "SELECT member_id,flat_type,block,flat,is_staff,id,first_name from home_members INNER JOIN auth_user ON home_members.user_id=auth_user.id where member_id=%d " % (m_id))

    for i in query_info:
        print(i.first_name)
        print(i.is_staff)

    # query_name=models.User.objects.raw("SELECT id,first_name from auth_user where id= (SELECT user_id from home_members where member_id=%d limit 1)"%(m_id))
    # query_block=models.User.objects.raw("SELECT member_id,flat_type,block,flat from home_members where member_id= %d limit 1"%(m_id))

    # print(query_2)
    # for i in query_2:
    #     print(i.first_name)
    due = 0
    for i in query_transact:
        if ((i.To_year >= todays_date.year) and (i.To_mon >= todays_date.month)):
            print("1")
            due = 0
        else:
            print("2")

            due_mon = (todays_date.year-i.To_year) * 12 + (todays_date.month-i.To_mon)
            due = due_mon*1000
    query_comm = models.members.objects.raw(
        "SELECT member_id,block,flat,id,first_name,Designation from home_members INNER JOIN auth_user ON home_members.user_id=auth_user.id where Designation in ('Chairman','Vice-Chairman','Secretary','Vice-Secretary','Advisor','Treasurer','Technical-Head')")

    return render(request, 'Dashboard-1.html', context={"q_comm": query_comm, "q_info": query_info, "amt": due})


@login_required
def billing(request):
    m_id = request.session['m_id']
    month_data = models.transactions.objects.raw(
        "SELECT id,From_mon,To_mon,To_year FROM home_transactions where room_id_id=%d and status='paid' ORDER BY id DESC LIMIT 1" % (m_id))
    for i in month_data:
        frm_db = i.To_mon
        year_db = i.To_year
    print(year_db)
    years = range(year_db, (todays_date.year + 5))
    if frm_db >=12:
        frm=1
        year=year_db+1

    else:
        frm = frm_db+1
        year=year_db

    frm = months[frm]
    for data in models.members.objects.raw("SELECT member_id,flat_type,block,flat,id,first_name,email,phone from home_members INNER JOIN auth_user ON home_members.user_id=auth_user.id where member_id=%d " % (m_id)):
        user = data
    if request.method == "POST":
        frmm = request.POST.get("frmm")
        tom = request.POST.get("to_month")
        frmy = request.POST.get("frmy")
        toy = request.POST.get("to_year")
        for key, value in months.items():
            if frmm == value:
                frmm = key
        for key, value in months.items():
            if tom == value:
                tom = key
        # print(frmy,toy,tom,frmm)

        nmon = (int(toy)-int(year_db)) * 12 + (int(tom)-int(frm_db))

        return checkout(request, m_id, nmon, frmy, toy, tom, frmm)

    return render(request, 'billing1.html', context={"user": user, "from": frm, "months": months, "year": year, "years": years})


def checkout(request, m_id, nmon, frmy, toy, tom, frmm):

    # return render(request,"succ.html",context)

    total = nmon*1000
    rzp_amount = total*100
    client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))

    DATA = {
        "amount": rzp_amount,
        "currency": "INR",
        "receipt": "receipt#1",
        "notes": {
            "key1": "value3",
            "key2": "value2"
        }
    }
    order = client.order.create(data=DATA)

    order_id = order.get('id')
    order_status = order.get('status')
    print(order_id)
    unix_t = order.get('created_at')
    tstmp = datetime.fromtimestamp(int(unix_t)).strftime('%Y-%m-%d %H:%M:%S')
    # models.transactions.objects.raw('''INSERT INTO home_transactions(room_id_id,order_id,amount,currency,type,status)
    #                                         values(%d,%s,%d,'INR','O',%s)'''%(m_id,order.get('order_id'),rzp_amount,order.get('status')))

    models.transactions.objects.create(timestamp=tstmp, room_id_id=m_id, order_id=order_id, From_mon=frmm, From_year=frmy, To_mon=tom, To_year=toy,
                                       amount=rzp_amount, currency='INR', type='O', status=order_status)

    return render(request, 'Billing.html', context={"order_id": order_id, "api_key": RAZORPAY_API_KEY, "nmon": nmon, "frmm": months[frmm], "frmy": frmy, "tom": months[tom], "toy": toy, "total": total})


@csrf_exempt
def payment(request, oid):

    client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))
    # only accept POST request.
    if request.method == "POST":

        # try:
        # get the required parameters from post request.
        payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        signature = request.POST.get('razorpay_signature')
        # print(payment_id,razorpay_order_id,signature)

        order_object = models.transactions.objects.get(
            order_id=razorpay_order_id)
        order = client.order.fetch(razorpay_order_id)
        print(order.get('status'))
        # save
        order_object.status = order.get('status')
        order_object.transact_id = payment_id
        order_object.save()

        # order_object.update(order.get('status'))
        # print(order.get('amount'),order.get('status'))
        # print(payment_id,razorpay_order_id,signature)
        # print(resp.status)
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
        # verify the payment signature.
        result = client.utility.verify_payment_signature(params_dict)

        if result is None:
            amount = order_object.amount
            print(amount)
            # try:
            # capture the payment

            client.payment.capture(payment_id, amount, {"currency": "INR"})
            order = client.order.fetch(razorpay_order_id)
            # print(order.get('status'))
            order_object.status = order.get('status')
            order_object.save()

            return pdf_view(request, razorpay_order_id, payment_id, client)
            # except:
            #     # if there is an error while capturing payment.
            #     print("1")
            #     return render(request, 'paymentfail.html')
        else:
            print("2")

            # if signature verification fails.
            return render(request, 'paymentfail.html')
    # except:
        print("3")

        # if we don't find the required parameters in POST data
        return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        print("4")

        return HttpResponseBadRequest()


def send_email(request, order_id, email_id):
    # time.sleep(5)
    order_id, email_id = str(order_id), str(email_id)

    print("received", order_id)
    content = "Thanks for using stepzer. Please find attached receipt"
    email = EmailMessage("Your Receipt for recent transaction for  order id %s " % (
        order_id), content, 'stepzer.noreply@gmail.com', [email_id])
    # fd = open("static/%s.pdf"%("WNsRqkXJHXHyxsya"), "rb")
    # email.attach('receipt.pdf', fd.read(), 'application/pdf')
    email.attach_file("static/%s.pdf" % (order_id))
    res = email.send()
    if res:
        return 1
    else:
        return 0


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    # , link_callback=fetch_resources)
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('Error')

# class GenerateInvoice(View):


def pdf_view(request, order_id, payment_id, client):
    # order = client.order.fetch(order_id)
    m_id = request.session['m_id']
    payment = client.payment.fetch(payment_id)
    order = models.transactions.objects.get(order_id=order_id)
    print(payment.get("amount"))
    print(order.room_id_id)
    for user in models.members.objects.raw("SELECT member_id,flat_type,block,flat,id,first_name,email,phone from home_members INNER JOIN auth_user ON home_members.user_id=auth_user.id where member_id=%d " % (m_id)):
        details = user
    email_id = details.email
    if m_id == order.room_id_id:
        time = payment.get("created_at")
        data = {
            'order_id': payment.get("order_id"),
            'transaction_id': payment_id,
            "fee": payment.get("fee")/100,
            "tax": payment.get("tax")/100,
            "method": payment.get("method"),
            "frmm": months[order.From_mon],
            "frmy": order.From_year,
            "tom": months[order.To_mon],
            "toy": order.To_year,
            "time": datetime.fromtimestamp(int(time)).strftime('%d-%m-%Y %H:%M:%S'),
            "date": datetime.fromtimestamp(int(time)).strftime('%d-%m-%Y'),
            'amount': payment.get("amount")/100,
            "block": details.block,
            "flat": details.flat,
            "raw_amount": (order.amount/100),
            "name": details.first_name
        }

        template = get_template("autoreceipt.html")

        html = template.render(data)
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
        
        template = get_template("autoreceipt.html")

        html = template.render(data)
        # result_mail = BytesIO()#, link_callback=fetch_resources)
        result_mail = open('static/%s.pdf' % (order_id), 'wb')
        pdf_mail = pisa.pisaDocument(
            BytesIO(html.encode("ISO-8859-1")), result_mail)
        print("sent", order_id)

        # mailed = send_email(request, order_id, email_id)
        # print(mailed)
        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type='application/pdf')

        return HttpResponse('Error Genrating invoice')

    else:
        return HttpResponse('AUTHENTICATION ERROR .')
        # try:
    #     order_db = Order.objects.get(id = pk, user = request.user, payment_status = 1)     #you can filter using order_id as well
    # except:
    #     return HttpResponse("505 Not Found")


def logout_view(request):
    del request.session["m_id"]
    logout(request)
    
    return HttpResponseRedirect(reverse("landing"))
