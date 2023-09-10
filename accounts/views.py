from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.exceptions import ValidationError
from .models import UserProfile
from products.models import Product
import re

def signin(request):
    if request.method == 'POST' and 'btnsignin' in request.POST:
        username = request.POST.get('user')
        password = request.POST.get('pass')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if 'rememberme' not in request.POST:
                request.session.set_expiry(0)
            auth.login(request, user)
            #return reverse("pages:home")
        else:
            messages.error(request, 'Username or Password invalid')
        return redirect('accounts:signin')
    else:
        return render(request, 'accounts/signin.html')

def create_user_with_profile(form_data):
    user = User.objects.create_user(
        first_name=form_data['fname'],
        last_name=form_data['lname'],
        email=form_data['email'],
        username=form_data['user'],
        password=form_data['pass']
    )
    
    userprofile = UserProfile.objects.create(
        user=user,
        address=form_data['address'],
        address2=form_data['address2'],
        city=form_data['city'],
        state=form_data['state'],
        zip_number=form_data['zip']
    )
    
    return user

def signup(request):
    if request.method == 'POST' and 'btnsignup' in request.POST:
        required_fields = ['fname', 'lname', 'address', 'address2', 'city', 'state', 'zip', 'email', 'user', 'pass']
        form_data = {field: request.POST.get(field) for field in required_fields}
        form_data['terms'] = request.POST.get('terms')

        if all(form_data.values()) and form_data['terms'] == 'on':
            if User.objects.filter(username=form_data['user']).exists():
                messages.error(request, 'This username already exists')
            else:
                if User.objects.filter(email=form_data['email']).exists():
                    messages.error(request, 'This email has been used')
                else:
                    email_pattern = r"^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$"
                    if re.match(email_pattern, form_data['email']):
                        user = create_user_with_profile(form_data)
                        messages.success(request, 'Your account has been created successfully! 🎉')
                        return redirect('accounts:signin')
                    else:
                        messages.error(request, 'Invalid email')
        else:
            if form_data['terms'] != 'on':
                messages.error(request, 'You must agree to the terms')
                
            elif not all(form_data.values()):
                messages.error(request, 'Check empty fields')
        
        return render(request, 'accounts/signup.html', form_data)
    else:
        return render(request, 'accounts/signup.html')

def profile(request):
    if request.method == 'POST' and 'btnprofile' in request.POST:
        user = request.user
        userprofile = UserProfile.objects.get(user=user)

        form_data = {
            'fname': request.POST.get('fname'),
            'lname': request.POST.get('lname'),
            'address': request.POST.get('address'),
            'address2': request.POST.get('address2'),
            'city': request.POST.get('city'),
            'state': request.POST.get('state'),
            'zip': request.POST.get('zip'),
            'email': user.email,
            'user': user.username,
            'pass': user.password,
        }

        try:
            update_user_profile(user, userprofile, form_data)
            messages.success(request, 'Your data has been changed successfully')
        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error)
        
        return redirect('accounts:profile')
    else:
        if request.user.is_authenticated and not request.user.is_anonymous:
            userprofile = UserProfile.objects.get(user=request.user)
            context = {
                'fname': request.user.first_name,
                'lname': request.user.last_name,
                'address': userprofile.address,
                'address2': userprofile.address2,
                'city': userprofile.city,
                'state': userprofile.state,
                'zip': userprofile.zip_number,
                'email': request.user.email,
                'user': request.user.username,
                'pass': request.user.password
            }
            return render(request, 'accounts/profile.html', context)
        else:
            return redirect('accounts:signin')

def update_user_profile(user, userprofile, form_data):
    user.first_name = form_data['fname']
    user.last_name = form_data['lname']
    user.email = form_data['email']
    user.username = form_data['user']
    
    if not form_data['pass'].startswith('pbkdf2_sha256$'):
        user.set_password(form_data['pass'])
    
    user.full_clean()
    user.save()
    
    userprofile.address = form_data['address']
    userprofile.address2 = form_data['address2']
    userprofile.city = form_data['city']
    userprofile.state = form_data['state']
    userprofile.zip_number = form_data['zip']
    
    userprofile.full_clean()
    userprofile.save()

def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('accounts:signin')

def product_favorite(request, pro_id):
    if request.user.is_authenticated and not request.user.is_anonymous:
        pro_fav = Product.objects.get(pk=pro_id)
        if UserProfile.objects.filter(user=request.user, product_favorites=pro_fav).exists():
            messages.success(request, 'Product already in the favorite list')
        else:
            userprofile = UserProfile.objects.get(user=request.user)
            userprofile.product_favorites.add(pro_fav)
            messages.success(request, 'Product has been favorited')
    else:
        messages.error(request, 'You must be logged in')
    return redirect('/products/' + str(pro_id))

def show_product_favorite(request):
    context=None
    if request.user.is_authenticated and not request.user.is_anonymous:
        userInfo = UserProfile.objects.get(user=request.user)
        product = userInfo.product_favorites.all()
        context = {'product_list':product}
    return render(request, 'products/product_list.html', context)