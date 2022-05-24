from django.forms import ModelForm
from .models import Expense, Contact, Subscribe

class ExpenseForm(ModelForm):
    class Meta:
        model = Expense
        fields = '__all__'

class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
        

class SubscribeForm(ModelForm):
    class Meta:
        model = Subscribe
        fields = '__all__'
        