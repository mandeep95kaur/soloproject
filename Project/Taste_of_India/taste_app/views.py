from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render(request, 'index.html')

def register(request):
    errors = User.objects.register_validator(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode(),
            address = request.POST['address'],
            city = request.POST['city'],
            state = request.POST['state'],
        )
        request.session['user_id'] = user.id
        return redirect('/')

def login(request):
    errors = User.objects.login_validator(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(email=request.POST['login_email'])
        request.session['user_id'] = user.id
        return redirect('/home')

def home(request):
    return render(request, 'home.html')

def edit_user(request, user_id):
    user = User.objects.get(id = user_id)
    
    context = {
        'user': user,
    }
    return render(request,'edit.html' , context)

def update(request):
    errors = User.objects.update_validator(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/home')
    else:
        to_update = User.objects.get(id= request.session['user_id'])
        to_update.first_name=request.POST['first_name']
        to_update.last_name=request.POST['last_name']
        to_update.email= request.POST['email']
        to_update.address= request.POST['address']
        to_update.state= request.POST['state']
        to_update.city= request.POST['city']
        to_update.save()
    return redirect('/home')




def review(request):
    context = {
        'recent_reviews': Review.objects.order_by('created_at').reverse()[:3]
    }
    return render(request, "review.html", context)

def create_review(request):
    review_errors = Review.objects.basic_validator(request.POST)
    if len(review_errors) > 0:
        for k, v in review_errors.items():
            messages.error(request, v)
        return redirect('/reviews')
    else:
        user = User.objects.get(id = request.session['user_id'])
        Review.objects.create(content = request.POST['review'], rating = request.POST['rating'], user = user)
        return redirect('/reviews')

def like_review(request, review_id):
        review = Review.objects.get(id = review_id)
        user = User.objects.get(id= request.session['user_id'])
        liking_review = review.review_by
        liking_review.add(user)
        return redirect('/reviews')

def unlike_review(request, review_id):
        review = Review.objects.get(id = review_id)
        user = User.objects.get(id= request.session['user_id'])
        liking_review = review.review_by
        liking_review.remove(user)
        return redirect('/reviews')


def delete_review(request, review_id):
    review = Review.objects.get(id = review_id)
    if review.user.id == request.session['user_id']:
        review.delete()
    else:
        messages.error(request, "This isn't yours to delete.")
    return redirect('/reviews')

def logout(request):
    request.session.flush()
    return redirect('/')
