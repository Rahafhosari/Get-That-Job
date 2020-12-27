from django.db import models
from datetime import date, datetime
from django.utils import timezone
import re
import bcrypt

class UserManager(models.Manager):
    def register_validator(self, user_info):
        errors = {}
#names
        if (str.isalpha(user_info['first_name'])) == False: #user_info['first_name'] is from the form of registration
            if len(user_info['first_name']) <4 :
                errors["firstname"] = "First Name should be more than 2 characters." #["first_name"] is a key for errors dictionary can be any word
        if (str.isalpha(user_info['last_name'])) == False:
            if len(user_info['last_name']) <4 :
                errors["lastname"] = "Last Name should be more than 2 characters."
#email  
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        new_user = User.objects.filter(email = user_info['email'])
        if not EMAIL_REGEX.match(user_info['email']): #checking if email matches the regex           
            errors['email'] = "Invalid email address!"
        if len(new_user):
            errors['email'] = "Email already exists.. Try another!"
#password
        if len(user_info['password']) < 8:
            errors["password"] = "Password should be at least 8 characters."
        if user_info['password'] != user_info['password_confirm']:
            errors['password_confirm']= "Password Dosent Match!"
#birthday
            now = timezone.now()
            if (user_info['birthday'] > str(now)):
                errors['birthday'] = "Invalid Birth date. Birthday should be in the past"
            today = datetime.now().strftime("%Y%m%d")
            user_birthday = user_info['birthday'].replace("-", "")
            # if len(user_info["birthday"]) > 0 and datetime.strptime(user_info["birthday"], '%Y-%m-%d') >= datetime.today() :
            #     errors["birthday"] = "Invalid Birth date"
            if (int(today[0:4]) - int(user_birthday[0:4])) <= 18:
                errors["birthday"] = "You should be at least 18 years old to register"
        return errors
#Login Validator
    def login_validator(self, user_info):
            errors = {}
            all_user = User.objects.filter(email = user_info['email'])
            EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
            if not EMAIL_REGEX.match(user_info['email']):
                errors['email'] = "Wrong email address!"
            if not len(all_user):
                errors['email'] = "Email not registered! /Wrong Email"
            if len(user_info['password']) < 8:
                errors["password"] = "Password should be 8 characters minimum"
            if len(all_user) and not bcrypt.checkpw(user_info['password'].encode(), all_user[0].password.encode()):
                errors["password"] = "Wrong Password!"
            return errors

#Data_Base Tables
class Role(models.Model):
    name = models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects = UserManager()

class User(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    birthday=models.DateField(null = True)
    education=models.TextField(null=True)
    field_of_experience=models.TextField(null=True)
    image = models.ImageField(upload_to="images/",null=True)
    interests=models.TextField(null=True)
    about=models.TextField(null=True)
    role=models.ForeignKey(Role,related_name='role', on_delete=models.CASCADE,default=2) # foreignkey one to many  user with role
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects = UserManager()
    
class Session (models.Model):
    date=models.DateField()
    period=models.TimeField()
    description=models.TextField()
    user=models.ForeignKey(User,related_name='user_session', on_delete=models.CASCADE) # foreignkey one to many  user with session 
    consultant=models.ForeignKey(User,related_name='consultant_session', on_delete=models.CASCADE)# foreignkey one to many  user with session 
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class Partner(models.Model):
    name=models.CharField(max_length=255)
    field_of_company=models.TextField()
    about=models.TextField()
    image = models.ImageField(upload_to="images/",null=True)
    admin=models.ForeignKey(User,related_name='partner', on_delete=models.CASCADE)# foreignkey one to many user with partner
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects = UserManager()

class Story(models.Model):
    description=models.TextField()
    user=models.ForeignKey(User, on_delete=models.CASCADE)# foreignkey one to one user with story
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

#Database Functions

#Registration
def add_new_user(new_user):
    user = User.objects.filter(email = new_user['email'])
    if len(user) == 0:
        if new_user['password_confirm'] == new_user['password']:
            password = new_user['password']  #hashing user password
            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            user_info = User.objects.create(first_name=new_user['first_name'],last_name=new_user['last_name'],email=new_user['email'],birthday=new_user['birthday'],education=new_user['education'],field_of_experience=new_user['field_expertise'],interests=new_user['interests'],about=new_user['about'])
            new_user_info = {
                        'user_id': user_info.id,
                        'user_role': user_info.role.id,
                        'first_name': user_info.first_name,
                        'last_name': user_info.last_name,
                        'email': user_info.email,
                        }
        return new_user_info
    return False

#Login
def user_login(login_info):
    user_exist = User.objects.filter(email=login_info['email'])
    if len(user_exist):
        password= login_info['password']
        if bcrypt.checkpw(password.encode(), user_exist[0].password.encode()):
            user=user_exist[0]
            new_user_exist={
                'user_id': user.id,
                'user_role': user.role.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
            }
        return new_user_exist
    return False

#Update user information
def edit(user_info,user_id):
    
    User.objects.filter(id=user_id).update(first_name=user_info['first_name'],last_name=user_info['last_name'],email=user_info['email'],birthday=user_info['birthday'],education=user_info['education'],field_of_experience=user_info['field_expertise'],image=user_info['img'],interests=['interests'],about=['about'])

#Show user info on profile
def display(user_id):
    user = User.objects.get(id=user_id)
    context={
        'user_id': user.id,
        'first_name' : user.first_name,
        'last_name' : user.last_name,
        'email' : user.email,
        'birthday':user.birthday,
        'education':user.education,
        'field_of_experience':user.field_of_experience,
        'interests':user.interests,
        'about':user.about,
    }
    return context



#ADMIN PAGE *******************************************
#Displaying Users
def all_users():
    context = {
        "users": User.objects.filter(role = Role.objects.get(id=2)),
        "consultants": User.objects.filter(role = Role.objects.get(id=3)),
        "partners": Partner.objects.all(),
        "admins": User.objects.filter(role = Role.objects.get(id=1)),
        "all_users" : User.objects.all(),

    }
    return context

#Adding Partner (Admin view page)
def add_partner(post_info):
    admin = User.objects.filter(role= Role.objects.get(id=1))
    partners = Partner.objects.create(name=post_info['company_name'],field_of_company=post_info['company_field'],about=post_info['co_about'],image=post_info['co_logo'],admin_id=1)
    return partners
    
    # admin.partner.create(name=post_info['company_name'],field_of_company=post_info['company_field'],about=post_info['co_about'],image=post_info['co_logo'])

def change_user_id(user_info):
    User.objects.filter(email=user_info['user_email']).update(role_id=user_info['user_role'])



#Test
#def all_users():
    #User.objects.all().user.filter(id=2)
#def all_consultants():
    #User.objects.all().user.filter(id=3)
#********************************************************





