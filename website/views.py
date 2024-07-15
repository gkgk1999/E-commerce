from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import *
from .form import CustomerRegistrationForm, ProfileForm
from django.db.models import Q




def home(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'home.html',locals())

def about(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'about.html',locals())

def contact(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'contact.html',locals())

class CategoryView(View):
    def get(self, request, val):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        category_products = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request, 'category.html', locals())

class CategoryTitle(View):
    def get(self, request, val):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        category_products = Product.objects.filter(title=val)
        title = Product.objects.filter(category=category_products[0].category).values('title')
        return render(request, "category.html", locals())

class ProductDetail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user))
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        product = get_object_or_404(Product, pk=pk)
        return render(request, 'productdetail.html', locals())

class CustomerRegistrationView(View):
    def get(self, request):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        form = CustomerRegistrationForm()
        return render(request, 'register.html', locals())

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! User Registered Successfully")
        else:
            messages.warning(request, "Invalid Input Data!")
        return render(request, 'register.html', locals())

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        form = ProfileForm()
        return render(request, 'profile.html', locals())

    def post(self, request):
        form = ProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            Customer.objects.update_or_create(
                user=user,
                defaults={
                    'name': name,
                    'locality': locality,
                    'city': city,
                    'mobile': mobile,
                    'state': state,
                    'zipcode': zipcode
                }
            )
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
        else:
            messages.warning(request, "Invalid Input Data!")
        return render(request, 'profile.html', locals())

@login_required
def address(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    add = Customer.objects.filter(user=request.user)
    return render(request, 'address.html', locals())

@method_decorator(login_required, name='dispatch')
class updateAddress(View):
    def get(self, request, pk):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        form = ProfileForm()
        return render(request, 'updateaddress.html', locals())

    def post(self, request, pk):
        form = ProfileForm(request.POST)
        if form.is_valid():
            customer = get_object_or_404(Customer, pk=pk, user=request.user)
            customer.name = form.cleaned_data['name']
            customer.locality = form.cleaned_data['locality']
            customer.city = form.cleaned_data['city']
            customer.mobile = form.cleaned_data['mobile']
            customer.state = form.cleaned_data['state']
            customer.zipcode = form.cleaned_data['zipcode']
            customer.save()
            messages.success(request, "Address updated successfully.")
            return redirect('address')
        else:
            messages.warning(request, "Invalid Input Data!")
        return render(request, 'updateaddress.html', locals())

@login_required
def add_to_cart(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    user = request.user
    product_id = request.GET.get('prod_id')
    product = get_object_or_404(Product, id=product_id)
    Cart.objects.create(user=user, product=product)
    return redirect('/cart')

@login_required
def show_cart(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = sum(item.quantity * item.product.discounted_price for item in cart)
    totalamount = amount + 40
    return render(request, 'addtocart.html', locals())

@login_required
def plus_cart(request):
    if request.method == 'GET':
        try:
            totalitem = 0
            if request.user.is_authenticated:
                totalitem = len(Cart.objects.filter(user=request.user))
            prod_id = request.GET['prod_id']
            user = request.user
            cart = Cart.objects.filter(product_id=prod_id, user=user).first()
            if cart:
                cart.quantity += 1
                cart.save()
                cart_items = Cart.objects.filter(user=user)
                amount = sum(item.quantity * item.product.discounted_price for item in cart_items)
                totalamount = amount + 40
                data = {
                    'quantity': cart.quantity,
                    'amount': amount,
                    'totalamount': totalamount,
                    'redirect_url': request.META.get('HTTP_REFERER', '/')
                }
                return JsonResponse(data)
            else:
                return JsonResponse({'error': 'Cart item not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@login_required
def minus_cart(request):
    if request.method == 'GET':
        try:
            totalitem = 0
            if request.user.is_authenticated:
                totalitem = len(Cart.objects.filter(user=request.user))
            prod_id = request.GET['prod_id']
            user = request.user
            cart = Cart.objects.filter(product_id=prod_id, user=user).first()
            if cart:
                if cart.quantity > 1:
                    cart.quantity -= 1
                    cart.save()
                cart_items = Cart.objects.filter(user=user)
                amount = sum(item.quantity * item.product.discounted_price for item in cart_items)
                totalamount = amount + 40
                data = {
                    'quantity': cart.quantity,
                    'amount': amount,
                    'totalamount': totalamount,
                    'redirect_url': request.META.get('HTTP_REFERER', '/')
                }
                return JsonResponse(data)
            else:
                return JsonResponse({'error': 'Cart item not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@login_required
def remove_cart(request):
    if request.method == 'GET':
        totalitem = 0
        if request.user.is_authenticated:
                totalitem = len(Cart.objects.filter(user=request.user))
        prod_id = request.GET.get('prod_id')
        user = request.user
        cart_item = get_object_or_404(Cart, product_id=prod_id, user=user)
        cart_item.delete()
        cart = Cart.objects.filter(user=user)
        amount = sum(item.quantity * item.product.discounted_price for item in cart) if cart.exists() else 0
        totalamount = amount + 40
        data = {
            'amount': amount,
            'totalamount': totalamount,
            'redirect_url': request.META.get('HTTP_REFERER', '/')
        }
        return JsonResponse({'success': True, 'redirect_url': request.META.get('HTTP_REFERER', '/')})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

class checkout(View):
    def get(self, request):
        totalitem = 0
        if request.user.is_authenticated:
                totalitem = len(Cart.objects.filter(user=request.user))
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        amount = sum(item.quantity * item.product.discounted_price for item in cart_items)
        totalamount = amount + 40
        return render(request, 'checkout.html', locals())


def plus_wishlist(request) :
    if request.method == 'GET' :
        prod_id=request.GET[ 'prod_id'] 
        product=Product.objects.get(id=prod_id)
        user = request.user
        Wishlist(user=user, product=product).save()
        data={'message': 'Wishlist Added Successfully',}
        return JsonResponse(data)
    

def minus_wishlist(request) :
    if request.method == 'GET' :
        prod_id=request.GET[ 'prod_id'] 
        product=Product.objects.get(id=prod_id)
        user = request.user
        Wishlist(user=user, product=product).delete()
        data={'message': 'Wishlist Remove Successfully',}
        return JsonResponse(data)    