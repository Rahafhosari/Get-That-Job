from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from . import models
import json
from django.http import JsonResponse

from .models import Partner

# to view the main page without sign in:
def home(request):
    context = models.all_users()
    return render(request, "home_page.html",context)

# to view the main page after sign in :
def home_in(request):
    if 'term' in request.GET:
        qs = Partner.objects.filter(name__icontains=request.GET.get('term'))
        titles = list()
        for product in qs:
            titles.append(product.name)
        # titles = [product.title for product in qs]
        return JsonResponse(titles, safe=False)
    if 'logged_user_info' in request.session:
        context = models.all_users()
        return render(request, "home_in.html",context)
    return redirect('/')


#to render the registration page
def registration_page(request):
    return render(request,"registration.html")

#to process the user info from registration form (checks for validation) and redirects to Home_in page
def registration(request):
    if request.method == 'POST':
        errors = models.User.objects.register_validator(request.POST) 
        if len(errors) > 0:  
            for key, value in errors.items():
                messages.error(request, value) #show the messages value
            return redirect('/register-page')                                                                   
        else: #if there are no errors >> create new user
                user = models.add_new_user(request.POST)
                request.session['logged_user_info'] = user #session name is new variable
                return redirect('/in')
    return redirect('/register-page') 

#for login 
def log_in(request):
    if request.method =='POST':
        errors = models.User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            user = models.user_login(request.POST)
            request.session['logged_user_info'] = user
            return redirect('/in')
    return redirect('/')

#for logout
def log_out(request):
    del request.session['logged_user_info']
    return redirect('/')

#to view the user's profile 
def profile(request):
    user_context = models.display(request.session['logged_user_info']['user_id'])
    return render(request,"profile.html",user_context)

#updating user information
def edit(request):
    user = request.session['logged_user_info']
    models.edit(request.POST,request.session['logged_user_info']['user_id'])
    return redirect('/profile')

#adding booking
def booking(request):
    context = models.all_users()
    return render(request,'Booking.html',context)



#adding partners
def partner(request):
    return render(request,'partners.html')

#Admin page
def admin(request):
    context = models.all_users()
    if 'logged_user_info' not in request.session:
        return HttpResponse('YOU ARE NOT ADMIN ')
    if not request.session['logged_user_info']['user_role']== 1 :
        return redirect('/in')
    return render(request,'admin.html',context)

def add_partner(request):
    models.add_partner(request.POST)
    return redirect('/admin')

#Admin changes user_id 
def edit_user_id(request):
    models.change_user_id(request.POST)
    return redirect('/admin')


