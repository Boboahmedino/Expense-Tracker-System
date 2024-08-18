

from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from authentication.views import login
from .models import Income,Source
from django.contrib import messages
from django.core.paginator import Paginator

# i imported line 29 like this
from services.models import Services

# Create your views here.


@login_required(login_url='authentication/login')
def income_history(request):
    income = Income.objects.filter(owner = request.user)
    paginator = Paginator(income, 3)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator,page_number)
    # currency = Services.objects.get(user = request.user).currency
    context = {'income' : income, 
               'page_obj': page_obj,
            #    'currency' : currency
            }
    categories = Source.objects.all()
    return render(request, 'dashboard/income_history.html', context)

@login_required(login_url='authentication/login')
def add_income(request):
    sources =Source.objects.all()
    context = {'sources' : sources,
               'values' : request.POST}
    
    if request.method == 'GET':   
        return render(request, 'dashboard/add_income.html', context)
        
    if request.method == 'POST':
        amount = request.POST ['amount']       
        description = request.POST['description']
        source = request.POST['source']      
        date = request.POST['transaction_date']
      
        if not amount:
            print ('Amount not specified')
            messages.error(request, 'Amount not specified')
            return render(request, 'dashboard/add_income.html', context)
        
        
        if not description:
            print ('Description not specified')
            messages.error(request, 'Description not specified')
            return render(request, 'dashboard/add_income.html', context)     
        
        
        Income.objects.create(owner = request.user, amount = amount, date = date, description = description, source = source)
        print("Income saved successfully")
        
        messages.success(request,"Your Income has been saved successfully")
        
        return redirect('income_history')
    
@login_required(login_url='authentication/login')
def edit_income(request, id):
    income = Income.objects.get(pk = id)
    sources = Source.objects.all()
    
    context = {"income" : income, 'values' : income, "sources" : sources}
    
    
    if request.method == 'GET':
        return render(request, "dashboard/edit_income.html", context)
    
    if request.method == 'POST':
        amount = request.POST ['amount']       
        description = request.POST['description']
        source = request.POST['source']      
        date = request.POST['transaction_date']
                 
        if not amount:
            print ('Amount not specified')
            messages.error(request, 'Amount not specified')
            return render(request, 'dashboard/edit_income.html', context)
        
        
        if not description:
            print ('Description not specified')
            messages.error(request, 'Description not specified')
            return render(request, 'dashboard/edit_income.html', context)     
        
        income.owner = request.user
        income.amount = amount
        income.date = date
        income.description = description
        income.source = source
        income.save()
        print("Income updated successfully")
        messages.success(request,"Your income record has been updated successfully")       
        return redirect('income_history')
  
        

def delete_income(request, id):
    income = Income.objects.get(pk=id)
    income.delete()    
    print('Your income record has been deleted')
    messages.success(request, 'Your income record has been deleted successfully')
    return redirect('income_history')
    
        
import csv    
from django.http import HttpResponse
import datetime

def csv_income(request):
    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition'] = 'attachment: filename = Transactions' + \
        str(datetime.datetime.now()) + ".csv"
    
    # from my datafram knowledge i did this
    writer  = csv.writer(response)
    writer.writerow(['Amount', 'Source', 'Description', 'Date' ])
    
    income = Income.objects.filter(owner = request.user)
    
    for income in income:
        writer.writerow([income.amount,income.category, income.description, income.date])
    return response    
