from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.views import View
from .models import Menu, CartItem, Order, OrderReport
from .forms import SignUpForm
from django.db.models import Sum, F
from django.conf import settings
from xhtml2pdf import pisa



def home(request):
    return render(request, 'home.html')

def menu(request):
    menu_items = Menu.objects.all()
    return render(request, 'menu.html', {'menu_items': menu_items})

@login_required
def add_to_cart(request, item_id):
    menu_item = Menu.objects.get(id=item_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, menu_item=menu_item)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('menu')

@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    subtotal = cart_items.aggregate(total=Sum(F('quantity') * F('menu_item__price')))['total'] or 0
    total = subtotal
    return render(request, 'cart.html', {'cart_items': cart_items, 'subtotal': subtotal, 'total': total})

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)
    cart_item.delete()
    return redirect('cart')



@login_required
def payment(request):
    cart_items = CartItem.objects.filter(user=request.user)
    subtotal = cart_items.aggregate(total=Sum(F('quantity') * F('menu_item__price')))['total'] or 0
    context = {
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
        'subtotal': subtotal,
        'csrf_token': request.COOKIES['csrftoken']
    }
    return render(request, 'payment.html', context)

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

@method_decorator(csrf_exempt, name='dispatch')
class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        customer_name = data.get('name')
        customer_email = data.get('email')
        customer_address = data.get('address')

        cart_items = CartItem.objects.filter(user=request.user)
        amount = sum(item.quantity * item.menu_item.price for item in cart_items)
        YOUR_DOMAIN = "http://localhost:8000"

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'inr',  
                        'product_data': {
                            'name': 'Total Amount',
                        },
                        'unit_amount': int(amount * 100),  
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            customer_email=customer_email,
            billing_address_collection='auto',  
            shipping_address_collection={
                'allowed_countries': ['IN']  
            },
            success_url=YOUR_DOMAIN + '/orderplaced/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
            metadata={
                'customer_name': customer_name,
                'customer_address': customer_address
            }
        )

        return JsonResponse({'id': checkout_session.id})



@login_required
def payment_cancel(request):
    return render(request, 'payment_cancel.html')

@login_required
def order_placed(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if cart_items.exists():
        description = '\n'.join([f"{item.menu_item.item} (x{item.quantity})" for item in cart_items])
        amount = sum(item.quantity * item.menu_item.price for item in cart_items)
        Order.objects.create(user=request.user, description=description, amount=amount)
        OrderReport.objects.create(user=request.user, description=description,amount=amount)
        cart_items.delete()
    return render(request, 'orderplaced.html')

@login_required
def bill(request):
    try:
        latest_order = Order.objects.filter(user=request.user).latest('date', 'time')

        order_items = []
        for item in latest_order.description.split('\n'):
            name, quantity = item.strip().rsplit(' (x', 1)
            order_items.append({
                'name': name.strip(),
                'quantity': int(quantity.strip(')'))  
            })

        context = {
            'order': latest_order,
            'user': request.user,
            'email': request.user.email,
            'order_items': order_items,
        }

        return render(request, 'bill.html', context)
    except Exception as e:
        return HttpResponse(f'An error occurred: {e}', status=500)


@login_required
def invoice_download(request):
    
    latest_order = Order.objects.filter(user=request.user).latest('date', 'time')

    order_items = []
    for item in latest_order.description.split('\n'):
        name, quantity = item.strip().rsplit(' (x', 1)
        order_items.append({
            'name': name.strip(),
            'quantity': int(quantity.strip(')'))  
        })

    context = {
        'order': latest_order,
        'user': request.user,
        'email': request.user.email,
        'order_items': order_items,
    }

    html_string = render_to_string('invoice_download.html', context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="FoodStack_Bill_{latest_order.id}.pdf"'

    pisa_status = pisa.CreatePDF(html_string, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors with the PDF generation', status=500)
    return response


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return render(request, 'registration/logout.html')

def restaurent(request):
    return render(request, 'restaurent.html')

def manage_orders(request):
    msg = ""
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        try:
            order = Order.objects.get(id=order_id)
            if 'cancel_order' in request.POST:
                order.delete()
                msg = "Order cancelled successfully."
            elif 'ready_order' in request.POST:
                order.delete()
                msg = "Order marked as ready for delivery."
        except Order.DoesNotExist:
            msg = "Order not found."
    orders = Order.objects.all()
    return render(request, 'manage_orders.html', {'orders': orders, 'msg': msg})

def update_menu(request):
    msg=""
    if request.method == 'POST':
        try:
            if 'add_item' in request.POST:
                item_name = request.POST.get('itemName')
                item_description = request.POST.get('itemDescription')
                item_price = request.POST.get('itemPrice')
                item_img = request.POST.get('img')
                Menu.objects.create(
                    item=item_name,
                    description=item_description,
                    price=item_price,
                    image_url=item_img
                )
                msg = "New item added to menu."
            elif 'delete_item' in request.POST:
                item_id = request.POST.get('item_id')
                item = Menu.objects.get(id=item_id)
                item.delete()
                msg = "Item removed from the menu."
        except:
            msg = "Updation not successful."
    menu_items = Menu.objects.all()
    return render(request, 'update_menu.html', {'menu_items': menu_items, 'msg': msg})


def report(request):
    msg = ""
    report_data = None

    if request.method == 'POST':
        date = request.POST.get('date')
        try:
            orders = OrderReport.objects.filter(date=date)
            if orders.exists():
                report_data = {
                    'date': date,
                    'orders': orders
                }
            else:
                msg = "No orders found for the selected date."
        except Exception:
            msg = "Something went wrong! Try again later."
           
    return render(request, 'report.html', {'report_data': report_data, 'msg': msg})


def report_download(request, date):
    orders = OrderReport.objects.filter(date=date)
    order_items = list(orders.values('id', 'user__username', 'description', 'amount'))
    report_data = {
        'date': date,
        'order_items': order_items
    }
    
    html_string = render_to_string('report_download.html', report_data)
    
  
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="FoodStack_Report_{date}.pdf"'
  
    pisa_status = pisa.CreatePDF(html_string, dest=response)
    
    if pisa_status.err:
        return HttpResponse('We had some errors with the PDF generation', status=500)
    
    return response
