from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import Product, Order, OrderItem, State, City
from django.contrib.auth.models import User
from datetime import date

# AJAX cart updates
@require_POST
def ajax_update_cart(request):
    pid    = request.POST['product_id']
    action = request.POST['action']
    cart   = request.session.get('cart', {})

    q = cart.get(pid, 0)
    if action in ('add', 'increase'):
        q += 1
    elif action == 'decrease':
        q = max(q - 1, 0)

    if q:
        cart[pid] = q
    else:
        cart.pop(pid, None)

    request.session['cart'] = cart

    # recompute
    product    = get_object_or_404(Product, id=pid)
    subtotal   = product.price * q
    cart_total = sum(
      get_object_or_404(Product, id=p).price * qty
      for p, qty in cart.items()
    )

    return JsonResponse({
      'success':   True,
      'quantity':  q,
      'subtotal':  float(subtotal),
      'cartTotal': float(cart_total),
      'cartCount': sum(cart.values())
    })

def product_list(request):
    return render(request, 'store/product_list.html', {
      'products': Product.objects.all(),
      'cart':     request.session.get('cart', {})
    })

def product_detail(request,product_id):
    return render(request,'store/product_cart.html',{
        'product':get_object_or_404(Product,id=product_id)
    })

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    pid  = str(product_id)
    cart[pid] = cart.get(pid, 0) + 1
    request.session['cart'] = cart

    # AJAX?
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
          'quantity': cart[pid],
          'cartCount': sum(cart.values())
        })
    return redirect('store:product-list')

def view_cart(request):
    cart_items,total,latest=[],0,None
    cart = request.session.get('cart',{})
    for pid,qty in cart.items():
        p = get_object_or_404(Product,id=pid)
        sub=p.price*qty
        cart_items.append({'product':p,'qty':qty,'subtotal':sub})
        total+=sub
        ed=p.estimated_delivery_date
        if not latest or ed>latest: latest=ed
    return render(request,'store/cart.html',{
        'cart_items':cart_items,'total':total,'latest_delivery':latest
    })

def buy_now(request,product_id):
    cart=request.session.get('cart',{})
    pid=str(product_id)
    if pid not in cart: cart[pid]=1
    request.session['cart']=cart
    return redirect('store:cart')

def remove_from_cart(request,product_id):
    cart=request.session.get('cart',{})
    cart.pop(str(product_id),None)
    request.session['cart']=cart
    return redirect('store:cart')

def update_cart(request):
    if request.method=='POST':
        pid,act=str(request.POST['product_id']),request.POST['action']
        cart=request.session.get('cart',{})
        if pid in cart:
            if act=='increase': cart[pid]+=1
            elif act=='decrease':
                if cart[pid]>1: cart[pid]-=1
                else: cart.pop(pid,None)
        request.session['cart']=cart
    return redirect('store:cart')

@login_required
def checkout(request):
    if not request.session.get('cart'): return redirect('store:product-list')
    items,total,latest=[],0,None
    for pid,qty in request.session['cart'].items():
        p=get_object_or_404(Product,id=pid)
        sub=p.price*qty; items.append({'product':p,'qty':qty,'subtotal':sub}); total+=sub
        ed=p.estimated_delivery_date
        if not latest or ed>latest: latest=ed
    states=State.objects.all()
    if request.method=='POST':
        o=Order.objects.create(
          user=request.user,price=total,
          address1=request.POST['address1'],address2=request.POST.get('address2',''),
          city=request.POST['city'],state=request.POST['state'],pincode=request.POST['pincode']
        )
        for it in items:
            OrderItem.objects.create(order=o,product=it['product'],quantity=it['qty'])
        request.session['cart']={}
        return redirect('store:thankyou')
    return render(request,'store/checkout.html',{
        'cart_items':items,'total':total,'latest_delivery':latest,'states':states
    })

@login_required
def thankyou(request):
    return render(request,'store/thankyou.html')

@login_required
def order_history(request):
    raw_orders = Order.objects.filter(user=request.user).order_by('-ordered_at')
    orders = []
    for o in raw_orders:
        items = []
        latest_delivery = None
        for itm in o.items.all():
            sub = itm.product.price * itm.quantity
            items.append({
                'product': itm.product,
                'quantity': itm.quantity,
                'subtotal': sub,
                'estimated_delivery': itm.product.estimated_delivery_date
            })
            ed = itm.product.estimated_delivery_date
            if not latest_delivery or ed > latest_delivery:
                latest_delivery = ed

        orders.append({
            'order': o,
            'items': items,
            'latest_delivery': latest_delivery,
        })

    return render(request, 'store/order_history.html', {
        'orders': orders,
        'today': date.today(),
    })

@login_required
def return_order(request,order_id):
    o=get_object_or_404(Order,id=order_id,user=request.user)
    if request.method=='POST' and o.can_return():
        o.is_returned=True; o.return_reason=request.POST['reason']; o.save()
        messages.success(request,'Return requested')
    return redirect('store:order-history')

def get_cities(request,state_id):
    return JsonResponse({'cities':list(City.objects.filter(state_id=state_id).values('id','name'))})

def register(request):
    if request.method == 'POST':
        uname = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        pwd   = request.POST.get('password', '')
        if not (uname and email and pwd):
            messages.error(request, "All fields are required.")
        elif User.objects.filter(username=uname).exists():
            messages.error(request, "Username already taken.")
        else:
            user = User.objects.create_user(username=uname, password=pwd, email=email)
            messages.success(request, "Registration successful! Please log in.")
            return redirect('store:login')
    return render(request, 'store/register.html')

def user_login(request):
    if request.method=='POST':
        u=authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if u: auth_login(request,u); return redirect('store:product-list')
        messages.error(request,'Invalid credentials')
    return render(request,'store/login.html')

@login_required
def user_logout(request):
    auth_logout(request)
    return redirect('store:login')