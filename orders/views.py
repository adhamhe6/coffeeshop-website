from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from products.models import Product
from .models import Order, OrderDetails, Payment
from django.utils import timezone

def add_to_cart(request):
    if 'qty' in request.GET and 'product_id' in request.GET and 'price' in request.GET and request.user.is_authenticated and not request.user.is_anonymous:
        product_id = request.GET['product_id']
        qty = request.GET['qty']
        order = Order.objects.all().filter(user=request.user, is_finished=False)
        if not Product.objects.all().filter(id=product_id).exists():
            return redirect(reverse('products:product-list'))
        product = Product.objects.get(id=product_id)
        if order:
            if int(qty)>=1:
                #messages.success(request, 'there is an old order')
                old_order = Order.objects.get(user=request.user, is_finished=False)
                if OrderDetails.objects.all().filter(order=old_order, product=product).exists():
                    orderdetails = OrderDetails.objects.get(order=old_order, product=product)
                    orderdetails.quantity += int(qty)
                    orderdetails.save()
                else:
                    orderdetails = OrderDetails.objects.create(product=product, order=old_order, price=product.price, quantity=qty)
                messages.success(request, 'Added to cart for old order')
            else:
                messages.error(request, 'Enter a valid Number!')
        else:
            if int(qty)>=1:
                #messages.success(request, 'there is a new order')
                new_order = Order()
                new_order.user = request.user
                new_order.order_date = timezone.now()
                new_order.is_finished = False
                new_order.save()
                orderdetails = OrderDetails.objects.create(product=product, order=new_order, price=product.price, quantity=qty)
                messages.success(request, 'Added to cart for new order')
            else:
                messages.error(request, 'Enter a valid Number!')
        return redirect('/products/' + request.GET['product_id'])
    else:
        if 'product_id' in request.GET:
            messages.error(request, 'You must be Logged in!')
            return redirect('/products/' + request.GET['product_id'])
        else:
            return redirect(reverse('pages:home'))
def cart(request):
    context = None
    if request.user.is_authenticated and not request.user.is_anonymous:
        if Order.objects.all().filter(user=request.user, is_finished=False):
            order = Order.objects.get(user=request.user, is_finished=False)
            orderdetails = OrderDetails.objects.all().filter(order=order)
            total = 0
            for sub in orderdetails:
                total += sub.price * sub.quantity
            context = {
                'order':order,
                'orderdetails':orderdetails,
                'total':total,
            }
    return render(request, 'orders/cart.html', context)
def remove_from_cart(request, orderdetails_id):
    if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
        orderdetails = OrderDetails.objects.get(id=orderdetails_id)
        if request.user.id == orderdetails.order.user.id:
            orderdetails.delete()
    return redirect(reverse('orders:cart'))
def add_qty(request, orderdetails_id):
    if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
        orderdetails = OrderDetails.objects.get(id=orderdetails_id)
        if request.user.id == orderdetails.order.user.id:
            orderdetails.quantity += 1
            orderdetails.save()
    return redirect(reverse('orders:cart'))
def sub_qty(request, orderdetails_id):
    if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
        orderdetails = OrderDetails.objects.get(id=orderdetails_id)
        if request.user.id == orderdetails.order.user.id:
            if orderdetails.quantity > 1:
                orderdetails.quantity -= 1
                orderdetails.save()
    return redirect(reverse('orders:cart'))
def payment(request):
    context = None
    ship_address = None
    ship_phone = None
    card_number = None
    expire = None
    security_code = None
    if request.method == 'POST' and 'btnpayment' in request.POST and 'ship_address' in request.POST and 'ship_phone' in request.POST and 'card_number' in request.POST and 'expire' in request.POST and 'security_code' in request.POST:
        ship_address = request.POST['ship_address']
        ship_phone = request.POST['ship_phone']
        card_number = request.POST['card_number']
        expire = request.POST['expire']
        security_code = request.POST['security_code']
        if request.user.is_authenticated and not request.user.is_anonymous:
            if Order.objects.all().filter(user=request.user, is_finished=False):
                order = Order.objects.get(user=request.user, is_finished=False)
                payment = Payment(order=order, shipment_address=ship_address, shipment_phone=ship_phone, card_number=card_number, expire=expire, security_code=security_code)
                payment.save()
                order.is_finished = True
                order.save()
                messages.success(request, "Your Order is finished!")
        context = {
            'ship_address':ship_address,
            'ship_phone':ship_phone,
            'card_number':card_number,
            'expire':expire,
            'security_code':security_code,
        }
    else:
        if request.user.is_authenticated and not request.user.is_anonymous:
            if Order.objects.all().filter(user=request.user, is_finished=False):
                order = Order.objects.get(user=request.user, is_finished=False)
                orderdetails = OrderDetails.objects.all().filter(order=order)
                total = 0
                for sub in orderdetails:
                    total += sub.price * sub.quantity
                context = {
                    'order':order,
                    'orderdetails':orderdetails,
                    'total':total,
                }
    return render(request, 'orders/payment.html', context)
def show_orders(request):
    context = None
    all_orders = None
    if request.user.is_authenticated and not request.user.is_anonymous:
        all_orders = Order.objects.all().filter(user=request.user)
        if all_orders:
            for x in all_orders:
                order = Order.objects.get(id=x.id)
                orderdetails = OrderDetails.objects.all().filter(order=order)
                total = 0
                for sub in orderdetails:
                    total += sub.price * sub.quantity
                x.total = total
                x.items_count = orderdetails.count
    context = {'all_orders':all_orders}
    return render(request, 'orders/show_orders.html', context)