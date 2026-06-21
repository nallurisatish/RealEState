from django.shortcuts import render,get_object_or_404
from .models import Property
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PropertySerializer
from django.core.mail import send_mail

def home(request):
    properties = Property.objects.all()

    return render(
        request,
        'index.html',
        {'properties': properties}
    )
def property_detail(request, id):
    property = get_object_or_404(
        Property,
        id=id
    )

    return render(
        request,
        'detail.html',
        {'property': property}
    )
def register(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            return redirect('login')

    return render(request, 'register.html', {'form': form})
def user_login(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect('/')

    return render(request, 'login.html')
def user_logout(request):
    logout(request)
    return redirect('/')

@login_required
def dashboard(request):

    favorites = Favorite.objects.filter(
        user=request.user
    )

    return render(
        request,
        'dashboard.html',
        {'favorites': favorites}
    )
def home(request):

    properties = Property.objects.all()

    search = request.GET.get('search')
    location = request.GET.get('location')
    category = request.GET.get('category')

    if search:
        properties = properties.filter(
            title__icontains=search
        )

    if location:
        properties = properties.filter(
            location__icontains=location
        )

    if category:
        properties = properties.filter(
            category=category
        )

    paginator = Paginator(properties, 6)

    page_number = request.GET.get('page')

    properties = paginator.get_page(page_number)

    return render(
        request,
        'index.html',
        {'properties': properties}
    )
@api_view(['GET'])
def api_properties(request):

    properties = Property.objects.all().order_by('-id')

    serializer = PropertySerializer(
        properties,
        many=True
    )

    return Response(serializer.data)
@api_view(['GET'])
def api_property(request, id):

    property = Property.objects.get(id=id)

    serializer = PropertySerializer(property)

    return Response(serializer.data)

from django.contrib.auth.decorators import login_required

@login_required
def add_favorite(request, id):

    property = Property.objects.get(id=id)

    Favorite.objects.get_or_create(
        user=request.user,
        property=property
    )

    return redirect('dashboard')
@login_required
def dashboard(request):

    favorites = Favorite.objects.filter(
        user=request.user
    )

    return render(
        request,
        'dashboard.html',
        {'favorites': favorites}
    )
from .models import Favorite, Inquiry

@login_required
def dashboard(request):

    favorites = Favorite.objects.filter(
        user=request.user
    )

    inquiries = Inquiry.objects.filter(
        email=request.user.email
    )

    return render(
        request,
        'dashboard.html',
        {
            'favorites': favorites,
            'inquiries': inquiries,
        }
    )