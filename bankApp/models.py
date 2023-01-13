from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.
TYPE_CHOICES = (
    ("1", "CURRENT"),
    ("2", "SAVING"),
)


class Account(models.Model):
    Account_number = models.AutoField(primary_key=True)
    Account_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    balance = models.BigIntegerField(default=0)

    def __str__(self):
        return str(self.Account_number)

class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    datetime = models.DateTimeField(default=datetime.now, blank=True)
    amount = models.BigIntegerField(default=0)
    from_account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name='from_acc')
    to_account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name='to_acc')

    def __str__(self):
        return str(self.transaction_id)
