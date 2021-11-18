from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt
from django.views import View
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q 
from django.http import JsonResponse



class ProductView(View):
    def get(self, request):
        vegetarian = Product.objects.filter(category='V')
        Nonveg = Product.objects.filter(category='N')
        drinks = Product.objects.filter(category='D')
        return render(request,'home.html', {'vegetarian': vegetarian, 'Nonveg': Nonveg, 'drinks': drinks})


class ProductDetailView(View):
    def get(self,request,id):
        product = Product.objects.get(id=id)
        return render(request,'productdetail.html', {'product':product})

def add_to_cart(request):
    user=request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')


def show_cart(request):
    if request.user.is_authenticated:
        user=request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0 
        shipping_amount = 10.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        if cart_product :
            for p in cart_product:
                teampamount=(p.quantity * p.product.price)
                amount += teampamount
                totalamount = amount + shipping_amount
            return render(request, 'addtocart.html', {'carts':cart , 'totalamount':totalamount , 'amount':amount})
        else:
            return render(request, 'emptycart.html')



def buy_now(request):
 return render(request, 'buynow.html')


class ProfileView(View):
    def get(self, request):
        form=CustomerProfileForm()
        return render(request, 'profile.html', {'form':form})

    def post(self,request):
        form= CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=user, name=name, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Congratulations! Profile Update successfully')
        return render(request, 'profile.html', {'form':form})


def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'address.html', {'add':add})

def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'orders.html', {'order_placed': op})

def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 10.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product :
        for p in cart_product:
            teampamount=(p.quantity * p.product.price)
            amount += teampamount
        totalamount = amount + shipping_amount
    return render(request, 'checkout.html', {'add':add, 'totalamount':totalamount, 'cart_items':cart_items})


def payment_done(request):
    user= request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("orders")

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request,'customerregistration.html', {'form':form})
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulation ! Registered successfully')
            form.save()
        return render(request,'customerregistration.html', {'form':form})
        
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c= Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount = 0.0
        shipping_amount = 10.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            teampamount=(p.quantity * p.product.price)
            amount += teampamount
            totalamount = amount + shipping_amount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c= Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount = 0.0
        shipping_amount = 10.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            teampamount=(p.quantity * p.product.price)
            amount += teampamount
            totalamount = amount + shipping_amount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c= Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 10.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            teampamount=(p.quantity * p.product.price)
            amount += teampamount

        data = {
            'amount': amount,
            'totalamount':amount + shipping_amount
        }
        return JsonResponse(data)

def show_review(request):
    context = {
        'recent_reviews': Review.objects.order_by('created_at').reverse()[:3]
    }
    return render(request,'review.html',context)

def create_review(request):
    user = request.user
    review = Review.objects.create(
        content = request.POST['content'],
        rating = request.POST['rating'],
        creater = user,
    )
    return redirect('/reviews')

def like(request, review_id):
        review = Review.objects.get(id=review_id)
        user = request.user
        liking_review = review.review_by
        liking_review.add(user)
        return redirect('/reviews')


def delete(request, review_id):
    review = Review.objects.get(id=review_id)
    review.delete()

    return redirect('/reviews')





