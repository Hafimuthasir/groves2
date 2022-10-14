# from asyncio.windows_events import NULL
from django.shortcuts import render,redirect
from app_ga.models import *
from app_ga import views
from .models import *
from app_ga.views import *
from app_ga.views import login
import datetime
import json
import io
from django.http import HttpResponse
from django.template.loader import get_template
from django.http import JsonResponse
from django.core.paginator import Paginator
from xhtml2pdf import pisa
from django.utils import timezone
import razorpay
from django.template.loader import *
import xlwt
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt



import pytz
utc=pytz.UTC

# Create your views here.

# def checkout(request):
#     if 'username' in request.session:
#         username = request.session.get('username')
#         user=myusers.objects.get(username=username)
#         cartitems=cart.objects.filter(userid = user.id)

        
#     return render(request,'checkout.html',{'cartdat':cartitems})


def checkout(request):
    
    if 'username' in request.session:
        # id = request.session.get('user_id')
        # cart=cart.objects.filter(user_id=id)
        coupstat=False
        username = request.session.get('username')
        user=myusers.objects.get(username=username)
        cartitems=cart.objects.filter(userid = user.id)
        address=Address.objects.filter(user_id=user.id )
        wall = wallet.objects.get(user = user)
        a=0
        subtotal=0
        logedin=True
        
        minusvalue=0
        disprice=0
        print("hhhhhggg",cartitems)
        
        if cartitems:
            for i in cartitems:
                if i.productid.dis_price :
                    a = a+int(i.productid.total_disprice)*int(i.quantity)
                    subtotal = subtotal+ int(i.productid.total_disprice)*int(i.quantity)
                else:
                    a = a+int(i.productid.price)*int(i.quantity)
                    subtotal = subtotal+ int(i.productid.price)*int(i.quantity)
            
            if request.POST.get('coupon_bt'):
                coupon = request.POST.get('coupon')
                print("couponnum",coupon)
                exist=Coupon.objects.filter(coupon_number=coupon).exists()
        
        
                if exist:
                    coupobj = Coupon.objects.get(coupon_number=coupon)
                    print("myyy",coupobj.start_date)
                    print("ds",coupobj.minimum_amount)
                    
                    d=coupobj.expiry_date
                    print(d,type(d))
                    e =timezone.now()
                    print(e,type(e))
                    g = d >= e
                    print(g)
                    if g :
                        print(coupobj.minimum_amount)
                        if coupobj.minimum_amount <= a:
                            print("in min amt",coupobj.minimum_amount)
                            print("in min amt",coupobj.discount_price)
                            disprice = coupobj.discount_price
                            minusvalue=coupobj.discount_price
                            coupstat = True
                            copu=coupon
                            sweetify.success(request,'Coupon applied successfully')
                            print("copu===",copu)
                            print("jjjj",disprice)
                            request.session['acoupon'] = minusvalue
                            request.session['copu'] = copu
                            if 'awallet' in request.session:
                                awalasigned=False
                                awal = request.session.get('wallet')
                                if awalasigned == False:
                                    minusvalue = minusvalue + int(awal)
                                    awalassigned=True
                                    copu=coupon
                            else:
                                minusvalue = coupobj.discount_price
                        else:
                            sweetify.error(request,'Minimum amount is Rs.'+str(coupobj.minimum_amount))
                    else:
                        print("dcsdsasdsdsdsdsadsa")
                        sweetify.error(request,'This Coupon has expired')
                else:
                    minusvalue = 0
                # request.session['acoupon'] = minusvalue
                a=a-minusvalue

            if request.POST.get('redeem_bt'):
                print("redeembt",wall.balance)
                
                inputwall = request.POST.get('inputwall')
                
                if int(inputwall)<=int(wall.balance):
                    a=int(a)-int(inputwall)
                    if 'acoupon' in request.session:
                        minusvalue=request.session.get('acoupon')
                        mvasignd=False
                        coupstat = True
                        print("bbb",disprice)
                        if mvasignd == False:
                            a=a-minusvalue
                            mvasignd=True
                    wall.balance = int(wall.balance)-int(inputwall)
                    request.session['wallet'] = inputwall
                    request.session['awallet'] = a
                    sweetify.success(request,'Successfully redeemed from wallet')
                else:
                    return render(request,'checkout.html',{'cart':cartitems,'total':a,'address':address,'coupstat':coupstat,'subtotal':subtotal,'disprice':disprice,'wallet':wall,'logedin':logedin})
                print("hihi",coupstat)
                return render(request,'checkout.html',{'cart':cartitems,'total':a,'address':address,'coupstat':coupstat,'subtotal':subtotal,'disprice':disprice,'wallet':wall,'logedin':logedin})

            if request.POST.get('checkbt'):
                payment_method=request.POST['payment_method']
                user_id = user.id
                print("gdgfheruiwergh",user_id)
                data1=myusers.objects.get(id=user_id)
                print("hdgsbjgf",data1)
                reg=Payment()
                reg.user=data1
                if payment_method == 'COD':
                    reg.payment_method=payment_method
                    reg.status='pending'
                reg.save()
                data=Order()
                data.user=data1
                data.payment=reg
                selected_address_id=request.POST.get('address')
                print("my",selected_address_id)
                data.address=Address.objects.get(id=1)
                yr = int(datetime.date.today().strftime('%Y'))
                dt = int(datetime.date.today().strftime('%d'))
                mt = int(datetime.date.today().strftime('%m'))
                d = datetime.date(yr,mt,dt)
                current_date = d.strftime("%Y%m%d") #20210305
                data.order_number = current_date + str(data.id)
                if 'awallet' in request.session:
                    a=request.session.get('awallet')
                if 'acoupon' in request.session:
                    minusval=request.session.get('acoupon')
                    a=a-minusval
                    copu = request.session.get('copu')
                    user.applied_coupons = copu
                    user.save()
                print("coupon applied to user")
                data.order_total=a
                data.save()
                data.order_number = current_date + str(data.id)
                data.save()
                for i in cartitems:
                    data2=OrderProduct()
                    data2.order=data
                    data2.payment=reg
                    data2.user=data1
                    data2.product=products.objects.get(id=i.productid.id)
                    data2.quantity=i.quantity
                    data2.product_price=i.productid.price
                    data2.save()
                if 'wallet' in request.session:
                    inputwall = request.session.get('wallet')
                    print('wallet in session')
                else:
                    inputwall = 0
                print("haaaai",inputwall)
                wall.balance = int(wall.balance) - int(inputwall)
                if 'wallet' in request.session:
                    del request.session['wallet']
                if 'awallet' in request.session:
                    del request.session['awallet']
                if 'acoupon' in request.session:
                    del request.session['acoupon']
                wall.save()
                if payment_method == 'paypal':
                    return redirect(payment_methods, reg.pk)

                if payment_method == 'razorpay':
                      return redirect(payment_methods_razorpay, reg.pk)
                
                      print("dfs")   
                return redirect(ordersuccess)
                # elif payment_method == 'paypal':

        else:
            return render(request,'cartlist.html')
    else :
        return redirect('login')
    
    return render(request,'checkout.html',{'cart':cartitems,'total':a,'coupstat':coupstat,'disprice':disprice,'subtotal':subtotal,'address':address,'wallet':wall,'logedin':logedin})



