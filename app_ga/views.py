from email import message
from unicodedata import category
from urllib import request
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import myusers
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.cache import never_cache
from django.views.decorators.cache import cache_control
from .models import *
from order.models import *
import random
from twilio.rest import Client
from django.core.paginator import Paginator
from ga import settings
import datetime
from datetime import date
import calendar
from django.db.models import Q
from django.db.models import Count
from django.db.models.functions import ExtractMonth,ExtractDay,ExtractYear
from django.http import JsonResponse
import json
from django.utils.crypto import get_random_string
import string
import sweetify
from xhtml2pdf import pisa
from django.template.loader import get_template
import xlwt
from django.db.models import Sum
# Create your views here.


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    
    product = products.objects.distinct('carbrand')
    allcates=categories.objects.all()
    if 'search-product' in request.POST:
            q=request.POST['search-product']
            searchwith=Q(Q(productname__icontains=q)|Q(prodbrand__icontains=q))
            prod=products.objects.filter(searchwith)
    else:
            prod = products.objects.all().order_by('id')

        # prod = products.objects.all()
    p = Paginator(prod, 4)
    page = request.GET.get('page')
    prod = p.get_page(page)
    nums = "a" * prod.paginator.num_pages
    logedin = True
    if 'username' in request.session:
        logedin = True
        use = request.session.get('username')
        userid = myusers.objects.get(username = use)
        recent = recent_products.objects.filter(user = userid).order_by('products','-id').distinct('products')[:4][::-1]
        for i in recent:
            print("'yyy",i.id)
        
    elif 'otp' in request.session:
        logedin = True
        
    else :
        logedin = False


    
    return render(request,'index.html',{'datas': prod,'nums':nums,'cate':allcates,'carbrand':product,'logedin':logedin,'recent':recent})
    # return render(request,'index.html',{'datas': prod,'nums':nums,'logedin':logedin})
    # elif 'otp' in request.session:
    #     return render(request,'index.html', {'datas': prod})
    # else:
    #     return render(request,'indexnot.html',{'datas': prod})
    


def login(request):
    if 'username' in request.session:
        return redirect(index)
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = myusers.objects.filter(username=username, password=password).exists()
        
        
        if user :
            usercheck = myusers.objects.get(username=username)
            if usercheck.status == False:
                 request.session['username'] = username
                 messages.success(request,"You have logged in successfully")
                 return redirect('index')
            else:
                messages.error(request, 'You are blocked')
        else:
            messages.error(request, '*Invalid Username or Password')
            return redirect(login) 
    return render(request,'login.html')

def otpfunc(request):
    otp = random.randint(1000,9999)
    account_sid = "ACf09abc09102db9662b14701508d05275"
    auth_tocken = "a8ec68c50e6a068f7d47bcc038979ba3"
    client = Client(account_sid,auth_tocken)
    
    # phone_number= "7994805975"
    
    # verification = client.verify \
    #                  .services(settings.SERVICE_ID) \
    #                  .verifications \
    #                  .create(to= f"{settings.COUNTRY_CODE}{phone_number}", channel='sms')
    # print(verification.status)
    msg = client.messages.create(
        body = f"Your OTP is {otp}",
        from_ = "+12183575790",
        to = "+917994805975"
    )
    print("otp = ",otp)
    request.session['otp'] = otp
    return redirect(otpverify)


def otplogin(request):
    if 'username' in request.session:
        return redirect(index)
    if request.method=='POST':
        phonenumber = request.POST.get('phonenumber')

        user = myusers.objects.filter(phonenumber=phonenumber).exists()
        
        if user :
            usercheck = myusers.objects.get(phonenumber=phonenumber)
            if usercheck.status == False:
                return redirect(otpfunc)
            #   request.session['username'] = username
            #   messages.success(request,"You have logged in successfully")
            #   return redirect('index')
            else:
                messages.error(request, 'You are blocked')

        else:
            messages.error(request, '*Invalid Username or Phone number')
            return redirect(login) 
    return render(request,'otplogin.html')

