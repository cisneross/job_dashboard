from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# responses gop here

def index(request):
    return render(request,'exam/index.html')

def validate(request):
    # Email Validation
    if len(request.POST['first_name']) < 3:
        messages.error(request,'Yo cuh, you need more than 2 characters for first name,letters only')
    if len(request.POST['last_name']) < 3:
        messages.error(request,'Yo cuh, you need more than 2 characters for last name,letters only')
    if len(request.POST['email']) < 1:
        messages.error(request,'Yo cuh, you need more than 1 character for an email')
    if not EMAIL_REGEX.match(request.POST['email']):
        messages.error(request,'Yo cuh, email is not valid!!')
    if len(User.objects.filter(email = request.POST['email'])) > 0:
        messages.error(request, 'Email already in db')
    if len(request.POST['password']) < 8:
        messages.error(request,'Yo cuh, password must be at least 8 characters!!')
    if not request.POST['password'] == request.POST['confirmpw']:
        messages.error(request,'Yo cuh, passwords dont match!!')

    else:
        # password hash
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        correct_hashed_pw = hashed_pw.decode('utf-8')
        usr=User.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],email=request.POST['email'],password=correct_hashed_pw)
        request.session['userID']=usr.id
        print(usr)

    return redirect('/')
# CHecks for email and password upon login
def log(request):
       # Query db
    user = User.objects.filter(email=request.POST['emaillog'])
    print(user)
    # if no match
    if len(user) == 0:
        print("user not in DB")
        messages.error(request,'Invalid Login')
        return redirect('/')
    # if a match
    else:
        # hash it
        matched = bcrypt.checkpw(request.POST['pwlog'].encode(),user[0].password.encode())
        print("matched = " , matched)
        # if they do match
        if matched:
            print("matched!")
            # store user id in session
            request.session['user_id'] = user[0].id
            return redirect('/login')
            # return redirect('/')
            # else error message 
        else:
            print('not matched')
            messages.error(request,'No match')
            return redirect('/')
# Checks if user is signed in renders dashboard
# doesnt do anything log in related(bad name i know)
def login(request):
    # checks if signed in
    if not 'user_id' in request.session:
        messages.error(request,'You must sign in first')

    context ={
        'users': User.objects.get(id=request.session['user_id']),
        # Filter jobs that that aren't in my_jobs
        'jobs': Jobs.objects.filter(my_jobs=None),
        # Finds the Jobs in my_jobs
        'myjobs': Jobs.objects.filter(my_jobs__id=request.session['user_id'])
    }
    return render(request,'exam/jobboard.html',context)
# Checks if signed in, if yes render add pg
def addpg(request):
    # checks if signed in
    if not 'user_id' in request.session:
        messages.error(request,'You must sign in first')
        return redirect('/')
    return render(request,'exam/addjob.html')
# validates and processes all the info for creating a new job
def addp(request):
    # checks if signed in
    if not 'user_id' in request.session:
        messages.error(request,'You must sign in first')
        return redirect('/')
    # validation
    if len(request.POST['title']) < 4:
        messages.error(request,'Aye cuh, you need a longer title')
    if len(request.POST['loc']) < 1:
        messages.error(request,'Aye cuh,location cannot be empty')
    if len(request.POST['desc']) < 11:
        messages.error(request,'Aye cuh, yo description wack(too short)')
    
    # Adds to the DB,Gives success message, redirects to dash 
    else:
        user = User.objects.get(id=request.session['user_id'])
        print(user)
        print(request.POST['title'])
        print(request.POST['desc'])
        print(request.POST['loc'])
        job=Jobs.objects.create(name=request.POST['title'],desc=request.POST['desc'],location=request.POST['loc'],juploader=user)#,my_jobs=user
        print(job)
        messages.success(request,'Succesfully Added Job!')
        return redirect('/login')

    return redirect('/addjob')

def vprocess(request,jid):
    context={
        'job': Jobs.objects.get(id=jid),
    }
    return render(request,'exam/display.html',context)

def logout(request):
    request.session.clear()
    return redirect('/')

def addtomyjobs(request,jid):
    # Grab user and job from DB
    user=User.objects.get(id=request.session['user_id'])
    print(user)
    job=Jobs.objects.get(id=jid)
    print(job)
    # Add to my jobs and return to dash
    job.my_jobs = user
    job.save()
    print(user.all_jobs.all())
    return redirect('/login')
# deletes record in DB
def remove(request,jid):
    # grab records in DB
    job=Jobs.objects.get(id=jid)
    user=User.objects.get(id=request.session['user_id'])
    print(job)
    print(user)
    # remove from my jobs list
    # job.my_jobs.remove(user)
    user.all_jobs.remove(job)
    # Then Delete job from DB and return to dash
    job.delete()
    return redirect('/login')

# deletes a job
def deletejob(request,id):
    # deletes job from left dashboard
    Jobs.objects.get(id=id).delete()
    return redirect('/login')

# Loads up the edit page
def edit(request,id):
    # checks if signed in
    if not 'user_id' in request.session:
        messages.error(request,'You must sign in first')
        return redirect('/')
    job=Jobs.objects.get(id=id)
    context={
        'job': job
    }
    return render(request,'exam/editpg.html',context)

# validates and processes the updated information
def editprocess(request,id):
    # validation
    if len(request.POST['title']) < 4:
        messages.error(request,'Aye cuh, you need a longer title')
    if len(request.POST['loc']) < 1:
        messages.error(request,'Aye cuh,location cannot be empty')
    if len(request.POST['desc']) < 11:
        messages.error(request,'Aye cuh, yo description wack(too short)')
    else:
        job=Jobs.objects.get(id=id)
        job.name=request.POST['title']
        job.location=request.POST['loc']
        job.desc=request.POST['desc']
        job.save()
    return redirect('/login')