def payment_methods_razorpay(request,id):
    print(id)
    prodid=id
    if 'razorpay_payment_for_order' in request.session:
        del request.session['razorpay_payment_for_order']
    if 'username' in request.session:
        logedin=True
        usrr=request.session.get('username')
        user=myusers.objects.get(username=usrr)
        order = Order.objects.get(payment_id=id)
        a= order.order_total
        client = razorpay.Client(auth=("rzp_test_egd7d17AHLqyoo","EjZKAZ5oGO6M2Jp58MJC4LeF"))

        data = { "amount": a*100, "currency": "INR", "receipt": "order_rcptid_11" }
        payment = client.order.create(data=data)
        # data = { 'amount': a*100, 'currency': 'INR', 'payment_capture':1 }
        # payment = client.order.create ({ 'amount': a*100, 'currency': 'INR', 'payment_capture':1 })
        print("iiii",payment)
        cart = OrderProduct.objects.filter(payment_id=id)
        print("cart 123",cart)
        request.session['razorpay_payment_for_order'] = payment

    return render(request,'razorpay_checkout.html',{'cart':cart,'total':a,'Razorpay_payment_id':id,'order':order,'payment':payment,'logedin':logedin})

@csrf_exempt
def razor_pay(request,id):
    if 'username' in request.session:
        print("dssssssssssssssssssssssssss")
        order = Order.objects.get(payment_id=id)
        userid=request.session.get('username')
        user=myusers.objects.get(username=userid)
        payment=request.session.get('razorpay_payment_for_order')
        pay = Payment.objects.get(id=id)
        pay.payment_method = 'razorpay'
        pay.status = payment['status']
        pay.payment_id = payment['id']
        pay.user = user
        actual_amount=payment['amount']
        actual_amount=actual_amount/100
        pay.amount_paid = actual_amount
        pay.save()
        # Cart.objects.filter(user_id=userid).delete()
    # return render(request,'order_successfully.html')
    return redirect(ordersuccess)