def otpverify(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        a=request.session.get('otp')
        print("otp = ",otp,a)
        print(type(otp),type(a))
        if otp == "":
             return render(otpverify)
        if int(otp) == a:
            request.session['otp'] = otp
            messages.success(request,"You have logged in successfully")
            
            return redirect(index)
        else:
            messages.warning(request,"Invalid OTP")
            return redirect(otpverify)
            
    return render(request,'otpverify.html')
    

def register(request):
    if request.method == 'POST':
        firstname=request.POST.get('firstname')
        lastname=request.POST.get('lastname')
        username=request.POST.get('username')
        email=request.POST.get('email')
        phonenumber=request.POST.get('phonenumber')
        password=request.POST.get('password')
        password2=request.POST.get('password2')
        refferal = request.POST.get('refferal')
        if password == password2:
            if myusers.objects.filter(username=username).exists():
                messages.info(request,"Username is already taken")
                return redirect(register)
            elif email == "":
                messages.info(request,"Email field is empty")
                return redirect(register)
            elif myusers.objects.filter(email=email).exists():
                messages.info(request,"Email is already taken")
                return redirect(register)
            else:
                random_code = get_random_string(7, allowed_chars=string.ascii_uppercase + string.digits)
                print("fsfsf",random_code)
                if refferal:
                    use = myusers.objects.filter(refferal_code=refferal).exists
                    if use:
                        se_user = myusers.objects.filter(refferal_code=refferal).exists
                        if se_user:
                            ref_user = myusers.objects.get(refferal_code=refferal)
                            addbal = wallet.objects.get(user = ref_user.id)
                            user = myusers.objects.create(
                            firstname=firstname, lastname=lastname, username=username, email=email,
                            password=password,refferal_code=random_code,phonenumber=phonenumber,status=False)
                            user.save()
                            addbal.balance = addbal.balance+120
                            addbal.save()
                            addwallet=myusers.objects.get(username=username)
                            print("fffffffffff",addwallet.id)
                            createwall=wallet.objects.create(user=addwallet,
                                balance=40
                            )
                            createwall.save()
                    else:
                        print("invalid refferal code")

                else:
                    user = myusers.objects.create(
                        firstname=firstname, lastname=lastname, username=username, email=email,
                            password=password,refferal_code=random_code,phonenumber=phonenumber, status=False)
                    user.save()

                    addwallet=myusers.objects.get(username=username)
                    createwall=wallet.objects.create(user=addwallet,
                                balance=0
                            )
                    createwall.save()
                messages.success(request,'Account has been created successfully')
                return redirect(login)
        else:
            messages.warning(request, 'Password not matching...!!')
            return redirect(register)

    return render(request,'register.html')


def logout(request):
    if 'username' in request.session:
        del request.session['username']
    return redirect(login)

def adminlogin(request):
     if 'susername' in request.session:
        return redirect(adminDashboard)
    
     if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
    
        admin = admins.objects.filter(username=username, password=password).exists()
    
        if admin:
            request.session['susername'] = username
            messages.success(request,"You have logged in successfully")
            return redirect('adminDashboard')
     return render(request,'adminlogin.html')

# def adminhome(request):
#     return render(request,'adminhome.html')

def adminlogout(request):
    if 'susername' in request.session:
        del request.session['susername']
    return redirect(adminlogin)
    
def userdatas(request):
    userlist = myusers.objects.all().order_by('id')
    return render(request,'userdata.html', {'datas': userlist})


def block(request,id):
    user = myusers.objects.get(id=id)
    if user.status is True:
        user.status = False
        user.save()
    else:
        user.status = True
        user.save()
        if 'username' in request.session:
            del request.session['username']
    return redirect(userdatas)

def addproduct(request):
    catedata=categories.objects.all()
    branddata=prodbrands.objects.all()
    carbrdata=carbrands.objects.all()
    if request.method =="POST":
        probj=products()
        probj.created_at=datetime.datetime.now().hour
        probj.productname = request.POST.get('productname')
        probj.price = request.POST.get('price')
        probj.description = request.POST.get('description')
        probj.stocks = request.POST.get('stock')
        rtrn = request.POST.get('retrn')
        if rtrn:
            probj.retrn = True
        else:
            probj.retrn = False
        probj.retrn_policy = request.POST.get('retrn_policy')
        probj.category = request.POST.get('category')
        print(probj.category)
        cateoptions = categories.objects.get(id=probj.category)
        probj.catid = cateoptions
        selecat=cateoptions.categoryname
        probj.category=selecat
        # carbrobj = carbrands.objects.get(id=probj.catid)
        
        probj.carbrand = request.POST.get('carbrand')
        caropts = carbrands.objects.get(id=probj.carbrand)
        probj.carbrid = caropts
        selecarbr=caropts.carbrand
        probj.carbrand=selecarbr
        
        probj.prodbrand = request.POST.get('prodbrand')
        probj.prodbrand = 1
        sel=1
        # brandopts = prodbrands.objects.get(brobj.productbrand=probj.prodbrand)
        
        brandopts=prodbrands.objects.get(id=sel)
        probj.prodid = brandopts

        
        probj.image = request.FILES.get('image')
        probj.image2 = request.FILES.get('image2')
        probj.image3 = request.FILES.get('image3')
        probj.image4 = request.FILES.get('image4')
        
        probj.save()
        # product = products.objects.create(productname=productname,price=price,
        # description=description,category=category,carbrand=carbrand)
        # product.save()
    return render(request,'addproduct.html',{'datas':catedata,'brand':branddata,
    'carbr':carbrdata}  )

# def viewproducts(request):
    # productlist = products.objects.all().order_by('id')
    # return render(request,'index.html', {'datas': productlist})

def addcategory(request):
    
    allcat = categories.objects.all()
    if request.method=="POST":
        cate=request.POST.get('addcategory')        
        if categories.objects.filter(categoryname=cate).exists():
            # message.info("Category already exist")
            sweetify.error(request,"Category Already exist")
            print("thid if working")
        else:
            add=categories.objects.create(
            categoryname=cate
            )
            add.save()
    return render(request,'addcategory.html',{'cats':allcat})

def productlist(request):
    if 'search-product' in request.POST:
        q=request.POST.get('search')
        searchwith=Q(Q(productname__icontains=q)|Q(prodbrand__icontains=q))
        productlist=products.objects.filter(searchwith)
    else:
        productlist = products.objects.all().order_by('id')

    p = Paginator(productlist, 7)
    page = request.GET.get('page')
    productlist = p.get_page(page)
    nums = "a" * productlist.paginator.num_pages
        

    return render(request,'productlist.html',{'datas': productlist,'nums':nums,})


def deleteproduct(request,id):
    mydata = products.objects.get(id=id)
    mydata.delete()
    sweetify.error(request,'Product Deleted Successfully')
    return redirect(productlist)


def prodetail(request,id):
    product = products.objects.get(id=id)
    incart = False
    logedin = False
    
    if 'username' in request.session:
        logedin = True
        username=request.session.get('username')
        userdat=myusers.objects.get(username=username)
        exist1 = cart.objects.filter(userid=userdat,productid=product).exists()
        if exist1 :
            incart= True 
        else:
            incart = False
        recent = recent_products()
        recent.user=userdat
        recent.products = product
        recent.save()
        if request.method == "POST":
            if 'username' in request.session:
                if request.POST.get('cartbt'):
                    print("button clicked")
                    username=request.session.get('username')
                    userdat=myusers.objects.get(username=username)
                    quantity=1
                    prodpr = product.price
                    
                    exist = cart.objects.filter(userid=userdat,productid=product).exists()
                    if exist:
                        incart = True
                        return redirect(prodetail,id)
                        
                    else:
                        addcart = cart.objects.create (
                        userid = userdat,
                        productid = product,
                        quantity = quantity,
                        total_price = prodpr
                        )
                        addcart.save()
                        sweetify.success(request,'Item added to cart')
                        return redirect(prodetail,id)

                if request.POST.get('wishlist_button'):
                    print("button clicked")
                    username=request.session.get('username')
                    userdat=myusers.objects.get(username=username)
                    quantity=1
                    addwish = wishlist.objects.create(
                        userid = userdat,
                        productid = product,
                        quantity = quantity
                    )
                    addwish.save()
    else:
        print("hello")
        if request.method == "POST" :
            print("hi")
            if request.POST.get('cartbt'):
                print("Guest Cart")
            # return redirect(login)        
    # return render(request,'homebase.html',{'datas': product})
    return render(request,'detailproduct.html',{'datas': product,'incart':incart,'logedin':logedin})

def editproduct(request,id):
    catedata=categories.objects.all()
    selprod=products.objects.get(id=id)
    carbrand = carbrands.objects.all()
    prodbrand = prodbrands.objects.all()
    if request.method =="POST":
        prod=products.objects.get(id=id)
        prod.productname = request.POST.get('productname')
        prod.price = request.POST.get('price')
        prod.description = request.POST.get('description')
        prod.category = request.POST.get('category')
        cateoptions=categories.objects.get(id=prod.category)
        prod.catid=cateoptions
        prod.carbrand = request.POST.get('carbrand')
        rtrn = request.POST.get('retrn')
        if rtrn:
            prod.retrn = True
        else:
            prod.retrn = False
        prod.retrn_policy = request.POST.get('retrn_policy')
        getimage = request.FILES.get('image')
        existimage = prod.image
        if getimage:
            prod.image = getimage
        else:
            prod.image = existimage
        prod.save()
        # product = products.objects.create(productname=productname,price=price,
        # description=description,category=category,carbrand=carbrand)
        # product.save()
    return render(request,'editproduct.html',{'prod':selprod,'cate':catedata,'carbr':carbrand,'prodbrand':prodbrand})
  
def sidebar(request):
    return render(request, 'sidebar.html')

def productmanage(request):
    allprod = products.objects.all()
    if request.method=="POST":
        cate=request.POST.get('addcategory')
        if categories.objects.filter(categoryname=cate).exists():
            message.info("Category already exist")
        else:
            add=categories.objects.create(
            categoryname=cate
            )
            add.save()
            
    return render(request,'addcategory.html',{'cats':allprod})


def brandman(request):
    allbrand = prodbrands.objects.all()
    if request.method=="POST":
        brand=request.POST.get('addbrand')
        if prodbrands.objects.filter(productbrand=brand).exists():
            message.warning("Brand already exist")
        else:
            add=prodbrands.objects.create(
            productbrand=brand
            )
            add.save()
    return render(request,'brandman.html',{'brand':allbrand})

def cartlist(request):
    if 'username' in request.session:
        logedin=True
        username = request.session.get('username')
        user=myusers.objects.get(username=username)
        cartitems=cart.objects.filter(userid = user.id)
        a=0
        for i in cartitems:
            if i.productid.dis_price :
                a = a+int(i.productid.dis_price)*int(i.quantity)
            else:
                a = a+int(i.productid.price)*int(i.quantity)
    return render(request,'cartlist2.html',{'cartdat':cartitems,'price':a,'logedin':logedin})

def wishlistt(request):
    # sum=0
    if 'username' in request.session:
        logedin=True
        username = request.session.get('username')
        user=myusers.objects.get(username=username)
        wishitems=wishlist.objects.filter(userid = user.id)       
    return render(request,'wishlist.html',{'wishitems':wishitems,'logedin':logedin})

def userprofile(request):
    if 'username' in request.session:
        logedin=True
        username = request.session.get('username')
        user = myusers.objects.get(username = username)
        
    return render(request,'userprofile.html',{'user':user,'logedin':logedin})

def addaddress(request):
    if 'username' in request.session:
        logedin = True
        username = request.session.get('username')
        user=myusers.objects.get(username=username)
        user_id = user.id
        address=Address.objects.filter(user_id=user_id )
        if request.method == "POST":
            print("hello")
            username = request.session.get('username')
            user=myusers.objects.get(username=username)
            user_id = user.id
            buyer_name = request.POST.get('name')
            buyer_phone = request.POST.get('phone')
            address=request.POST.get('address')
            pincode=request.POST.get('pincode')
            city=request.POST.get('city')
            state=request.POST.get('state')
            
            country="india"
            reg=Address.objects.create(user_id=user_id,buyer_name=buyer_name,buyer_phone=buyer_phone,address=address,pincode=pincode,city=city,state=state,country=country)
            reg.save()
        return render(request,'addaddress.html',{'address':address,'logedin':logedin})

def remove_cart(request,id):
    test=cart.objects.get(id=id)
    test.delete()
    return redirect(cartlist)
def remove_wish(request,id):
    test = wishlist.objects.get(id=id)
    test.delete()
    return redirect(wishlistt)

def qplus(request,id):
    obj=cart.objects.get(id=id)
    value=int(obj.quantity) + 1
    print (obj.quantity)
    obj.quantity=value
    obj.save()
    return redirect(cartlist)

def qminus(request,id):
    obj=cart.objects.get(id=id)
    if int(obj.quantity) > 1:
        value=int(obj.quantity) - 1
        print (obj.quantity)
        obj.quantity=value
        obj.save()
    return redirect(cartlist)

def editprofile(request):
    if 'username' in request.session:
        logedin=True
        user=request.session.get('username')
        userdetail = myusers.objects.get(username=user)
        edit=myusers.objects.get(id=userdetail.id)
        page='name'
        if request.method == 'POST':
            page='name'
            edit.firstname = request.POST.get('firstname')
            edit.lastname = request.POST.get('lastname')
            edit.email = request.POST.get('email')
            edit.save()
            return redirect(userprofile)
    return render(request,'editprofile.html',{'user':userdetail,'page':page,'logedin':logedin})

def changepassword(request,id):
    if 'username' in request.session:
        logedin = True
        edit=myusers.objects.get(id=id)
        if request.method == 'POST':
            oldpass=request.POST.get('oldpass')
            newpass=request.POST.get('newpass')
            confirmpass=request.POST.get('confirmpass')
            if oldpass!="" and newpass!="" and confirmpass!="":
                if edit.password == oldpass:
                    if newpass == confirmpass:
                        if newpass != edit.password:
                            edit.password = newpass
                            edit.save()
                            sweetify.success(request,"Password Changed Succefully")
                            return render(request,'userprofile.html')
                            
                        else:
                            sweetify.error(request,"Password not updated.You have entered your old password..!!")
                    else:        
                        sweetify.error(request,"Password and Confirm Password doesnot match..!!")
                else:
                    sweetify.error(request,'Invalid Old Password*')
                    return render (request,'changepassword.html')
            else:
                sweetify.error(request,"Please fill all the Fields")
        return render (request,'changepassword.html',{'logedin':logedin})

def products_main(request):
        product = products.objects.distinct('carbrand')
        allcates=categories.objects.all()
        
        if 'search-product' in request.POST:
                q=request.POST['search-product']
                searchwith=Q(Q(productname__icontains=q)|Q(prodbrand__icontains=q))
                prod=products.objects.filter(searchwith)
                print('search function')
                
        else:
                print('normal function')
                prod = products.objects.all().order_by('id')
                # off=[]
                # for i in prod:
                #     if i.total_disprice:
                #         price = int(i.price)
                #         dis_price = int(i.total_disprice)
                #         pr = price - dis_price
                #         perc = round(pr/price * 100)
                #         off.append(perc)
                #     else:
                #         off.append(False)
                # print("dscda",off)
        for i in prod:

            # if i.distype == "percentage":
            #     dis
            #     diperc =  disperc
            # else :
            #         c=int(i.price)
            #         d=int(i.total_disprice)
            #         e=c-d
            #         diperc = e/c*(100)
            if i.total_disprice:
                dprice = i.total_disprice
                price = i.price
                off = int(i.price) - int(i.total_disprice)
                perc=off/int(i.price)*100
                perc = round(perc)
                print(i.productname,i.price,i.total_disprice)
                print("llll",perc)
                i.disperc = perc
                i.save()
            # prod = products.objects.all()
        p = Paginator(prod, 4)
        page = request.GET.get('page')
        prod = p.get_page(page)
        nums = "a" * prod.paginator.num_pages
        if 'username' in request.session:
            logedin = True

        elif 'otp' in request.session:
            logedin = True

        else:
            logedin = False

        return render(request,'products_main.html',{'datas': prod,'nums':nums,'cate':allcates,'carbrand':product,'logedin':logedin})
    
    # product=products.objects.filter(carbrand='Toyota')
    # for i in product:
    #     return render(request,'products_main.html')

def filter(request,id):
    
    allcates = categories.objects.all()
    product = products.objects.distinct('carbrand')
    
    print('filter button')
    categ = categories.objects.get(id=id)
    print("YYYYAAAA",categ.categoryname)
    prod = products.objects.filter(category=categ.categoryname)
    

        # prod = products.objects.all()
    p = Paginator(prod, 4)
    page = request.GET.get('page')
    prod = p.get_page(page)
    nums = "a" * prod.paginator.num_pages
    # logedin = True
    if 'username' in request.session:
        logedin = True
    elif 'otp' in request.session:
        logedin = True
    else:
        logedin = False

    return render(request,'products_main.html',{'datas': prod,'nums':nums,'cate':allcates,'carbrand':product,'logedin':logedin})
    
def filterbycar(request,id):
    if 'username' in request.session:
        logedin = True
    elif 'otp' in request.session:
        logedin = True
    else:
        logedin = False
    allcates=categories.objects.all()
    product = products.objects.distinct('carbrand')
    
    print('filter button')

    seleprod = products.objects.get(id=id)
    print("YYYYAAAA",seleprod.carbrand)
    prod = products.objects.filter(carbrand = seleprod.carbrand)
    print(prod)
    
        # prod = products.objects.all()
    p = Paginator(prod, 4)
    page = request.GET.get('page')
    prod = p.get_page(page)
    nums = "a" * prod.paginator.num_pages
    return render(request,'products_main.html',{'datas': prod,'cate':allcates,'carbrand':product,'logedin':logedin})



def adminDashboard(request):
    orders=Order.objects.annotate(month=ExtractMonth('created_at')).values('month').annotate(count=Count('id')).values('month','count')
    monthord=Order.objects.annotate(month=ExtractMonth('created_at')).values('month')
    print("montttt",monthord)
    yearorders=Order.objects.annotate(year=ExtractYear('created_at')).values('year').annotate(count=Count('id')).values('year','count')
    Dayorders=Order.objects.annotate(day=ExtractDay('created_at')).filter(created_at=date.today()).values('day').annotate(count=Count('id')).values('day','count')
    DayNumber=[]
    YearNumber=[]
    monthNumber=[]
    totalOrders=[]
    totaltyearorders=[]
    totaldayorder=[]
    for d in orders:
        monthNumber.append(calendar.month_name[d['month']])
        print("dewdw",monthNumber)
        totalOrders.append(d['count'])
    for d in yearorders:
        YearNumber.append([d['year']])
        totaltyearorders.append(d['count']) 
    for d in Dayorders:
        DayNumber.append([d['day']])
        totaldayorder.append(d['count'])
    

# ---------------------------------- payment --------------------------------- #
    cod = Payment.objects.filter(payment_method = 'COD').aggregate(Count('id')).get('id__count')
    raz = Payment.objects.filter(payment_method = 'razorpay').aggregate(Count('id')).get('id__count')
    pay = Payment.objects.filter(payment_method = 'Paypal').aggregate(Count('id')).get('id__count')
    context={
        'Order':orders,
        'MonthNumber':monthNumber,
        'TotalOrders':totalOrders,
        'YearNumber':YearNumber,
        'totaltyearorders':totaltyearorders,
        'DayNumber':DayNumber,
        'totaldayorder':totaldayorder,
        'paypal':pay,
        'raz':raz,
        'cod':cod
    }
    return render(request,'adminhome.html',context)

def sort(request,id):
    product = products.objects.distinct('carbrand')
    allcates=categories.objects.all()
    if 'search-product' in request.POST:
            q=request.POST['search-product']
            searchwith=Q(Q(productname__icontains=q)|Q(prodbrand__icontains=q))
            prod=products.objects.filter(searchwith,stock_status=True)
            print('search function')
            
    else:
        if id == 1:
            print('normal function')
            prod = products.objects.filter(stock_status=True).order_by('price')
            for i in prod:
                print("all prod",i.price )
        elif id == 2:
            prod = products.objects.filter(stock_status=True).order_by('-price')
        else:
            prod = products.objects.filter(stock_status=True).order_by('-created_at')

    
        # prod = products.objects.all()
    p = Paginator(prod, 4)
    page = request.GET.get('page')
    prod = p.get_page(page)
    nums = "a" * prod.paginator.num_pages
    
    if 'username' in request.session:
        logedin=True
    elif 'otp' in request.session:
        logedin=True
    else:
        logedin=False
    return render(request,'products_main.html',{'datas': prod,'nums':nums,'cate':allcates,'carbrand':product,'logedin':logedin})
    
    


def cart_update(request):
   print('cart')
   body = json.loads(request.body)
   cartv = cart.objects.get(id=body['cart_id'])
   
   cartv.quantity = body['product_qty']
   cartv.total_price = body['total']
   cartv.save()
   print("cart_test",body)
   print("update cart")
   return redirect(cartlist)

def couponman(request):
    allcoup = Coupon.objects.all().order_by('id')
    if request.method == 'POST':
        startdate = request.POST.get('start_date')
        enddate = request.POST.get('end_date')
        minamt = request.POST.get('min_amt')
        coupon_num = request.POST.get('coupon_num')
        disprice = request.POST.get('dis_price')
        disperc = 0
        
        create = Coupon()
        create.start_date=startdate
        create.expiry_date=enddate
        create.minimum_amount=minamt
        create.coupon_number=coupon_num
        create.discount_price=disprice
        create.discount_percentage=disperc
        create.save()
        
    return render (request,'couponman.html',{'coupon':allcoup})

def delete_coupon(request,id):
    coupobj = Coupon.objects.get(id=id)
    coupobj.delete()
    return redirect(couponman)

def shopbycar(request):
    brands = carbrands.objects.all()
    return render(request,'shopbycar.html',{'carbrand':brands})

# sales per day...............
# def sales(request):
#     if 'date' in request.GET:
#         date = request.GET['date']
#         print("datesss",date)
#         Total = 0
#         if date:
#             excel_products = sales_report.objects.all().delete()
#             products =OrderProduct.objects.order_by('-created_at').filter(created_at__icontains=date)
            
#             for product in products:
#                 excel_products = sales_report()
#                 excel_products.date = product.created_at
#                 excel_products.product_name = product.product.productname
#                 excel_products.quantity = product.quantity
#                 excel_products.amount = product.order.order_total
#                 Total += product.order.order_total
#                 excel_products.save()
#             context = {
#             'products':products,
#             }
#             return render(request,'sales.html',context)
#     return render(request,'sales.html')









# # sales per month.............................
# def monthly_sales(request):
#     if 'month_date' in request.GET:
#         month_date = request.GET['month_date']
#         Total = 0
#         if month_date:
#             excel_products = monthly_sales_report.objects.all().delete()
#             # months = OrderProduct.objects.annotate(month=ExtractMonth('created_at'))
#             months = OrderProduct.objects.filter(created_at__icontains = month_date)
#             print("months",months)
#             for month in months:
#                 excel_products = monthly_sales_report()
#                 excel_products.date = month.created_at
#                 excel_products.product_name = month.product.productname
#                 excel_products.quantity = month.quantity
#                 excel_products.amount = month.order.order_total
#                 Total += month.order.order_total
#                 excel_products.save()
#             context = {
#                 'month_products': months,
#                 'Total':Total
#             }
#             return render(request, 'sales.html', context)
#     return redirect(sales)


# # sales per day excel download................
# def export_to_excel(request):
#     response = HttpResponse(content_type='application/ms-excel')
#     response['content-Disposition'] = 'attachment; filename="sales.xls"'
#     wb = xlwt.Workbook(encoding='utf-8')
#     # this will generate a file named as sales Report
#     ws = wb.add_sheet('Sales Report')

#     # Sheet header, first row
#     row_num = 0

#     font_style = xlwt.XFStyle()
#     font_style.font.bold = True

#     columns = ['Date','Product Name', 'Quantity', 'Amount', ]

#     for col_num in range(len(columns)):
#     # at 0 row 0 column
#         ws.write(row_num, col_num, columns[col_num], font_style)

#     font_style = xlwt.XFStyle()
#     total = 0
#     rows = sales_report.objects.all().values_list('date','product_name', 'quantity', 'amount')

#     print("row", rows)
#     for row in rows:
#         row_num += 1
#         for col_num in range(len(row)):
#             ws.write(row_num, col_num, row[col_num], font_style)

#     wb.save(response)
#     return response


# def export_to_pdf(request):
#     total_sales = 0
#     report = sales_report.objects.all()
#     sales = OrderProduct.objects.filter(status="OutForDelivery").annotate(Count('id'))

#     for total_sale in report:
#         total_sales += total_sale.amount

#     template_path = 'sales_pdf.html'
#     context = {
#         'report':report,
#         'total_amount':total_sales,
#     }
    
#     # csv file can also be generated using content_type='application/csv
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

#     template = get_template(template_path)
#     html = template.render(context)

#     # create a pdf
#     pisa_status = pisa.CreatePDF(
#         html, dest=response)
#     # if error then show some funny view
#     if pisa_status.err:
#         return HttpResponse('We had some errors <pre>' + html + '</pre>')

#     return response

    #########################################################################################

# def export_to_excel1(request):
#     response = HttpResponse(content_type='application/ms-excel')
#     response['content-Disposition'] = 'attachment; filename="sales.xls"'
#     wb = xlwt.Workbook(encoding='utf-8')
#     # this will generate a file named as sales Report
#     ws = wb.add_sheet('Sales Report')

#     # Sheet header, first row
#     row_num = 0

#     font_style = xlwt.XFStyle()
#     font_style.font.bold = True

#     columns = ['Date','Product Name', 'Quantity', 'Amount', ]

#     for col_num in range(len(columns)):
#     # at 0 row 0 column
#         ws.write(row_num, col_num, columns[col_num], font_style)

#     font_style = xlwt.XFStyle()
#     total = 0
#     rows = monthly_sales_report.objects.all().values_list('date','product_name', 'quantity', 'amount')

#     print("row", rows)
#     for row in rows:
#         row_num += 1
#         for col_num in range(len(row)):
#             ws.write(row_num, col_num, row[col_num], font_style)

#     wb.save(response)
#     return response



# def export_to_pdf1(request):
#     Date = []
#     product_name= []
#     quantity =[]
#     amount=[]
#     rows = monthly_sales_report.objects.all()
#     for i in rows:
#         Date.append(i.date)
#         product_name.append(i.product_name)
#         quantity.append(i.quantity)
#         amount.append(i.amount)
    
#     template_path = 'sales_pdf.html'
#     context = {
#         'brand_name':Date,
#         'order_count':product_name,
#         'total_amount':quantity,
#         'amount':amount,
#     }
    
#     # csv file can also be generated using content_type='application/csv
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

#     template = get_template(template_path)
#     html = template.render(context)

#     # create a pdf
#     pisa_status = pisa.CreatePDF(
#         html, dest=response)
#     # if error then show some funny view
#     if pisa_status.err:
#         return HttpResponse('We had some errors <pre>' + html + '</pre>')

#     return response




def addoffer(request,id):
    add = products.objects.get(id=id)
    if request.method=='POST':
        disprice = request.POST.get('disprice')
        disperc = request.POST.get('disperc')
        if disperc:
                a=int(add.price)*int(disperc)/100
                print("perc sele",disperc)
        elif disprice:
                a=disprice
                print("price sele",disprice)
        else:
                a=0

        add.dis_proprice = int(add.price) - int(a)
        add.dis_applied = True
        add.save()
        exist = add.dis_price
        # existcheck = add.dis_applied
        # if exist :
        
        diis=int(add.price) - int(a)
        print('exist',exist)
        print('totdis',add.total_disprice)
        print("www",a)
        print("www",diis)
        
        if exist:
            if int(exist) >= diis:
                add.total_disprice = diis
                add.save()
            elif int(exist) <= diis :
                print("www",a)
                add.total_disprice = exist
                add.save()
        else:
            add.total_disprice=diis
            add.save()
            
    return render (request,'addoffer.html',{'add':add})

def addoffers(request):
    prod = products.objects.all()
    return render(request,'addoffers.html',{'datas':prod})

def clear_all_offer(request,id):
    prod = products.objects.get(id=id)
    prod.dis_price = None
    prod.dis_proprice = None
    prod.total_disprice = None
    prod.dis_price_type = None
    prod.save()
    sweetify.success(request,'All Offer cleared on thid product')
    return redirect(addoffer,id)

def clear_cate_offer(request,id):
    print("ss",id)
    prod = products.objects.get(id=id)
    prod.dis_price = None
    # prod.dis_proprice = None
    prod.total_disprice = prod.dis_proprice
    prod.save()
    return redirect(addoffer,id)

def clear_pro_offer(request,id):
    print("ss",id)
    prod = products.objects.get(id=id)
    # prod.dis_price = None
    prod.dis_proprice = None
    prod.total_disprice = prod.dis_price
    prod.save()
    return redirect(addoffer,id)

def addbanner(request):
    return redirect(request,'addbanner.html')





def sales_report_date(request):
    data = OrderProduct.objects.all()
    if request.method == 'POST':
        if request.POST.get('month'):
            month = request.POST.get('month')
            print(month)
            data = OrderProduct.objects.filter(created_at__icontains=month)
            
            if data:
                if SalesReport.objects.all():
                    SalesReport.objects.all().delete()
                    for i in data:
                        sales = SalesReport()
                        sales.productName = i.product.productname
                        sales.categoryName = i.product.category
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum']}
                    return render(request,'sales_report_.html',context)
                else:
                    for i in data:
                        sales = SalesReport()
                        sales.productName = i.product.product_name
                        sales.categoryName = i.product.cat_id.category_name
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum']}
                    return render(request,'sales_report_.html',context)
            else:
                messages.warning(request,"Nothing Found!!")
        if request.POST.get('date'):
            date = request.POST.get('date')
            print("0,",date)
            
            date_check = OrderProduct.objects.filter(created_at__icontains=date)
            print(date_check)
            if date_check:
                if SalesReport.objects.all():
                    SalesReport.objects.all().delete()
            
                    for i in date_check:
                        sales = SalesReport()
                        sales.productName = i.product.productname
                        sales.categoryName = i.product.category
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum']}
                    return render(request,'sales_report_.html',context)
                else:
                    for i in date_check:
                        sales = SalesReport()
                        sales.productName = i.product.productname
                        sales.categoryName = i.product.category
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum']}
                    return render(request,'sales_report_.html',context)
            else:
                messages.warning(request,"Nothing Found!!")
        if request.POST.get('date1'):
            date1 = request.POST.get('date1')
            date2 = request.POST.get('date2')
            data_range = OrderProduct.objects.filter(created_at__gte=date1,created_at__lte=date2)
            if data_range:
                if SalesReport.objects.all():
                    SalesReport.objects.all().delete()
            
                    for i in data_range:
                        sales = SalesReport()
                        sales.productName = i.product.productname
                        sales.categoryName = i.product.category
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum']}
                    return render(request,'sales_report_.html',context)
                else:
                    for i in data_range:
                        sales = SalesReport()
                        sales.productName = i.product.productname
                        sales.categoryName = i.product.category
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum']}
                    return render(request,'sales_report_.html',context)
            else:
                messages.warning(request,"Nothing Found!!")
    if data:
        if SalesReport.objects.all():
            SalesReport.objects.all().delete()
            for i in data:
                sales = SalesReport()
                sales.productName = i.product.productname
                sales.categoryName = i.product.category
                sales.date = i.created_at
                sales.quantity = i.quantity
                sales.productPrice = i.product_price
                sales.save()
            sales = SalesReport.objects.all()
            total = SalesReport.objects.all().aggregate(Sum('productPrice'))
            context = { 'sales':sales,'total':total['productPrice__sum']}
            return render(request,'sales_report_.html',context)

        else:
            for i in data:
                sales = SalesReport()
                sales.productName = i.product.productname
                sales.categoryName = i.product.category
                sales.date = i.created_at
                sales.quantity = i.quantity
                sales.productPrice = i.product_price
                sales.save()
            sales = SalesReport.objects.all()
            total = SalesReport.objects.all().aggregate(Sum('productPrice'))
            context = { 'sales':sales,'total':total['productPrice__sum']}
            return render(request,'sales_report_.html',context)
        
    else:
        messages.warning(request,"Nothing Found!!")
    
    return render(request,'sales_report_.html')

def export_to_excel(request):
    response = HttpResponse(content_type = 'application/ms-excel')
    response['content-Disposition'] = 'attachment; filename="sales.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Sales Report') #this will generate a file named as sales Report

     # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Product Name','Category','Price','Quantity', ]

    for col_num in range(len(columns)):
        # at 0 row 0 column
        ws.write(row_num, col_num, columns[col_num], font_style)

    
    font_style = xlwt.XFStyle()
    total = 0

    rows = SalesReport.objects.values_list(
        'productName','categoryName', 'productPrice', 'quantity')
    for row in rows:
        total +=row[2]
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    row_num += 1
    col_num +=1
    ws.write(row_num,col_num,total,font_style)

    wb.save(response)

    return response


def export_to_pdf(request):
    prod = products.objects.all()
    order_count = []
    # for i in prod:
    #     count = SalesReport.objects.filter(product_id=i.id).count()
    #     order_count.append(count)
    #     total_sales = i.price*count
    sales = SalesReport.objects.all()
    total_sales = SalesReport.objects.all().aggregate(Sum('productPrice'))



    template_path = 'sales_pdf.html'
    context = {
        'brand_name':prod,
        'order_count':sales,
        'total_amount':total_sales['productPrice__sum'],
    }
    
    # csv file can also be generated using content_type='application/csv
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response