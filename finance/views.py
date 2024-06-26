from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import *

from django.template.loader import get_template
from xhtml2pdf import pisa
import plotly.graph_objects as go
from io import BytesIO
from datetime import datetime, timedelta

# Create your views here.

def render_to_pdf(template_src, context_dict=None):
    if context_dict is None:
        context_dict = {}
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    return None if pdf.err else HttpResponse(result.getvalue(), content_type='application/pdf')

def generate_report(request):
    if 'email' not in request.session:
        return redirect('LOGIN')
    email = SignUp.objects.get(email=request.session['email'])
    expenses = Expense.objects.filter(owner=email)
    total = sum(int(i.amount) for i in expenses)
    data = {'expenses': expenses, 'total': total}
    pdf = render_to_pdf('GeneratePdf.html', data)
    cat_name = []
    values = []
    for i in expenses:
        values.append(i.amount)
        cat_name.append(str(i.category))
    fig = go.Figure(data=[go.Pie(labels=cat_name, values=values, hole=0.3)])
    fig.show()
    return HttpResponse(pdf, content_type='application/pdf')

def index(request):
    msg = ''
    if request.POST:
        email = request.POST['email']
        try:
            if data := Subscribe.objects.get(email=email):
                msg = f"{email} is Already Subscribed for our updates"
                print(msg)
                return render(request, 'index.html', {'msg': msg})
        except Exception:
            sub = Subscribe(email=email)
            sub.save()
            msg = f"{email} have successfully Subscribed for our updates"
            print(msg)
            return render(request, 'index.html', {'msg': msg})
    return render(request, 'index.html', {'msg': msg})
# ----------------------------------------------------------------------

def innerpage(request):
    return render(request, 'inner-page.html')

# def portfolio(request):
#     return render(request, 'portfolio.html')

# def portfoliodetails(request):
#     return render(request, 'portfolio-details.html')

# def pricing(request):
#     return render(request, 'pricing.html')

# def services(request):
#     return render(request, 'services.html')

def faq(request):
    return render(request, 'faq.html')

# def team(request):
#     return render(request, 'team.html')

# def testimonials(request):
#     return render(request, 'testimonials.html')

# def about(request):
#     return render(request, 'about.html')

# def elements(request):
#     return render(request, 'elements.html')

def contact(request):
    key = ''
    print('00')
    if request.method == 'POST':
        print('01')
        if 'contact' in request.POST:
            print('02')
            name = request.POST.get('name')
            email = request.POST.get('email')
            details = request.POST.get('details')
            print(name, email, details)
            db = Contact(name = name, email = email, details = details)
            db.save()
            key = "Your Message has been sent successfully"
        elif 'subs' in request.POST:
            email = request.POST.get('email')
            print(email)
            Subscribe.objects.create(email=email)
            key = 'You have successfully subscribed for our latest updates'
        print(key)
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
            if SignUp.objects.get(email=email):
                msg = 'Email already taken'
                return render(self, 'signup.html', {'msg': msg})
        except Exception:
            if confirmPassword == password:
                SignUp.objects.create(
                    name = name,
                    email = email,
                    number = number,
                    address = address,
                    password = password)
                msg = f'{name} has Successfully Signed up'
            else:
                msg = 'Enter Same Password'
            return render(self, 'signup.html', {'msg': msg})
    return render(self, 'signup.html')

def login(self):
    if self.POST:
        em = self.POST.get('email')
        pass1 = self.POST.get('password')
        try:
            check = SignUp.objects.get(email=em)
            if check.password != pass1:
                return render(self, 'login.html', {'msg': 'Invalid Password'})
            self.session['email'] = check.email
            return redirect('INDEX')
        except Exception:
            return render(self, 'login.html', {'msg': 'Invalid Email ID'})
    return render(self, 'login.html')

def user_log_out(request):
    try:
        if request.session['email']:
            del request.session['email']
            print('User logged out successfully')
            return redirect('LOGIN')
    except Exception:
        return redirect('LOGIN')

def add_category(request):
    if 'email' not in request.session:
        return redirect('LOGIN')
    email = SignUp.objects.get(email=request.session['email'])
    category_name = request.POST['category_name']
    try:
        data = Categories.objects.get(category = category_name, owner = email)
    except Exception:
        Categories.objects.create(category = category_name, owner = email)
    return redirect('all_expense')

def all_expense(request):
    if 'email' not in request.session:
        return redirect('LOGIN')

    msg = ''
    email = SignUp.objects.get(email=request.session['email'])
    all_expense = Expense.objects.filter(owner__email=request.session['email']).filter(is_delete = False).order_by('-entry_date')
    add_category = Categories.objects.filter(owner__email=request.session['email'])
    if request.method == 'POST':
        if request.POST.get('add_entry'):
            expense_cat = request.POST['item_cat']
            expense_name = request.POST['item_name']
            expense_price = request.POST['item_price']
            expense_date = request.POST['item_date']
            expense_narr = request.POST['item_narr']
            expense_cat = Categories.objects.filter(owner__email=request.session['email']).get(category=expense_cat)
            Expense.objects.create(item=expense_name, amount=expense_price, date=expense_date, category=expense_cat, owner=email, narration=expense_narr)
            msg = "Expense entry created successfully"

        elif request.POST.get('date_wise_entry'):
            start_date = request.POST['st_date']
            end_date = request.POST['en_date']
            if start_date and end_date:
                end_date = (datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
                all_expense = all_expense.filter(date__range=[start_date,end_date], is_delete = False).order_by('-entry_date')
            elif start_date:
                all_expense = all_expense.filter(date__gte=start_date, is_delete = False).order_by('-entry_date')
            elif end_date:
                all_expense = all_expense.filter(date__lte=end_date, is_delete = False).order_by('-entry_date')

            # Graph Rendering
            cat_name = []
            values = []
            for i in all_expense:
                values.append(i.amount)
                cat_name.append(str(i.category))
            fig = go.Figure(data=[go.Pie(labels=cat_name, values=values, hole=0.3)])
            fig.show()

            # PDF Rendering
            # total = sum(i.amount for i in all_expense)
            # data = {'expenses': all_expense, 'total': total}
            # pdf = render_to_pdf('GeneratePdf.html', data)
            # return HttpResponse(pdf, content_type='application/pdf')

    context = {'add_category': add_category, 'all_expense': all_expense, 'msg': msg}
    return render(request, 'expense.html', context=context)

def update(request, id):
    if 'email' not in request.session:
        return redirect('LOGIN')
    id = int(id)
    email = SignUp.objects.get(email=request.session['email'])
    add_category = Categories.objects.filter(owner = email)
    expense_fetched = Expense.objects.get(id = id)
    if request.method == 'POST':
        categories_expense_fetched = Categories.objects.get(category = request.POST.get('item_cat'))
        expense_fetched.item = request.POST.get('item_name')
        expense_fetched.amount = request.POST.get('item_price')
        expense_fetched.date = request.POST.get('item_date')
        expense_fetched.category = categories_expense_fetched
        expense_fetched.narration = request.POST.get('item_narr')
        expense_fetched.save()
        return redirect(all_expense)
    context = {
        'item':expense_fetched.item,
        'amount':expense_fetched.amount,
        'category':expense_fetched.category,
        'date':expense_fetched.date,
        'narration':expense_fetched.narration,
        'add_category':add_category
    }
    return render(request, 'expense.html', context=context)

def delete(request,id):
    if 'email' not in request.session:
        return redirect('LOGIN')
    Expense.objects.filter(id=id).update(is_delete = True)
    return(redirect(all_expense))