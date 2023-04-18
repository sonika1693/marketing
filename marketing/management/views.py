from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
# from .forms import UserProfileForm

# Create your views here.
def profile(request):
    user = request.user
    if request.method == 'GET':
        try:
            user_details = UserProfile.objects.get(user = user)
            context = {
                'user_details':user_details,
            }
            return render(request,'management/profile.html',context)
        except:
            return render(request,'management/profile.html')
    else:
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        pincode = request.POST.get('pincode')

        details = UserProfile()
        details.user = user
        if name:
            details.name = name

        if email:   
            details.email = email

        if phone:
            details.phone = phone
        
        if city:
            details.city = city

        if state:
            details.state = state

        if country:
            details.country = country

        if pincode:   
            details.pincode = pincode

        details.save()
        user_details = UserProfile.objects.get(user = user)
        messages.success(request, 'Profile Updated Successfully')
        return render(request,'management/profile.html',{'user_details':user_details})
