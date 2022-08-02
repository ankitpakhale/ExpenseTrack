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
        total = 0
        for i in expenses:
            total += int(i.amount)
        print(total)
        data = {
            'expenses': expenses,
            'total': total
            }
        pdf = render_to_pdf('GeneratePdf.html', data)
        cat_name = []
        values = []
        for i in expenses:
            values.append(i.amount)
            cat_name.append(str(i.category))
        fig = go.Figure(data=[go.Pie(labels=cat_name, values=values, hole=.3)])
        fig.show()
        return HttpResponse(pdf, content_type='application/pdf')
    else:
        return redirect('LOGIN')
# -------------------------------------------------------------------------------
def update(request, id):
    id = int(id)
    expense_fetched = Expense.objects.get(id = id)
    
    if request.method == 'POST':
        category = request.POST['category']
        item = request.POST['item']
        amount = request.POST['amount']
        date = request.POST['narration']
        
        expense_fetched.item = item
        expense_fetched.amount = amount
        expense_fetched.category = category
        expense_fetched.date = date
        expense_fetched.save()
    return redirect(ALL_EXPENSE)
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
        # if 'ContactForm' in request.POST:
        name = request.POST.get('name')
        email = request.POST.get('email')
        details = request.POST.get('details')
        db = Contact(name = name, email = email, details = details)
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
    try:
        if request.session['email']:
            del request.session['email']
            print('User logged out successfully')
            return redirect('LOGIN')
    except:
        return redirect('LOGIN')

def base(request):
    if 'email' in request.session:
        name = SignUp.objects.get(email=request.session['email'])
        print(name)
        return render(request, 'base.html', {'name':name})
    return redirect('LOGIN')

# ############################# New Work #################################
def add_category(request):
    if 'email' in request.session:
        email = SignUp.objects.get(email=request.session['email'])
        category_name = request.POST['category_name']
        try:
            data = Categories.objects.get(category = category_name, owner = email)
            print("this category is already in database")
        except:
            Categories.objects.create(category = category_name, owner = email)
            print(category_name," created successfully")
        return redirect('ALL_EXPENSE')
    return redirect('LOGIN')

def add_expense(request):
    if 'email' in request.session:
        email = SignUp.objects.get(email=request.session['email'])
        if request.method == 'POST':           
            expense_cat = request.POST['item_cat']
            expense_name = request.POST['item_name']
            expense_price = request.POST['item_price']
            expense_narr = request.POST['item_narr']
            expense_cat = Categories.objects.filter(owner = email).get(category=expense_cat) 
            Expense.objects.create(
                item = expense_name,
                amount = expense_price, 
                category = expense_cat,
                owner = email,
                narration = expense_narr
            )
            print("expense created successfully")
        return redirect('ALL_EXPENSE')
    return redirect('LOGIN')

def ALL_EXPENSE(request):
    if 'email' in request.session:
        email = SignUp.objects.get(email=request.session['email'])
        all_expense = Expense.objects.filter(owner=email)
        add_category = Categories.objects.filter(owner = email)
        context = {
            'add_category': add_category,
            'all_expense': all_expense,
        }
        return render(request, 'expense.html', context=context)
    return redirect('LOGIN')

def delete(request, id):
    id = int(id)
    expense_fetched = Expense.objects.get(id = id)
    expense_fetched.delete()
    return redirect(ALL_EXPENSE)
