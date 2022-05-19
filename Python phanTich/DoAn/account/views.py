from cart.models import Cart, CartItem
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages, auth
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate

from .forms import RegistrationForm, UserForm, UserProfileForm
from order.models import Order, OrderProduct
from .models import Account, UserProfile
from cart.views import _cart_id

import requests


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = email.split('@')[0]

            user = Account.objects.create_user(
                first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()

            current_site = get_current_site(request=request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('accounts/active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            send_email = EmailMessage(mail_subject, message, to=[email])
            send_email.send()
            messages.success(
                request=request,
                message="Vui lòng xác nhận email để hoàn tất đăng ký!"
            )
            return redirect('register')
        else:
            messages.error(request=request, message="Đăng ký thất bại!")
    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)


def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                cart_items = CartItem.objects.filter(cart=cart)
                if cart_items.exists():
                    product_variation = []
                    for cart_item in cart_items:
                        variations = cart_item.variations.all()
                        product_variation.append(list(variations))
                        # cart_item.user = user
                        # cart_item.save()
                    cart_items = CartItem.objects.filter(user=user)
                    existing_variation_list = [list(item.variations.all()) for item in cart_items]
                    id = [item.id for item in cart_items]

                    for product in product_variation:
                        if product in existing_variation_list:
                            index = existing_variation_list.index(product)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_items = CartItem.objects.filter(cart=cart)
                            for item in cart_items:
                                item.user = user
                                item.save()
            except Exception:
                pass
            auth.login(request=request, user=user)
            messages.success(request=request, message="Đăng nhập thành công")

            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split("=") for x in query.split("&"))
                if "next" in params:
                    next_page = params["next"]
                    return redirect(next_page)
            except Exception:
                return redirect('dashboard')
        else:
            messages.error(request=request, message="Đăng nhập thất bại!")
    context = {
        'email': email if 'email' in locals() else '',
        'password': password if 'password' in locals() else '',
    }
    return render(request, 'accounts/login.html', context=context)


@login_required(login_url="login")
def logout(request):
    auth.logout(request)
    messages.success(request=request, message="Bạn đã đăng xuất!")
    return redirect('login')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account.objects.get(pk=uid)
    except Exception:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request=request, message="Tài khoản của bạn đã được kích hoạt, vui lòng đăng nhập!")
        return render(request, 'accounts/login.html')
    else:
        messages.error(request=request, message="Link xác nhận không tồn tại!")
        return redirect('home')


@login_required(login_url="login")
def dashboard(request):
    orders = Order.objects.order_by('-created_at').filter(user=request.user, is_ordered=True)
    orders_count = orders.count()

    #user_profile = UserProfile.objects.get(user_id=request.user.id)

    context = {
        'orders_count': orders_count,
       # 'user_profile': user_profile,
    }
    return render(request, 'accounts/dashboard.html', context=context)

@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    context = {
        'orders': orders
    }
    return render(request, 'order/my_orders.html', context=context)

def order_detail(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    subtotal = 0
    for i in order_detail:
        subtotal += i.product_price * i.quantity

    context = {
        'order_detail': order_detail,
        'order': order,
        'subtotal': subtotal,
    }
    return render(request, 'order/order_detail.html', context)

@login_required(login_url='login')
def edit_profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Thông tin của bạn đã được cập nhật')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'user_profile': user_profile,
    }
    return render(request, 'accounts/edit_profile.html', context=context)