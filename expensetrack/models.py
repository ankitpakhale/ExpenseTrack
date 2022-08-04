from django.db import models

# Create your models here.

class SignUp(models.Model):
    name = models.CharField(max_length=30, default='')
    email = models.EmailField(default='')
    number = models.PositiveIntegerField(default='')
    address = models.CharField(max_length=100, default='')
    password = models.CharField(default='', max_length=15)
    def __str__(self):
        return self.name

class Categories(models.Model):
    owner = models.ForeignKey(SignUp, on_delete=models.CASCADE, blank=True, null=True)
    category = models.CharField(max_length=50)
    def __str__(self):
        return self.category

class Expense(models.Model):
    item = models.CharField(max_length=50, null=True, blank=True)
    amount = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    narration = models.CharField(max_length=1000, null=True, blank=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, blank=True, null=True)
    owner = models.ForeignKey(SignUp, on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return self.item

class Contact(models.Model):
    name = models.CharField(max_length=30, default='')
    email = models.EmailField(default='')
    details = models.CharField(max_length=1000, default='')
    def __str__(self):
        return self.name

class Subscribe(models.Model):
    email = models.EmailField(default='')
    def __str__(self):
        return self.email
    
class Faqs(models.Model):
    ques = models.CharField(max_length=50)
    ans = models.CharField(max_length=300)
    def __str__(self):
        return self.ques