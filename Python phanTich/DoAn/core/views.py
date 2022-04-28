from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from customer.models import Customers
from product.models import Products, Category
from django.views import View

# Create your views here.
class ShopView(View):
    def post(self, request):
        product = request.POST.get('product')
        cart = request.session.get('cart')
    def get(self, request):
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        products = None
        categories = Category.get_all_categories()
        categoryID = request.GET.get('product.models.Category')
        customers = Customers.get_all_customers()
        if categoryID:
            products = Products.get_all_products_by_categoryid(categoryID)
        else:
            products = Products.get_all_products();

        data = {}
        data['products'] = products
        data['categories'] = categories
        data['customers'] = customers
        return render(request, 'store/store.html', data)
class HomeView(View):
    def post(self, request):
        product = request.POST.get('product')
        cart = request.session.get('cart')
    def get(self , request):
        return HttpResponseRedirect(f'/home{request.get_full_path()[1:]}')

def home(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('product.models.Category')
    customers = Customers.get_all_customers()
    if categoryID:
        products = Products.get_all_products_by_categoryid(categoryID)
    else:
        products = Products.get_all_products();

    data = {}
    data['products'] = products
    data['categories'] = categories
    data['customers'] = customers

    return render(request, 'homepage/index.html', data)

class Login(View):
    return_url = None

    def get(self, request):
        Login.return_url = request.GET.get ('return_url')
        return render(request, 'login/login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customers.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id
                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('homepage')
            else:
                error_message = 'Mật khẩu sai !!'
        else:
            error_message = 'Không tồn tại tài khoản !!'

        return render(request, 'login/login.html', {'error': error_message})

def logout(request):
    request.session.clear()
    return redirect('homepage')
class Signup(View):
    def get(self, request):
        return render(request, 'signup/signup.html')

    def post(self, request):
        postData = request.POST
        first_name = postData.get ('firstname')
        last_name = postData.get ('lastname')
        phone = postData.get ('phone')
        email = postData.get ('email')
        password = postData.get ('password')
        # validation
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }
        error_message = None

        customer = Customers(first_name=first_name,
                             last_name=last_name,
                             phone=phone,
                             email=email,
                             password=password)
        error_message = self.validateCustomer(customer)

        if not error_message:
            customer.password = make_password(customer.password)
            customer.register()
            return redirect('homepage')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return redirect('homepage')

    def validateCustomer(self, customer):
        error_message = None
        if (not customer.first_name):
            error_message = "Vui lòng nhập Họ của bạn."
        elif (not customer.last_name):
            error_message = 'Vui lòng nhập Tên của bạn.'
        elif (not customer.phone):
            error_message = 'Vui lòng nhập số điện thoại.'
        elif not 10 <= len(customer.phone) <= 15:
            error_message = 'Số điện thoại không hợp lệ.'
        elif len (customer.password) < 5:
            error_message = 'Mật khẩu phải có độ dài hơn 5 ký tự'
        elif len (customer.email) < 5:
            error_message = 'Địa chỉ Email không hợp lệ.'
        elif customer.isExists ():
            error_message = 'Tài khoản Email này đã tồn tại !!!'
        # saving

        return error_message