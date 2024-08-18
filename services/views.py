from genericpath import exists
from locale import currency
from django.shortcuts import render
import os
import json
from django.conf import settings
from .models import Services
from django.contrib import messages
# Create your views here.


# This json file took me 3 days sir due to the fact that i did not know i was going to use a
# python  to load my json file
def service(request):
    currency_data = []
    
    file_path =  os.path.join(settings.BASE_DIR, 'currency.json')
    with open(file_path,'r') as json_file:
        data  = json.load(json_file)
        
        for key, val in data.items():
            currency_data.append({'name': key, 'value': val}) 
        
        # import pdb
        # pdb.set_trace()

    exists = Services.objects.filter(user = request.user).exists()   
    user_services =  None
    
    if exists:
        user_services = Services.objects.get(user = request.user)

    # import pdb
    # pdb.set_trace()
    
    if request.method == 'GET':

        return render (request, 'services/_services.html',{'currencies': currency_data,'user_services' : user_services})
                                                       
    else:
        currency = request.POST['currency']
        
        if exists:          
            # import pdb
            # pdb.set_trace()
            user_services.currency = currency
            user_services.save()
            
        else:
            Services.objects.create(user = request.user, currency = currency)    
            print('Currency saved succesfully')    
            
        messages.success(request, 'Currency saved succesfully')
        return render (request, 'services/_services.html',{'currencies': currency_data,'user_services' : user_services})
    # the user_services in the return allows the chosen/saved currency type to be shown in the select template after it has been reloaded
        
        