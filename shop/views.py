from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
import requests
from django.views import generic
from django.shortcuts import render
# Create your views here.
import json

def index(request):

    # polls = About.objects.all()  # For  Print all In Home page
    # context_object_name = 'latest_question_list'
   #  queryset_list = About.objects.all() 

    if request.method == 'POST':
        firstname = request.POST.get('fname')
        lastname = request.POST.get('lname')

        r = requests.get('http://api.icndb.com/jokes/random?firstName=' + firstname + '&lastName=' + lastname)
        json_data = json.loads(r.text)
        joke = json_data.get('value').get('joke')

        context = {'joker': joke }
        return render(request, 'index.html', context)
    else:
        firstname = 'Rahul '
        lastname = 'Raj '

        r = requests.get('http://api.icndb.com/jokes/random?firstName=' + firstname + '&lastName=' + lastname)
        json_data = json.loads(r.text)
        joke = json_data.get('value').get('joke')


        context = {'joker': joke}
        return render(request, 'index.html', context)
