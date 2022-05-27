from django.shortcuts import render
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import Monitored_Detail, Profile
from rest_framework import viewsets
from .serializers import MonitoredSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
def index(request):
	context = {

	}
	return render(request, 'index.html', context=context)

def details(request):
    profile = Profile.objects.get(user=request.user)
    device = profile.device_id
    weight = profile.weight
    age = profile.age
    gender = profile.gender
    context = {'created':[], 'heart_rate':[], 'steps':[], 'calories':[], 'labels':[], 'list_val':[]}
    try:
        readings = Monitored_Detail.objects.filter(device_id=device)
        for obj in readings:
            context['created'].append(obj.created)
            context['heart_rate'].append(obj.heart_rate)
            context['steps'].append(obj.steps)
            context['calories'].append(calculate_calories(obj.heart_rate, age, weight, obj.dance_duration, gender))
        for i in range(len(context['list_val'])):
            context['labels'].append(i)
    except Monitored_Detail.DoesNotExist:
        pass

    return render(
        request,
        'details.html',
        context=context
    )

def dashboard(request):
    context = {'heart_rate': 0, 'steps': 0, 'calories': 0, 'labels':[], 'list_val': 0}

    return render(
        request,
        'dashboard.html',
        context=context
    )    

@api_view(['GET'])
def readings(request):
    profile = Profile.objects.get(user=request.user)
    device = profile.device_id
    weight = profile.weight
    age = profile.age
    gender = profile.gender
    context = {'heart_rate': 0, 'steps': 0, 'calories': 0, 'hrThreshold' : 0}
    try:
        readings = Monitored_Detail.objects.filter(device_id=device).latest('created')
        if int(readings.heart_rate) > 100 or int(readings.heart_rate) < 60:
            context['hrThreshold'] = 1
        context['heart_rate'] = readings.heart_rate
        context['steps'] = readings.steps
        context['calories'] = calculate_calories(readings.heart_rate, age, weight, readings.dance_duration, gender)
    except Monitored_Detail.DoesNotExist:
        pass
    return Response(context)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            user.profile.device_id = form.cleaned_data.get('device_id')
            user.profile.gender = form.cleaned_data.get('gender')
            user.profile.age = form.cleaned_data.get('age')
            user.profile.weight = form.cleaned_data.get('weight')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def calculate_calories(heart_rate, age, weight, time, gender):
    calories = 0
    if gender == "M":
        calories = ((-55.0969+(.6309*heart_rate)+(0.1988*weight)+(0.2017*age))/4.184*time)
    elif gender == "F":
        calories =  ((-20.4022 + (0.4472*heart_rate)- (0.1263*weight) + (0.074*age))/4.184 * time)  
    return round(calories)

#After the serializers are created we need to create a view to the API and connect it to the Django URLs.
#Viewsets provide the advantage of combining multiple sets of logic into a single class.
class MonitoredViewSet(viewsets.ModelViewSet):
   queryset = Monitored_Detail.objects.all()
   serializer_class = MonitoredSerializer


