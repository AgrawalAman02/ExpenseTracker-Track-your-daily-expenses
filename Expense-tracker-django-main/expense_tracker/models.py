from django.db import models
import datetime

class user(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)

    class Meta:
        db_table = "user"
current_datetime = datetime.datetime.now()
class expense(models.Model):
    expense_name = models.CharField(max_length=1000)
    amount = models.DecimalField(max_digits=100  , decimal_places=2)
    user = models.ForeignKey(user, on_delete=models.CASCADE, related_name='expenses')
    username = models.CharField(max_length=1000)
    date = models.DateTimeField(default=current_datetime.strftime("%Y-%m-%d %H:%M:%S"))

    class Meta:
        db_table = "expense"