def myorders(request):
    if 'username' in request.session:
        logedin = True
        username=request.session.get('username')
        user=myusers.objects.get(username=username)
        userid=user.id
        order=OrderProduct.objects.filter(user=userid).order_by('-id')
        # order=Order.objects.filter(user=userid).order_by('-created_at')
        realtime = datetime.datetime.now
        
        # print("realtime",int(realtime))
        # for i in order:
        #     ret = i.created_at
        #     if realtime - ret  >= 3:
        #         print("ffffff",ret)
        #     else : 
        #         print("fuv")   
        p = Paginator(order, 4)
        page = request.GET.get('page')
        order = p.get_page(page)
        nums = "a" * order.paginator.num_pages
        return render(request,'myorders.html',{'orders':order,'nums':nums,'logedin':logedin})


def orderman(request):
    orders=OrderProduct.objects.all().order_by('id')
    for i in orders:
        print("fhahaha",i.product.retrn_policy)
    p = Paginator(orders, 10)
    page = request.GET.get('page')
    orders = p.get_page(page)
    nums = "a" * orders.paginator.num_pages
    
    return render (request,'orderman.html',{'datas': orders,'nums':nums,})

def updateproduct(request,id):
    chose_order= OrderProduct.objects.get(id=id)
    status=chose_order.status
    image=chose_order.product.image.url
    productname=chose_order.product.productname
    created=chose_order.created_at
    quantity=chose_order.quantity
    price=chose_order.product.price
    user=chose_order.user.username
    prodid=chose_order.product.id
    ordernumber=chose_order.order.order_number
    
    if request.method == 'POST':
        odstatus=request.POST.get('od_status')
        change=OrderProduct.objects.get(id=id)
        # print("sdsdds",change.order.status)
        # change.order.status=odstatus
        # change.save()
        # test=OrderProduct.order.id
        
        print("dfsd",change.status)
        change.status=odstatus
        change.save()
        return redirect(updateproduct,id)

    return render (request,'orderdetail.html',{'status':status,'image':image,
    'productname':productname,'created':created,'price':price,'quantity':quantity,'user':user,
    'ordernumber':ordernumber,'id':id})


def cancelord(request,id):
    value=OrderProduct.objects.get(id=id)
    value.status="Cancelled"
    value.save()
    return redirect(myorders)

def returnord(request,id):
    value=OrderProduct.objects.get(id=id)
    value.status="Return Requested"
    value.save()
    return redirect(myorders)

@csrf_exempt
def ordersuccess(request):
    if 'username' in request.session:
        username = request.session.get('username')
        user=myusers.objects.get(username=username)

        
        cartitems=cart.objects.filter(userid = user.id)
        print("cartitemssss",cartitems)
        for i in cartitems:
            
            product=i.productid

            print("hahaha",product.stocks)
            print("hihiihi",product.stock_status)
            if int(product.stocks) < 1:
                product.stock_status = False
                product.save()
            else:
                product.stocks = int(product.stocks) - int(i.quantity)
                print("lasthi",product.stocks)       
                product.save()
        
        # product=products.objects.filter(id=cartitems.productid)
        
        cartitems.delete()

        return render(request,'ordersuccess.html')

def payment_methods(request,id):
    print(id)
    if 'username' in request.session:
        cart = OrderProduct.objects.filter(payment_id=id)
        print("cart 123",cart)
        order = Order.objects.get(payment_id=id)
        a= order.order_total
    

    return render(request,'paypal_checkout.html',{'cart':cart,'total':a,'order':order})

def payment_confirm(request,id):
    if 'username' in request.session:
    
        uname = request.session.get('username')
        user=myusers.objects.get(username=uname)

        order = Order.objects.get(payment_id=id)
        body = json.loads(request.body)
        
        pay = Payment.objects.get(id=id)
        pay.payment_id = body['transId']
        pay.payment_method = 'Paypal'
        pay.status = body['status']
        pay.amount_paid = order.order_total
        pay.user = user
        pay.save()

        data={
            'transId': pay.payment_id,
        }
        return JsonResponse(data)

def payment_complete(request):
     return redirect(ordersuccess)

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return



def download(request,id):
    v=OrderProduct.objects.get(id=id)
    print(id)
    mydict={

        'customerName':v.user.firstname,
        'customerEmail':v.user.email,
        'customerMobile':v.user.phonenumber,
        'shipmentAddress':v.order.address.address,
        'orderStatus':v.status,
        'productimage':v.product.image,
        'productName':v.product.productname,
        'productPrice':v.product.price,
        'productDescription':v.product.description,
    }

    return render_to_pdf ('download.html',mydict)

