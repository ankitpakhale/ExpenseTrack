from django.shortcuts import render, redirect
from .models import Expense
from django.http import HttpResponse
from django.contrib import messages
from . models import *

from django.template.loader import get_template
from xhtml2pdf import pisa
import plotly.graph_objects as go
from io import BytesIO
import plotly.express as px


def home(request):
    expenses = Expense.objects.all()

    labels = []
    values = []

    for i in expenses:
        print(i.amount)
        print(i.item)
        
        labels.append(i.item)
        values.append(i.amount)
    print(labels,"----------::::---------",values)
    
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    a = fig.show()

        
    if request.POST:
        month = request.POST['month']
        year = request.POST['year']
        expenses = Expense.objects.filter(date__year=year, date__month=month)
    return render(request, 'index1.html', {'expenses': expenses, 'a': a})
# -------------------------------------------------------------------------------
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
# -------------------------------------------------------------------------------

def report(request):
    expenses = Expense.objects.all()
    data = {'expenses': expenses}
    pdf = render_to_pdf('GeneratePdf.html', data)
    return HttpResponse(pdf, content_type='application/pdf')
# -------------------------------------------------------------------------------
def add(request):
    if request.method == 'POST':
        item = request.POST['item']
        amount = request.POST['amount']
        category = request.POST['category']
        date = request.POST['date']
        expense = Expense(item=item, amount=amount, category=category, date=date)
        expense.save()
    return redirect(home)


def update(request, id):
    id = int(id)
    expense_fetched = Expense.objects.get(id = id)
    if request.method == 'POST':
        item = request.POST['item']
        amount = request.POST['amount']
        category = request.POST['category']
        date = request.POST['date']

        expense_fetched.item = item
        expense_fetched.amount = amount
        expense_fetched.category = category
        expense_fetched.date = date

        expense_fetched.save()

    return redirect(home)

def delete(request, id):
    id = int(id)
    expense_fetched = Expense.objects.get(id = id)
    expense_fetched.delete()
    return redirect(home)


# ----------------------------------------------------------------

def index(request):
    if 'email' in request.session:
        expenses = Expense.objects.all()
        if request.POST:
            month = request.POST['month']
            year = request.POST['year']
            expenses = Expense.objects.filter(date__year=year, date__month=month) 
        return render(request, 'index.html', {'expenses': expenses})
    return redirect('LOGIN')

    
def about(request):
    if 'email' in request.session:
        return render(request, 'about.html')
    return redirect('LOGIN')

def expense(request):
    if 'email' in request.session:
        return render(request, 'expense.html')
    return redirect('LOGIN')

def contact(request):
    if 'email' in request.session:  
        key = ''
        if request.method == 'POST':
            db = ContactForm(name = request.POST.get('name') ,email = request.POST.get('email'), details = request.POST.get('details'))
            db.save()
            key = "Your Message has been sent successfully"
        return render(request, 'contactus.html', {'msg': key})
    return redirect('LOGIN')


def signup(self):
    if self.POST:
        print('signup')
        FName = self.POST['fname']
        LName = self.POST['lname']
        Email = self.POST['email']
        Password = self.POST['password']
        ConfirmPassword = self.POST['confirmPassword']
        
        try:
            print('try')
            data=SignUp.objects.filter(email=Email)
            if data:
                msg = 'Email already taken'
                return render(self , 'signup.html',{'msg':msg})

            elif ConfirmPassword == Password:
                print('elif')
                v = SignUp()
                v.firstname = FName
                v.lastname = LName
                v.email = Email
                v.password = Password
                v.save()
                return redirect('LOGIN')

            else:
                msg = 'Enter Same Password'
                return render(self , 'signup.html',{'msg':msg}) 
        finally:
            messages.success(self, 'Signup Successfully Done...')
    return render(self,'signup.html')

def login(self):
    if self.POST:
        em = self.POST.get('email')
        pass1 = self.POST.get('password')
        try:
            print("Inside first try block")
            check = SignUp.objects.get(email = em)
            print("Email is ",em,check.email)
            if check.password == pass1:
                # print(check.Password)
                self.session['email'] = check.email
                return redirect('INDEX')
            else:
                msg = 'Invalid Password'
                return render(self , 'login.html',{'msg':msg}) 
                # return HttpResponse('Invalid Password')
        except:
            print("Inside first except block")
            msg = 'Invalid Email ID'
            return render(self , 'login.html',{'msg':msg}) 
            # return HttpResponse('Invalid Email ID')

    return render(self,'login.html')


def userLogOut(request):
    del request.session['email']
    print('User logged out successfully')
    return redirect('LOGIN')


