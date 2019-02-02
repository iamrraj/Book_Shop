from django.shortcuts import render
import requests
from django.views import generic
from django.contrib import messages
from django.shortcuts import render
from .forms import SignUpForm,UpdateProfile,BookForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import Product,Categoty
import datetime
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone




class BlogCreateView(CreateView):
    model = Product
    template_name = 'addbook.html'
    fields = ['categoty', 'name', 'image','file','description','specification','seller','pub_date','available']
    success_url = '/'

# def BlogCreateView(request):
#     if request.method == "POST":
#         form = BookForm(request.POST)
#         if form.is_valid():
#             new_poll = form.save(commit=False)
#             new_poll.pub_date = datetime.datetime.now()
#             new_poll.owner = request.user
#             new_poll.save()
#             messages.success(
#                             request,
#                             'Books Added Successfully!',
#                             extra_tags='alert alert-success alert-dismissible fade show'
#                             )
#             return redirect('user_login')
#     else:
#         form = BookForm()
#     context = {'form': form}
#     return render(request, 'addbook.html', context)

def BlogListView(request):
    
    time = timezone.now().date()
    contact_list = Product.objects.all()
    search_term=''
    # if request.user.is_staff or request.user.is_superuser:
    #     contact_list = Post.objects.all()

    # query = request.GET.get("q")
    # if query:
    #     contact_list= Post.filter(title_iconatins=query)
    #     return render(request, 'home.html')
                      

    if 'q' in request.GET:
        search_term = request.GET['q']
        contact_list = contact_list.filter(Q(name__icontains=search_term)|
                                           Q(seller__icontains=search_term)).distinct()
        

                        # Q(author=query)
                        # # ).distinct()
    paginator = Paginator(contact_list, 12) # Show 4 contacts per page

    page = request.GET.get('page')
    contacts = paginator.get_page(page)
    return render(request, 'booklist.html', {'contacts': contacts})



class CatCreateView(CreateView):
    model = Categoty
    template_name = 'addcat.html'
    fields = ['name']
    success_url = '/'


@login_required
def detail(request):
    return render(request, 'detail.html')


@login_required
def special(request):
    return HttpResponse("You are logged in !")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


# def register(request):
#     registered = False
#     if request.method == 'POST':
#         user_form = SignUpForm(data=request.POST)
#         profile_form = UpdateProfile(data=request.POST)
#         if user_form.is_valid() and profile_form.is_valid():
#             user = user_form.save()
#             user.set_password(user.password)
#             user.save()
#             profile = profile_form.save(commit=False)
#             profile.user = user
#             if 'profile_pic' in request.FILES:
#                 print('found it')
#                 profile.profile_pic = request.FILES['profile_pic']
#             profile.save()
#             registered = True
#         else:
#             print(user_form.errors,profile_form.errors)
#     else:
#         user_form = SignUpForm()
#         profile_form = UpdateProfile()
#     return render(request,'registration.html',
#                           {'user_form':user_form,
#                            'profile_form':profile_form,
#                                                       'registered':registered})

def register(request):
    registered = False
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'registration.html', {'form': form})




def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'login.html', {})



class ProductDetailView(DetailView):
    model = Product
    template_name = 'bookdetail.html'