def offerbycategory(request):
    cate = categories.objects.all()
    perc = 0
    if request.POST.get('cate_choice'):
        print("jicked")
        chose_cate = request.POST.get('category')
        disperc = request.POST.get('disperc')
        disprice = request.POST.get('disprice')
        prod = products.objects.filter(catid_id=chose_cate)
        if int(disperc)<=75:

            for i in prod:
                if disperc:
                    a=int(i.price)*int(disperc)/100
                    print("perc sele",disperc)
                    distype="percentage"
                elif disprice:
                    a=disprice
                    print("price sele",disprice)
                    distype="flat"
                else:
                    a=0
                
                i.dis_price = int(i.price) - int(a)
                i.dis_applied = True
                i.dis_price_type = distype
                i.save()
                
                exist = i.dis_proprice
                diis = int(i.price)-int(a)
                if exist:
                    if int(exist) >= int(diis) :
                        i.total_disprice = diis
                        
                        i.save()
                        
                    elif int(exist) <= diis :
                        i.total_disprice=exist
                        i.save()
                else:
                    i.total_disprice = diis
                    i.save()
                # if distype == "percentage":
                #     diperc =  disperc
                # else :
                #     c=int(i.price)
                #     d=int(i.total_disprice)
                #     e=c-d
                #     diperc = e/c*(100)

        else :
            messages.error(request,"offer should be below 75%")  
            return redirect (offerbycategory)          

    # produ=products.objects.filter(dis_price__gte = 0) 
    produ=products.objects.filter(~Q(dis_price = None) ).distinct('category')
    for i in produ:
        print("prrr",i.productname)
        price = int(i.price)
        dis_price = int(i.dis_price)
        print("ddd",price,dis_price)
        print(i.dis_price_type)
        if i.dis_price_type == 'percentage':
            print("if1",i.dis_price_type)
            pr=price - dis_price
            perc = round(pr/price * 100)
            print("worked",perc)
        elif i.dis_price_type == "flat" :
            print("if2",i.dis_price_type)
            perc = price - dis_price
            print('perc',perc)

    
    return render(request,'offerbycategory.html',{'datas':cate,'produ':produ,'perc':perc})

def remove_cate_offer(request,id):
    cate=id
    print('dddddddd',cate)
    prod = products.objects.filter(category=cate)
    for i in prod:
        i.dis_price = None
        i.save()
        if i.dis_proprice:
            i.total_disprice = i.dis_proprice
        else :
            i.total_disprice = None
    return redirect(offerbycategory)

def offerman(request):
    return render(request,'offerman.html')

def productofferlist(request):
    allprod = products.objects.all()
    prod=products.objects.filter(~Q(dis_proprice = None) )
    print(prod)
    for i in prod:
        print(i.productname,i.dis_proprice)
    return render(request,'productofferlist.html',{'prod':prod,'allprod':allprod})



def mywallet(request):
    if 'username' in request.session:
        logedin = True
        user=request.session.get('username')
        user1=myusers.objects.get(username=user)
        userwallet = wallet.objects.get(user = user1)
        return render(request,'mywallet.html',{'userwallet':userwallet,'logedin':logedin})

def downexel(request):
    response = HttpResponse(content_type = 'application/ms-excel')
    response['content-Disposition'] = 'attachment; filename="sales.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Sales Report') #this will generate a file named as sales Report

     # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Order_ID', 'User Id','Amount', ]

    for col_num in range(len(columns)):
        # at 0 row 0 column
        ws.write(row_num, col_num, columns[col_num], font_style)

    
    font_style = xlwt.XFStyle()
    total = 0

    rows = Order.objects.values_list(
        'order_number', 'user', 'order_total')
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

def export_sales_to_pdf(request):
    brand_name = []
    brand_order_count = []
    total_sales = 0
    brand_orders = OrderProduct.objects.filter(ordered=True)
    sales = OrderProduct.objects.filter(status="OutForDeliver").annotate(Count('id'))

    for brand in brand_orders:
        if brand.product.category.title not in brand_name:
            brand_name.append(brand.product.category.title)
            sum_prod = OrderProduct.objects.filter(
            product=brand.product.id).count()
            brand_order_count.append(sum_prod)

    for total_sale in sales:
        total_sales += total_sale.order_total

    template_path = 'exportsalestopdf.html'
    context = {
        'brand_name':brand_name,
        'order_count':brand_order_count,
        'total_amount':total_sales,
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

def order_detail_user(request,id):
    if 'username' in request.session:
        logedin = True
        ordpro = OrderProduct.objects.get(id=id)
        ordd = Order.objects.get(id=ordpro.order_id)
        # print('ccc',ordd.product.productname)
        address = ordd.address
        print("ggggg",ordpro)
        print("ooo",ordd)
        return render(request,'orderdetailuser.html',{'address':address,'ordpro':ordpro,'ordd':ordd,'logedin':logedin})


def cateoffer(request):
     prod = products.objects.all()
     










# def clearofr(request):
#      prod = products.objects.all()