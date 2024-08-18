from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from authentication.views import login
from .models import Expense, Category, Profile
from django.contrib import messages
from django.core.paginator import Paginator

from services.models import Services
@login_required(login_url='authentication/login')
def profile(request):
    profiles = Profile.objects.filter(owner = request.user)
    current_user = request.user
    Full_Name = current_user.username
    Email = current_user.email
    context = {
        'profiles' : profiles,
        'values' :profiles,
        'Full_Name' : Full_Name,
        'Email' : Email, 
    }
    return render(request, "dashboard/profile.html", context)


@login_required(login_url='authentication/login')
def expense_history(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner = request.user)
    paginator = Paginator(expenses, 3)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator,page_number)
    # currency = Services.objects.get(user = request.user).currency
    context = {'expenses' : expenses,
               'page_obj': page_obj,
            #    'currency' : currency
               }
    
    return render(request, 'dashboard/expense_history.html', context)


@login_required(login_url='authentication/login')
def add_expense(request):
    categories = Category.objects.all()
    context = {'categories' : categories,
               'values' : request.POST}
    if request.method == 'GET':   
        return render(request, 'dashboard/add_expense.html', context)

    if request.method == 'POST':
        amount = request.POST ['amount']       
        description = request.POST['description']
        category = request.POST['category']      
        date = request.POST['transaction_date']
        
        # import pdb
        # pdb.set_trace()
        # this is a python debugger just like when it took me 3 days to lad the json file for currency
         
        if not amount:
            print ('Amount not specified')
            messages.error(request, 'Amount not specified')
            return render(request, 'dashboard/add_expense.html', context)
        
        
        # to specify if description is not given
        if not description:
            print ('Description not specified')
            messages.error(request, 'Description not specified')
            return render(request, 'dashboard/add_expense.html', context)     
        
        
        Expense.objects.create(owner = request.user, amount = amount, date = date, description = description, category = category)
        print("Income saved successfully")
        # print('Click to add another transaction')
        
        messages.success(request,"Your transaction has been saved successfully")
        return redirect('expense_history')
    
    
# this function creates how to edit transactions made
@login_required(login_url='authentication/login')
def edit_expense(request, id):
    # pk is an attribute that django set up automatically
    expense = Expense.objects.get(pk = id)
    categories = Category.objects.all()
    
    context = {"expense" : expense, 'values' : expense, "categories" : categories}
    
    
    # I have been using post which saves into the db
    # get retrieves what you have posted vice versa
    if request.method == 'GET':
        return render(request, "dashboard/edit_expense.html", context)
    # I copied everything i did for add expense to edit expense the explaination remains the same 
    if request.method == 'POST':
        amount = request.POST ['amount']       
        description = request.POST['description']
        category = request.POST['category']      
        date = request.POST['transaction_date']
                 
        if not amount:
            print ('Amount not specified')
            messages.error(request, 'Amount not specified')
            return render(request, 'dashboard/edit_expense.html', context)
        
        
        # to specify if description is not given
        if not description:
            print ('Description not specified')
            messages.error(request, 'Description not specified')
            return render(request, 'dashboard/edit_expense.html', context)     
        
        expense.owner = request.user
        expense.amount = amount
        expense.date = date
        expense.description = description
        expense.category = category
        expense.save()
        print("transaction updated successfully")
        messages.success(request,"Your transaction has been updated successfully")       
        return redirect('expense_history')
    
def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()    
    print('Your transaction record has been deleted')
    messages.success(request, 'Your transaction record has been deleted successfully')
    return redirect('expense_history')
    
    
import csv    
from django.http import HttpResponse
import datetime

def csv_expense(request):
    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition'] = 'attachment: filename = Transactions' + \
        str(datetime.datetime.now()) + ".csv"
    
    # from my dataframe knowledge i did this
    writer  = csv.writer(response)
    writer.writerow(['Amount', 'Category', 'Description', 'Date' ])
    
    expenses = Expense.objects.filter(owner = request.user)
    
    for expense in expenses:
        writer.writerow([expense.amount,expense.category, expense.description, expense.date])
    return response    
    


from django.contrib.auth.views import PasswordChangeView
from .forms import PasswordChangingForm
from django.urls import reverse_lazy

class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('success')


# Successful message after password change
def success(request):
    return render(request, 'dashboard/password_success.html')


# To export from database to pdf file
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.db.models import Sum

# function to create pdf
def create_pdf_report(request):
    expenses = Expense.objects.filter(owner = request.user) 
    sum = expenses.aggregate(Total= Sum('amount'))
    current_user =  request.user
    user_name = current_user.username
    email = current_user.email
    
    # template_path = 'home/pdf_output.html'
    template_path = 'dashboard/pdf.html'
    context = {
        'expenses' : expenses,
        'total' : sum,
        'user_name' : user_name,
        'email' : email,
        }
    response = HttpResponse(content_type = 'application/pdf')
    # if you want user to download immediately you use attachment.
    # response['Content-Disposition'] = 'attachment:filename = "Expense_Report.pdf"'
    # if you do not want user to download immediately but to view the file remove attachment.
    response['Content-Disposition'] = 'filename = "Expense Report.pdf"'
    template = get_template(template_path)
    html = template.render(context)

# to create pdf
    pisa_status = pisa.CreatePDF(
        html, dest = response
        )
    # if error error occurs
    if pisa_status.err:
        return HttpResponse('Some errors occured <pre>' + html + '</pre>')
    return response
 