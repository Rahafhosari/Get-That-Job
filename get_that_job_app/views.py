from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from . import models

# to view the main page without sign in:
def home(request): 
    return render(request, "home_page.html")

# to view the main page after sign in :
def home_in(request):
    if 'logged_user_info' in request.session:
        return render(request, "home_in.html")
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
            return redirect('/home')
        else:
            user = models.user_login(request.POST)
            request.session['logged_user_info'] = user
            return redirect('/in')
    return redirect('/')

#for logout
def log_out(request):
    
    del request.session['logged_user_info']
    return redirect('/')
