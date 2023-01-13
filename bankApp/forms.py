from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Account, Transaction
from django.db.models import Q

class CustomRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.IntegerField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "phone", "password1", "password2"]


class CustomAccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["Account_type", "balance"]
        # exclude = ()

class TransactionForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.fields['from_account'].queryset = Account.objects.filter(user_id=user)
        self.fields['to_account'].queryset = Account.objects.filter(~Q(user_id=user))


    
    class Meta:
        model = Transaction
        fields = ["from_account", "to_account", "amount"]
        # exclude = ()

# class ClientForm(forms.ModelForm):
#     def __init__(self,company,*args,**kwargs):
#         super (ClientForm,self ).__init__(*args,**kwargs) # populates the post
#         self.fields['rate'].queryset = Rate.objects.filter(company=company)
#         self.fields['client'].queryset = Client.objects.filter(company=company)

#     class Meta:
#         model = Client