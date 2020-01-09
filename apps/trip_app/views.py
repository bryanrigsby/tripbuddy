from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from datetime import datetime

from .models import User, Trip

# Create your views here.
def login_page(request):
    return render(request, 'trip_app/login.html')

def register_page(request):
    return render(request, 'trip_app/register.html')

def register(request):
    if request.method=='POST':
        errors = User.objects.register_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/register_page')
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            print(pw_hash) 
            User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash)
            request.session['email'] = request.POST['email']
            return redirect('/success')

def login(request):
    if request.method=='POST':
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/login_page')
        else:
            user = User.objects.filter(email=request.POST['email']) 
            if user: 
                logged_user = user[0] 
                if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                    request.session['email'] = logged_user.email
                    print(logged_user.email)
                    return redirect('/success')
                else:
                    messages.error(request, 'Password is incorrect')
                    return redirect('/login_page')

            
        
        

def success(request):
    if 'email' in request.session:
        context = {
            'user': User.objects.get(email=request.session['email']),
            'trips': Trip.objects.all(),
        }
        return render(request, 'trip_app/main.html', context)
    else:
        return redirect('/')

def main(request):
    return redirect('/success')
    

def clear(request):
    request.session.clear()
    return redirect('/')

def new(request):
    context = {
            'user': User.objects.get(email=request.session['email']),
    }
    return render(request, 'trip_app/new.html', context)


    
def add_trip(request):
    if request.method=='POST':
        errors = Trip.objects.trip_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/new')
        else:
            #create trip and attach who uploaded it
            this_trip = Trip.objects.create(destination=request.POST['destination'], start_date=request.POST['start_date'], end_date=request.POST['end_date'], plan=request.POST['plan'], uploaded_by=User.objects.get(email=request.session['email']))
            this_user = User.objects.get(email=request.session['email'])
            this_trip.users_who_like.add(this_user)
            return redirect('/success')
    else:
        return redirect('/success')



def trips(request, id):
    if 'email' in request.session:
        context = {
            'user': User.objects.get(email=request.session['email']),
            'trips': Trip.objects.all(),
            'trip': Trip.objects.get(id=id),
        }
        return render(request, 'trip_app/trip.html', context)
    else:
        return redirect('/')
    


def update(request):
    if request.method=='POST':
        this_trip = Trip.objects.get(id=request.POST['update'])
        errors = Trip.objects.trip_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f"/trip/edit/{this_trip.id}")
        else:
            this_trip.destination = request.POST['destination']
            this_trip.start_date = request.POST['start_date']
            this_trip.end_date = request.POST['end_date']
            this_trip.plan = request.POST['plan']
            this_trip.save()
            return redirect(f"/main")
    else:
        return redirect(f"/main")

def delete(request):
    if request.method=='POST':
        this_trip = Trip.objects.get(id=request.POST['delete'])
        this_trip.delete()
        return redirect('/main')
    else:
        return redirect(f"/main")


def edit_page(request, id):
    if 'email' in request.session:
        context = {
            'user': User.objects.get(email=request.session['email']),
            'trips': Trip.objects.all(),
            'trip': Trip.objects.get(id=id),
        }
        return render(request, 'trip_app/edit.html', context)
    else:
        return redirect('/')