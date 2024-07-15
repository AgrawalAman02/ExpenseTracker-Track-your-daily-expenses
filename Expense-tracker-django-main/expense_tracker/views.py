from django.shortcuts import render , redirect , HttpResponse
from expense_tracker.models import *
from django.db.models import Sum
import datetime


### code khrab nahi hojayega  
# Create your views here.
def register(request):
    return render(request , 'register.html')

def regi(request):
    if request.method == 'POST':
        name = request.POST['user_name']
        email = request.POST['user_email']
        password = request.POST['user_pass']

    if len(password) < 8 or not any(char.islower() for char in password) \
                or not any(char.isupper() for char in password) \
                or not any(char.isdigit() for char in password) \
                or not any(char in "!@#$%^&*" for char in password):
            return HttpResponse("Password must contain at least one lowercase letter, one uppercase letter, one number, one special character, and be at least 8 characters long")

    if user.objects.filter(email= email).exists():
        data = {'email' :email , 'message' : "User Already exists Please Login "}
        return render(request , 'login.html' , {'data' : data})

    u = user()
    u.name = name 
    u.email = email
    u.password = password
    u.save()
    exp = expense.objects.filter(user=u)
    return render(request, 'welcome.html', {'u': u, 'expense': exp, 'total': 0})
def login(request):
    return render(request , 'login.html')

def logi(request):
     if request.method == 'POST':
        email = request.POST['user_email']
        password = request.POST['user_pass']
        
        if user.objects.filter(email=email, password=password).exists():
            u = user.objects.get(email=email)
            exp = expense.objects.filter(user=u)
            total_expense = expense.objects.filter(user=u).aggregate(total_amount=Sum('amount'))['total_amount'] or 0
            return render(request, 'welcome.html', {'u': u, 'expense': exp, 'total': total_expense})
        
        data = {'message': "Wrong password or user does not exist."}
        return render(request, 'login.html', {'data': data})

    # If the request method is not POST, redirect to some appropriate URL
     return redirect('')  # You might want to change this redirection to suit your application

def show(request ):
    u = user.objects.all()
    return render(request , 'show.html' , {'db':u})


def addTransaction(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        description = request.POST.get('expense_name')
        amount = request.POST.get('amount')

        u = user.objects.get(email=email)

        if expense.objects.filter(user=u, expense_name=description).exists():
            # If description already exists for the same user
            obj = expense.objects.get(user=u, expense_name=description)
            obj.amount += int(amount)
            obj.save()
        else:
            exp = expense(expense_name=description, amount=amount, user=u)
            exp.save()

        user_obj = user.objects.get(email=email)
        db = expense.objects.filter(user=user_obj).values()
        total_expense = expense.objects.filter(user=user_obj).aggregate(total_amount=Sum('amount'))['total_amount'] or 0

        return render(request, 'welcome.html', {'u': user_obj, 'expense': db, 'total': total_expense})


    # If the request method is not POST, redirect to some appropriate URL
        return redirect('')  # You might want to change this redirection to suit your application


def delete_transaction(request , id):
        u = expense.objects.get(id = id)
        email = u.user.email
        u.delete()
        user_obj = user.objects.get(email=email)
        db = expense.objects.filter(user=user_obj).values()
        total_expense = expense.objects.filter(user=user_obj).aggregate(total_amount=Sum('amount'))['total_amount'] or 0
        return render(request, 'welcome.html', {'u': user_obj, 'expense': db, 'total': total_expense})


current_datetime = datetime.datetime.now() # get's the latest date and time

def editTransaction(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        email = request.POST.get('email')
        description = request.POST.get('description')
        amount = request.POST.get('amount')

        to_change = expense.objects.get(id=id)
        user_data = user.objects.get(email=email)

        print(f'Data to be changed')
        print(f'\nName: {to_change.expense_name}')
        print(f'\nAmount : {to_change.amount}')

        if expense.objects.filter(user=user_data, expense_name=description).exists():
            obj = expense.objects.get(user=user_data, expense_name=description)
            obj.amount = float(obj.amount) + float(amount)
            obj.save()
           # to_change.delete() all errors are here
        else:
            to_change.amount = float(amount)
            to_change.expense_name = description
            to_change.save()

        db = expense.objects.filter(user=user_data).values()  # get all the entries for user with email = email ez
        total = expense.objects.filter(user=user_data).aggregate(total_amount=Sum('amount'))['total_amount']

        context = {'u': user_data, 'expense': db, 'total': total}
        return render(request, 'welcome.html', context)
    else:
        pass

def edit_profile(request,email):
    u = user.objects.get(email=email)
    return render(request,'edit_profile.html',{'u':u})

def update_profile(request, email):
    if request.method == 'POST':
        new_name = request.POST.get('new_name')
        new_email = request.POST.get('new_email')
        new_pass = request.POST.get('new_pass')
        # Fetch the user based on the provided email
        u = user.objects.get(email=new_email)
        # Update the user's details
        u.name = new_name  # Update to user.name
        u.email = new_email
        u.password = new_pass
        u.save()
        return redirect('login')
  # Redirect to profile or any other URL after update
    else:
        return redirect('edit_profile', email=email)  # Redirect if not a POST request