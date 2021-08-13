from django.db import models
from django.utils import timezone

from accounts.models import User

class Currency(models.Model):
    shortcut = models.CharField(max_length=5, unique=True)
    country = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f'{self.country} - {self.shortcut}'

    class Meta:
        verbose_name = 'Currency'
        verbose_name_plural = 'Currencies'
        ordering = ('country',)



class Category(models.Model):
   
    name = models.CharField(max_length=25, unique=True)
    
    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ('name',)


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    title = models.CharField(max_length=30, blank=True)
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    transaction_types=(
        ('E','Expence'),
        ('I','Income')
    )
    type = models.CharField(max_length=1, choices=transaction_types, default='E')
    description = models.CharField(max_length=255, blank=True)
    date = models.DateTimeField(blank=True)
    update_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.date:
            self.date = timezone.now()
        return super(Transaction, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username}, {self.category.name}, {self.currency.shortcut}, {self.amount}'

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'


class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.amount}'    

    class Meta:
        verbose_name = 'Budget'
        verbose_name_plural = 'Budgets'