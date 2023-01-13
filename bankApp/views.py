from django.shortcuts import render, redirect, HttpResponse
from .forms import CustomRegisterForm, CustomAccountForm, TransactionForm
from django.contrib.auth import login as auth_login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .decorators import already_loggedin
from django.contrib.auth.forms import AuthenticationForm
from .models import Account
import time
from django.db import transaction
    

# Create your views here.
@login_required(login_url='/login')
def home(request):
    print(request.user.email)
    return render(request, 'main/homepage.html')

@login_required(login_url='/login')
def create_bank_account(request):
    if request.method == "POST":
        form = CustomAccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user_id = request.user
            account.save()
            return redirect('/home')
    else:
        form = CustomAccountForm()
    
    return render(request, 'account/account_signup.html', {"form":form})


# https://dev.to/techschoolguru/how-to-avoid-deadlock-in-db-transaction-queries-order-matter-oh7

@login_required(login_url='/login')
def make_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.user, request.POST)
        if form.is_valid():
            transact = form.save(commit=False)
            sender = transact.from_account
            reciever = transact.to_account
            amount = transact.amount

            confirm_sender = Account.objects.filter(Account_number=sender.Account_number).first()
            print(type(confirm_sender.user_id), type(request.user))
            if(confirm_sender and request.user == confirm_sender.user_id):

                with transaction.atomic():

                    if sender.balance >= amount:
                        if(sender.Account_number > reciever.Account_number):
                            locked_sender = Account.objects.select_for_update().get(Account_number=sender.Account_number)
                            locked_sender.balance = locked_sender.balance - amount
                            locked_sender.save()
                            print("Amount deducted from sender account")
                            time.sleep(5)
                            locked_reciever = Account.objects.select_for_update().get(Account_number=reciever.Account_number)
                            locked_reciever.balance = locked_reciever.balance + amount
                            locked_reciever.save()
                            print("Amount added to reciever account")

                        else:
                            locked_reciever = Account.objects.select_for_update().get(Account_number=reciever.Account_number)
                            locked_reciever.balance = locked_reciever.balance + amount
                            locked_reciever.save()
                            print("Amount added to reciever account")
                            time.sleep(5)
                            locked_sender = Account.objects.select_for_update().get(Account_number=sender.Account_number)
                            locked_sender.balance = locked_sender.balance - amount
                            locked_sender.save()
                            print("Amount deducted from sender account")


                        transact.save()
                        return redirect('/home')

                    else:
                        return HttpResponse("INSUFFICIENT FUNDS")
            else:
                return HttpResponse("REQUEST FROM FALSE USER DETECTED")
        else:
            return HttpResponse("INVALID FORM")
    else:
        form = TransactionForm(request.user)
    
    return render(request, 'account/make-transaction.html', {"form":form})

@already_loggedin(redirect_to='/home')
def sign_up(request):
    
    if request.method == "POST":
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('/home')
    else:
        form = CustomRegisterForm()
    
    return render(request, 'registration/sign-up.html', {"form":form})


@already_loggedin(redirect_to='/home')
def login(request):
    
    if request.method == "POST":
        logform = AuthenticationForm(request, data=request.POST)
        if logform.is_valid():
            user = logform.get_user()
            auth_login(request, user)
            return redirect('/home')
    else:
        logform = AuthenticationForm(request)

    return render(request, 'registration/login.html', {"form":logform, "title":"Login Page"})
        





