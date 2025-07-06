from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from shop.form import CustomUserForm
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import json


def favviewpage(request):
    if request.user.is_authenticated:
        fav = Favourite.objects.filter(user=request.user)
        return render(request, "shop/fav.html", {"fav": fav})
    return redirect("home")

def remove_fav(request, fid):
    if request.user.is_authenticated:
        item = get_object_or_404(Favourite, id=fid, user=request.user)
        item.delete()
    return redirect("favviewpage")

def cart_page(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        return render(request, "shop/cart.html", {"cart": cart})
    return redirect("home")

def remove_cart(request, cid):
    if request.user.is_authenticated:
        cartitem = get_object_or_404(Cart, id=cid, user=request.user)
        cartitem.delete()
    return redirect("cart")

def fav_product(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'Login to Add Favourite'}, status=400)

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            product_id = data.get('pid')
            product = get_object_or_404(Product, id=product_id)

            if Favourite.objects.filter(user=request.user, product_id=product_id).exists():
                return JsonResponse({'status': 'Product Already in Favourite'}, status=200)

            Favourite.objects.create(user=request.user, product_id=product_id)
            return JsonResponse({'status': 'Product Added to Favourite'}, status=200)

        except Exception as e:
            return JsonResponse({'status': 'Error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'Invalid Request'}, status=400)

# ✅ FIXED: Add product to cart
def add_to_cart(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'Login to Add to Cart'}, status=400)

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            product_qty = int(data.get('product_qty', 1))
            product_id = data.get('pid')
            product = get_object_or_404(Product, id=product_id)

            if Cart.objects.filter(user=request.user, product_id=product_id).exists():
                return JsonResponse({'status': 'Product Already in Cart'}, status=200)

            if product.quantity >= product_qty:
                Cart.objects.create(
                    user=request.user,
                    product_id=product_id,
                    product_qty=product_qty
                )
                return JsonResponse({'status': 'Product Added to Cart', 'redirect_url': '/cart/'}, status=200)

            return JsonResponse({'status': 'Product Stock Not Available'}, status=200)

        except Exception as e:
            return JsonResponse({'status': 'Error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'Invalid Request'}, status=400)

# Logout user
def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logged out Successfully")
    return redirect("home")

# Login user
def login_page(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged in Successfully")
            return redirect("home")

        messages.error(request, "Invalid Username or Password")
        return redirect("login")

    return render(request, "shop/login.html")

# Register user
def register(request):
    if request.user.is_authenticated:
        return redirect("home")

    form = CustomUserForm()
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration Successful! You can now login.")
            return redirect('login')

    return render(request, "shop/register.html", {'form': form})

def home(request):
    products = Product.objects.filter(status=0)
    return render(request, "shop/index.html", {"products": products})

# View all categories
def collections(request):
    catagory = Category.objects.filter(status=0)
    return render(request, "shop/collections.html", {"catagory": catagory})

# View products by category name
def collection_by_name(request, name):
    category = get_object_or_404(Category, name=name, status=0)
    products = Product.objects.filter(category=category, status=0)
    return render(request, "shop/collection_products.html", {
        "category": category,
        "products": products
    })

# Product details
def product_details(request, cname, pname):
    category = get_object_or_404(Category, name=cname)
    product = get_object_or_404(Product, category=category, name=pname)
    return render(request, "shop/products/product_details.html", {"product": product})
