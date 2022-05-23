import re
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
    if 'email' in request.session:
        print("---------------Home---------------")
        email = SignUp.objects.get(email=request.session['email'])
        expenses = Expense.objects.filter(owner = email)
        if request.POST:
            month = request.POST['month']
            year = request.POST['year']
            expenses = Expense.objects.filter(date__year=year, date__month=month)
        return render(request, 'index1.html', {'expenses': expenses})
    else:
        return redirect('LOGIN')   
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
def myreport(request):
    if 'email' in request.session:
        email = SignUp.objects.get(email=request.session['email'])
        expenses = Expense.objects.filter(owner = email)
        data = {'expenses': expenses}
        pdf = render_to_pdf('GeneratePdf.html', data)
        labels = []
        values = []
        for i in expenses:
            print(i.amount)
            print(i.item)
            
            labels.append(i.item)
            values.append(i.amount)
        print(labels,"----------::::---------",values)
        
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
        fig.show()

        return HttpResponse(pdf, content_type='application/pdf')
    else:
        return redirect('LOGIN')

def report(request):
    expenses = Expense.objects.all()
    data = {'expenses': expenses}
    pdf = render_to_pdf('GeneratePdf.html', data)

    labels = []
    values = []

    for i in expenses:
        print(i.amount)
        print(i.item)
        
        labels.append(i.item)
        values.append(i.amount)
    print(labels,"----------::::---------",values)
    
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    fig.show()

    return HttpResponse(pdf, content_type='application/pdf')
# -------------------------------------------------------------------------------
def add(request):
    if 'email' in request.session:
        print("00")
        email = SignUp.objects.get(email=request.session['email'])
        print("01")
        if request.method == 'POST':
            print("02")
            item = request.POST['item']
            amount = request.POST['amount']
            category = request.POST['category']
            date = request.POST['date']
            expense = Expense(item=item, amount=amount, category=category, date=date, owner = email)
            print("03")
            expense.save()
            print("04")
        return redirect('index')
    else:
        print("05")
        return redirect('LOGIN')

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
    msg =  ''
    if request.POST:
        email = request.POST['email']
        try:
            data = Subscribe.objects.get(email=email)
            if data:
                msg = f"{email} is Already Subscribed for our updates"
                print(msg)
                return render(request, 'index.html', {'msg': msg})
        except:
            sub = Subscribe(email=email)
            sub.save()
            msg = f"{email} have successfully Subscribed for our updates"
            print(msg)
            return render(request, 'index.html', {'msg': msg})
    return render(request, 'index.html', {'msg': msg})
# ----------------------------------------------------------------------

def innerpage(request):
    return render(request, 'inner-page.html')

def portfolio(request):
    return render(request, 'portfolio.html')

def portfoliodetails(request):
    return render(request, 'portfolio-details.html')

def pricing(request):
    return render(request, 'pricing.html')

def services(request):
    return render(request, 'services.html')

def faq(request):
    return render(request, 'faq.html')

def team(request):
    return render(request, 'team.html')

def testimonials(request):
    return render(request, 'testimonials.html')


# ----------------------------------------------------------------------

def about(request):
    return render(request, 'about.html')

    
def elements(request):
    return render(request, 'elements.html')


def contact(request):
    key = ''
    if request.method == 'POST':
        db = ContactForm(
            name = request.POST.get('name') ,
            email = request.POST.get('email'), 
            details = request.POST.get('details'))
        db.save()
        key = "Your Message has been sent successfully"
    return render(request, 'contact.html', {'msg': key})


def signup(self):
    if self.POST:
        print('signup')
        name = self.POST['name']
        email = self.POST['email']
        number = self.POST['number']
        address = self.POST['address']
        password = self.POST['password']
        confirmPassword = self.POST['confirmPassword']
        
        try:
            print('try')
            data=SignUp.objects.get(email=email)
            if data:
                msg = 'Email already taken'
                return render(self , 'signup.html',{'msg':msg}) 
        except:
            if confirmPassword == password:
                print('elif')
                v = SignUp()
                v.name = name
                v.email = email
                v.number = number
                v.address = address
                v.password = password
                v.save()
                msg = f'{name} has Successfully Signed up'
                return render(self , 'signup.html',{'msg':msg})
            else:
                msg = 'Enter Same Password'
                return render(self , 'signup.html',{'msg':msg})
    return render(self,'signup.html')

def login(self):
    if self.POST:
        em = self.POST.get('email')
        pass1 = self.POST.get('password')
        try:
            print("Inside first try block")
            check = SignUp.objects.get(email = em)
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

def base(request):
    if 'email' in request.session:
        name = SignUp.objects.get(email=request.session['email'])
        print(name)
        return render(request, 'base.html', {'name':name})
    return redirect('LOGIN')

def category(request):
    if 'email' in request.session:
        if request.POST:
            cat_name = request.POST['cat_name']
            if cat_name == None:
                msg = f'You can not enter blank category '
                return render(request, 'categories.html', {'msg':msg})
            else:    
                try:
                    data = Categories.objects.get(category = cat_name)
                    if data:
                        msg = f'{cat_name} Category Already Exists'
                        return render(request, 'categories.html', {'msg':msg})
                except:
                    Categories.objects.create(category = cat_name)
                    msg = f'{cat_name} category created successfully'
                    print(msg)
                    return render(request, 'categories.html', {'msg':msg})
        return render(request, 'categories.html')
    return redirect('LOGIN')


def expense(request):
    if 'email' in request.session:
        category = Categories.objects.all()
        allexpense = Expense.objects.all()
        total = 0
        for i in allexpense:
            total += i.amount
        if request.POST.get('delete')=='delete':
            print("This is inside the delete func")
            
        if request.POST.get('edit')=='edit':
            print("This is inside the EDIT func")

        if request.POST.get('adddata')=='adddata':
            item_name = request.POST['item_name']
            item_amount = request.POST['item_amount']
            item_category = request.POST['item_category']
            item_date = request.POST['item_date']
            
            category_name = Categories.objects.get(category = item_category)
            email = SignUp.objects.get(email=request.session['email'])
            expense = Expense(
                item = item_name,
                amount = item_amount,
                category = category_name,
                date = item_date,
                owner = email
            )
            expense.save()
            msg = "Expense properly saved"
            return render(request, 'expense.html', {'msg': msg, 'category': category, 'allexpense': allexpense, 'total':total})
        return render(request, 'expense.html', {'category': category, 'allexpense': allexpense,'total':total})
    return redirect('LOGIN')




