from django.urls import path
from . import views

urlpatterns = [
    path('checkout', views.checkout,name='checkout'),
    path('myorders', views.myorders,name='myorders'),
    path('orderman', views.orderman,name='orderman'),
    path('ordersuccess', views.ordersuccess,name='ordersuccess'),
    path('offerbycategory', views.offerbycategory,name='offerbycategory'),
    path('offerman', views.offerman,name='offerman'),
    path('productofferlist', views.productofferlist,name='productofferlist'),
    path('remove_cate_offer/<id>', views.remove_cate_offer,name='remove_cate_offer'),
    path('mywallet', views.mywallet,name='mywallet'),
    path('payment_methods/<int:id>', views.payment_methods,name='payment_methods'),
    path('payment_confirm/<int:id>', views.payment_confirm,name='payment_confirm'),
    path('payment_complete', views.payment_complete,name='payment_complete'),
    path('downexel', views.downexel,name='downexel'),
    # path('clearofr', views.clearofr,name='clearofr'),
    path('exportsalestopdf', views.export_sales_to_pdf,name='exportsalestopdf'),
    path('payment_methods_razorpay/<int:id>', views.payment_methods_razorpay, name='payment_methods_razorpay'),
    path('razor_pay/<int:id>', views.razor_pay, name='razor_pay'),
    path('updatetproduct/<int:id>', views.updateproduct,name='updateproduct'),
    path('download/<int:id>', views.download,name='download'),
    path('cancelord/<int:id>', views.cancelord,name='cancelord'),
    path('order_detail_user/<int:id>', views.order_detail_user,name='order_detail_user'),
    path('returnord/<int:id>', views.returnord,name='returnord')

]